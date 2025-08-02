CREATE DATABASE IF NOT EXISTS expense_db;

USE expense_db;

CREATE TABLE IF NOT EXISTS expenses (
      id INT AUTO_INCREMENT PRIMARY KEY,
      amount DECIMAL(10,2) NOT NULL,
      category ENUM('Food','Travel','Shopping','Rent','Other') NOT NULL,
      date DATE NOT NULL,
      description TEXT
  );
