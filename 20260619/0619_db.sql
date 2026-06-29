CREATE DATABASE EXAM01;

USE EXAM01;

CREATE TABLE member(
	id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    regdate DATETIME DEFAULT NOW()
);

INSERT INTO member(username, password, name, email) VALUES('test','test12','테스트', 'email@email.com');
SELECT * FROM member;


CREATE TABLE product(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    price INT NOT NULL,
    stock INT,	-- 재고 수량
    created_at DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE order_header(
	id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    total_price INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK(status IN('ready','paid', 'shipping', 'done', 'cancel')),
    FOREIGN KEY (member_id) REFERENCES member(id)
);

CREATE TABLE order_item(
	id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES order_header(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE payment(
	id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    method VARCHAR(20) NOT NULL CHECK(method IN('card', 'bank', 'easy')),
    paid_amount INT NOT NULL,
    paid_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (order_id) REFERENCES order_header(id)
);



INSERT INTO product(name, price, stock) VALUES('가방', 50000, 5), 
											  ('지갑', 40000, 3), 
                                              ('과자', 1000, 6), 
                                              ('음식', 5000, 2),
                                              ('품절템', 2000, 0);

-- 맘편히 유저 생성
CREATE USER 'AAA'@'localhost' IDENTIFIED BY '1111';
GRANT ALL ON EXAM01.* TO 'AAA'@'localhost';


SELECT * FROM product;

DROP TABLE product;