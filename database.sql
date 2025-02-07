CREATE DATABASE job_test_db;
USE job_test_db;

CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    match_score FLOAT NOT NULL
);
