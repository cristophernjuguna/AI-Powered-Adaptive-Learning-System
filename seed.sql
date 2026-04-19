
INSERT INTO quiz_questions (
  topic, question_text, choice0, choice1, choice2, choice3, correct_index
) VALUES

-- EXCEL (5)
('Excel','Which function is used to sum values?','SUM()','ADD()','TOTAL()','PLUS()',0),
('Excel','What does VLOOKUP do?','Formats cells','Searches vertically','Creates charts','Deletes rows',1),
('Excel','Which symbol starts a formula in Excel?','#','=','@','$',1),
('Excel','What is a Pivot Table used for?','Writing text','Data summarization','Drawing shapes','Printing sheets',1),
('Excel','Which function counts numeric values?','COUNT()','COUNTA()','COUNTIF()','SUM()',0),

-- PYTHON (5)
('Python','Which keyword defines a function?','func','def','function','define',1),
('Python','What data type is [1,2,3]?','Tuple','List','Set','Dictionary',1),
('Python','Which symbol is used for comments?','//','#','<!--','--',1),
('Python','What does len() do?','Adds numbers','Counts items','Deletes items','Sorts list',1),
('Python','Which loop is used for iteration?','loop','for','repeat','iterate',1),

-- MACHINE LEARNING (5)
('Machine Learning','What is supervised learning?','Learning without data','Learning with labeled data','Random guessing','Manual coding',1),
('Machine Learning','Which is a classification algorithm?','Linear Regression','KNN','PCA','Clustering',1),
('Machine Learning','What is overfitting?','Model too simple','Model memorizes data','Model crashes','Data loss',1),
('Machine Learning','Which metric evaluates classification?','MSE','Accuracy','Mean','Sum',1),
('Machine Learning','What is a feature?','Output','Input variable','Error','Prediction',1),

-- POWER BI (5)
('Power BI','What is Power BI used for?','Coding','Data visualization','Gaming','Networking',1),
('Power BI','What language is used in Power BI formulas?','SQL','DAX','Python','Java',1),
('Power BI','What is a dashboard?','Raw data','Collection of visuals','Database','Query tool',1),
('Power BI','What does Power Query do?','Visualizes data','Transforms data','Deletes data','Prints reports',1),
('Power BI','Which chart shows trends over time?','Pie chart','Line chart','Bar chart','Table',1);

INSERT INTO students (name, email, created_at)
VALUES
('mary wambui','wambui@gmail.com',NOW()),
('john kamau','kamau@gmail.com',NOW()),
('faith njeri','njeri@gmail.com',NOW()),
('peter otieno','otieno@gmail.com',NOW()),
('lilian chebet','chebet@gmail.com',NOW()),
('daniel mutua','mutua@gmail.com',NOW()),
('grace akinyi','akinyi@gmail.com',NOW()),
('brian mwangi','mwangi@gmail.com',NOW()),
('susan wanjiku','wanjiku@gmail.com',NOW()),
('kevin kiptoo','kiptoo@gmail.com',NOW()),
('esther nyambura','nyambura@gmail.com',NOW()),
('james odhiambo','odhiambo@gmail.com',NOW()),
('ruth chepkemoi','chepkemoi@gmail.com',NOW()),
('samuel kariuki','kariuki@gmail.com',NOW()),
('agnes anyango','anyango@gmail.com',NOW()),
('victor kiprotich','kiprotich@gmail.com',NOW()),
('lucy wangari','wangari@gmail.com',NOW()),
('george kimani','kimani@gmail.com',NOW()),
('ann wairimu','wairimu@gmail.com',NOW()),
('david njuguna','njuguna@gmail.com',NOW());