CREATE DATABASE buyme;
USE buyme;


DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  f_name VARCHAR(50),
  l_name VARCHAR(50),
  user_type ENUM('customer', 'representative', 'admin') NOT NULL
);
SELECT * FROM USERS;


DROP TABLE IF EXISTS category;
CREATE TABLE category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(50) NOT NULL,
  parent_id INT DEFAULT NULL,
  FOREIGN KEY (parent_id) REFERENCES category(category_id)
);

INSERT INTO category (category_name, parent_id) VALUES 
('Electronics', NULL),
('Laptops', 1),
('Gaming Laptops', 2),
('Phones', 1),
('Cameras', 1);

SELECT * FROM CATEGORY;

DROP TABLE IF EXISTS item;
CREATE TABLE item (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  item_name VARCHAR(255) NOT NULL,
  item_desc TEXT,
  category_id INT,
  FOREIGN KEY (category_id) REFERENCES category(category_id)
);

SELECT * FROM ITEM;

DROP TABLE IF EXISTS auctions;
CREATE TABLE auctions (
  auction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  item_id INT NOT NULL,
  user_id INT NOT NULL,
  starting_price DECIMAL(12,2) NOT NULL,
  auction_start DATETIME NOT NULL,
  auction_end DATETIME NOT NULL,
  current_highest_bid DECIMAL(12,2) DEFAULT NULL,
  FOREIGN KEY (item_id) REFERENCES item(item_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
SELECT * FROM AUCTIONS;

DROP TABLE IF EXISTS bid;
CREATE TABLE bid (
  bid_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  auction_id BIGINT UNSIGNED NOT NULL,
  user_id INT NOT NULL,
  bid_price DECIMAL(12,2) NOT NULL,
  bid_status ENUM('PLACED','LEADING','OUTBID','RETRACTED','INVALID','WON','LOST') NOT NULL,
  auction_bid_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (auction_id) REFERENCES auctions(auction_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
SELECT * FROM BID ;