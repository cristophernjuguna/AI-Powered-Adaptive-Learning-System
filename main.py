import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import SubmitAnswerRequest, SubmitAnswerResponse, StudentProgress
from app.db import DB
from app.groq_client import (
    build_wrong_answer_prompt,
    build_correct_answer_prompt,
    call_groq,
)

app = FastAPI(title="AI‑Powered Adaptive Learning System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DB()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


async def update_performance_history(conn, student_id: int, topic: str):
    row = await conn.fetchrow(
        """
        SELECT
            AVG(CASE WHEN qr.is_correct THEN 1.0 ELSE 0.0 END) AS avg_score,
            AVG(qr.response_time_ms)::int AS avg_time_ms,
            COUNT(*)::int AS num_quizzes
        FROM quiz_results qr
        JOIN quiz_questions qq ON qq.id = qr.question_id
        WHERE qr.student_id = $1
          AND qq.topic = $2
        """,
        student_id,
        topic,
    )

    if row and row["num_quizzes"] > 0:
        await conn.execute(
            """
            INSERT INTO performance_history (
                student_id,
                topic,
                avg_score,
                avg_time_ms,
                num_quizzes,
                updated_at
            )
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT (student_id, topic)
            DO UPDATE SET
                avg_score = EXCLUDED.avg_score,
                avg_time_ms = EXCLUDED.avg_time_ms,
                num_quizzes = EXCLUDED.num_quizzes,
                updated_at = NOW()
            """,
            student_id,
            topic,
            row["avg_score"],
            row["avg_time_ms"],
            row["num_quizzes"],
        )


@app.post("/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(req: SubmitAnswerRequest):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT correct_index, topic, question_text, choice0, choice1, choice2, choice3
            FROM quiz_questions
            WHERE id = $1
            """,
            req.question_id,
        )
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")

        correct_index = row["correct_index"]
        is_correct = req.choice_given == correct_index

        choices = [
            row["choice0"],
            row["choice1"],
            row["choice2"],
            row["choice3"],
        ]

        if req.choice_given < 0 or req.choice_given > 3:
            raise HTTPException(status_code=400, detail="choice_given must be between 0 and 3")

        student_answer = choices[req.choice_given]
        correct_answer = choices[correct_index]
        topic = row["topic"]
        question_text = row["question_text"]

    if not is_correct:
        prompt = build_wrong_answer_prompt(
            topic=topic,
            question=question_text,
            student_answer=student_answer,
            correct_answer=correct_answer,
        )
    else:
        prompt = build_correct_answer_prompt(
            topic=topic,
            question=question_text,
            student_answer=student_answer,
        )

    ai_feedback = "We're having trouble contacting the AI right now."
    next_challenge = None

    for attempt in range(3):
        try:
            ai_feedback = await call_groq(prompt)
            break
        except Exception as e:
            print(f"Groq call failed (attempt {attempt + 1}): {e}")
            await asyncio.sleep(1 * (2 ** attempt))

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO quiz_results (
                        student_id,
                        question_id,
                        choice_given,
                        is_correct,
                        ai_feedback,
                        response_time_ms
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    req.student_id,
                    req.question_id,
                    req.choice_given,
                    is_correct,
                    ai_feedback,
                    req.response_time_ms,
                )

                await update_performance_history(conn, req.student_id, topic)
    except Exception as e:
        print(f"Failed to save result for student={req.student_id}: {e}")

    return SubmitAnswerResponse(
        is_correct=is_correct,
        ai_feedback=ai_feedback,
        next_challenge=next_challenge,
    )


@app.get("/student-progress/{student_id}", response_model=list[StudentProgress])
async def student_progress(student_id: int):
    rows = await db.fetchall(
        """
        SELECT topic, avg_score, avg_time_ms, num_quizzes
        FROM performance_history
        WHERE student_id = $1
        ORDER BY topic
        """,
        student_id,
    )

    return [
        StudentProgress(
            student_id=student_id,
            topic=r["topic"],
            avg_score=r["avg_score"],
            avg_time_ms=r["avg_time_ms"],
            num_quizzes=r["num_quizzes"],
        )
        for r in rows
    ]


@app.get("/analytics/struggling")
async def struggling_students():
    rows = await db.fetchall(
        """
        SELECT
          s.id AS student_id,
          s.name,
          AVG(ph.avg_score) AS overall_avg
        FROM students s
        JOIN performance_history ph ON s.id = ph.student_id
        GROUP BY s.id, s.name
        HAVING AVG(ph.avg_score) < 0.5
        ORDER BY overall_avg
        """
    )
    return [dict(row) for row in rows]


@app.get("/analytics/hardest-topic")
async def hardest_topic():
    rows = await db.fetchall(
        """
        SELECT
          topic,
          AVG(avg_score) AS avg_score
        FROM performance_history
        GROUP BY topic
        ORDER BY avg_score ASC
        LIMIT 3
        """
    )
    return [dict(row) for row in rows]


@app.get("/analytics/student-report/{student_id}")
async def student_report(student_id: int):
    rows = await db.fetchall(
        """
        SELECT
          topic,
          avg_score,
          avg_time_ms,
          num_quizzes
        FROM performance_history
        WHERE student_id = $1
        ORDER BY avg_score
        """,
        student_id,
    )
    return [dict(row) for row in rows]