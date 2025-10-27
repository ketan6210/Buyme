-- SQLite Schema for BuyMe application

DROP TABLE IF EXISTS bid;
DROP TABLE IF EXISTS auctions;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS user;

-- User table (singular to match your code)
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    user_type VARCHAR(20) NOT NULL CHECK(user_type IN ('customer', 'representative', 'admin'))
);

-- Category table
CREATE TABLE category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL,
    parent_id INTEGER DEFAULT NULL,
    FOREIGN KEY (parent_id) REFERENCES category(category_id)
);

INSERT INTO category (category_name, parent_id) VALUES 
('Electronics', NULL),
('Laptops', 1),
('Gaming Laptops', 2),
('Phones', 1),
('Cameras', 1);

-- Item table
CREATE TABLE item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name VARCHAR(255) NOT NULL,
    item_desc TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

-- Auctions table
CREATE TABLE auctions (
    auction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    starting_price DECIMAL(12,2) NOT NULL,
    auction_start DATETIME NOT NULL,
    auction_end DATETIME NOT NULL,
    current_highest_bid DECIMAL(12,2) DEFAULT NULL,
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Bid table
CREATE TABLE bid (
    bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    bid_price DECIMAL(12,2) NOT NULL,
    bid_status VARCHAR(20) NOT NULL CHECK(bid_status IN ('PLACED','LEADING','OUTBID','RETRACTED','INVALID','WON','LOST')),
    auction_bid_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (auction_id) REFERENCES auctions(auction_id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);