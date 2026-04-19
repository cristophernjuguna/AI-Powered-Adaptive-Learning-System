# AI-Powered-Adaptive-Learning-Syste
Project Summary
This project is an AI-powered adaptive learning system built with FastAPI, Groq API, and Aiven PostgreSQL. The goal of the system is to provide personalized feedback to students based on their quiz performance and to give teachers useful analytics about student progress. The application accepts student answers, determines whether the response is correct, generates tailored feedback using an AI model, stores the result in a cloud database, and summarizes learning progress over time.

The system was designed to be beginner-friendly while still demonstrating a practical real-world backend architecture. It includes clear separation of concerns across the database layer, AI integration layer, and API routing layer.

System Design
The application is structured around three main database tables:

Students: stores basic learner information such as name, email, and registration time.

Quiz Results: stores each student submission, including the selected answer, correctness, response time, and AI-generated feedback.

Performance History: stores aggregated performance data by topic for each student, such as average score, average response time, and total number of attempts.

This structure allows the system to preserve detailed quiz history while also maintaining a summarized view of student progress for analytics and reporting.

Core Functionality
The main endpoint, POST /submit-answer, performs the following steps:

Receives the student’s answer.

Looks up the correct answer from the database.

Determines whether the response is correct.

Builds a Groq prompt based on whether the answer is right or wrong.

Sends the prompt to Groq and receives personalized feedback.

Saves the quiz result and AI feedback in PostgreSQL.

Updates the student’s performance history.

Returns the response to the client immediately.

Additional endpoints support analytics and progress tracking:

GET /student-progress/{student_id} returns topic-level performance for one student.

GET /analytics/struggling identifies students with low overall performance.

GET /analytics/hardest-topic shows the most difficult topics based on average scores.

GET /analytics/student-report/{student_id} provides a detailed report for one student.

Challenges Encountered and Solutions
Several technical issues arose during development, and each one was resolved systematically:

1. Python import and application startup issues
Initially, the application could not start because of import path problems in the FastAPI project structure.

Solution:
The project was reorganized into a proper package structure, and the application was run using the correct module path. This resolved the import errors and allowed the FastAPI server to start successfully.

2. Database schema errors
At first, the application failed because the required PostgreSQL tables had not yet been created in the correct database.

Solution:
The database schema was created manually in Aiven PostgreSQL, and sample data was inserted to support testing. This ensured that the backend could query and update the expected tables.

3. Connection pool limits
The application initially tried to open too many PostgreSQL connections, which exceeded the limits of the Aiven service plan.

Solution:
The connection pool size was reduced to a small number suitable for development. This stabilized the database connection and prevented connection exhaustion.

4. Incorrect AI response parsing
The first version of the Groq integration returned an incorrect value instead of the model’s actual text response.

Solution:
The Groq client code was updated to read the assistant message content properly from the API response. This ensured that the feedback shown to students was meaningful and human-readable.

5. Input validation errors
The system crashed when invalid answer indexes were submitted.

Solution:
Validation was added to the request model and reinforced in the route handler. This prevented out-of-range values from reaching the list lookup and improved API reliability.

6. Summary data not updating automatically
Although quiz attempts were being saved, the summary table for student progress was not updating at first.

Solution:
A helper function was introduced to recalculate and upsert student-topic performance after each submission. This ensured that the analytics endpoints always reflected the latest performance data.

Testing and Verification
The system was tested using FastAPI’s interactive documentation, direct HTTP requests, and SQL queries in PostgreSQL. Testing confirmed that:

correct answers return encouraging feedback,

wrong answers return explanatory feedback,

all quiz attempts are stored correctly,

performance summaries are updated automatically,

and analytics endpoints return meaningful results.

Outcome
The final system demonstrates how AI can be integrated into a backend application to create a more personalized learning experience. It goes beyond a simple quiz application by combining real-time AI feedback, persistent storage, and analytics into one coherent workflow. The result is a functional and extensible adaptive learning backend that can support both students and teachers.

Future Improvements
Possible future enhancements include:

adding a frontend interface,

implementing authentication for students and teachers,

supporting multiple teachers and classes,

generating new quiz questions dynamically,

improving observability and logging,

and introducing caching or batching to reduce AI usage cost.

Conclusion
This project successfully demonstrates the use of FastAPI, Groq API, and Aiven PostgreSQL in a practical educational application. It shows how AI can be used to support adaptive learning by providing personalized feedback, storing progress data, and enabling useful analytics for instructors. The development process also provided valuable experience in backend architecture, database design, API integration, and debugging real-world issues.
