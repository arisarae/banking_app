CREATE DATABASE banking_management;
USE banking_management;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- store hashed password
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    account_type VARCHAR(255) NOT NULL, -- checking, savings, etc
    account_number VARCHAR(255) UNIQUE NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    from_account_id INTEGER, -- optional for transfer
    FOREIGN KEY (from_account_id) REFERENCES accounts(id),
    to_account_id INTEGER, -- optional for deposit
    FOREIGN KEY (to_account_id) REFERENCES accounts(id),
    amount DECIMAL(10, 2) NOT NULL,
    type VARCHAR(255), -- deposit, withdrawal, transfer, etc
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

select * from users;
select * from accounts;
select * from transactions;