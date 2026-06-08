-- create and use smoothie_ingredients_db.

CREATE DATABASE IF NOT EXISTS smoothie_ingredients_db;

USE smoothie_ingredients_db;

-- create smoothies table and insert data.

CREATE TABLE smoothies (
	smoothie_id INT AUTO_INCREMENT PRIMARY KEY,
	smoothie_name VARCHAR(50) UNIQUE NOT NULL);

INSERT INTO smoothies (smoothie_name) VALUES 
	('Append and Blend'),
	('Debug and Detox'),
	('Flask of Fruit'),
	('Infinite Fruit Loop'),
	('Lambda and Lime'),
	('__main__ Squeeze'),
	('Mutable Mango'),
	('Return Smoothie'),
	('Smooth Operator'),
	('Zip() and Sip()');

-- create ingredients table and insert data.

CREATE TABLE ingredients (
	ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
	ingredient_name VARCHAR(50) UNIQUE NOT NULL,
	calories DECIMAL(6,2),
	protein_g DECIMAL(6,2),
	carbohydrates_g DECIMAL(6,2),
	sugar_g DECIMAL(6,2),
	fat_g DECIMAL(6,2));

INSERT INTO ingredients (ingredient_name, calories, protein_g, carbohydrates_g, sugar_g, fat_g) VALUES
	('Apple', 52, 0.3, 13.8, 10.4, 0.2),
	('Banana', 89, 1.1, 22.8, 12.2, 0.3),
	('Blackcurrants', 63, 1.4, 15.4, 6.8, 0.4),
	('Blueberries', 57, 0.7, 14.5, 10, 0.3),
	('Kiwi', 61, 1.1, 14.7, 9, 0.5),
	('Lime', 30, 0.7, 10.5, 1.7, 0.2),
	('Mango', 60, 0.8, 15, 13.7, 0.4),
	('Orange', 47, 0.9, 11.8, 9.4, 0.1),
	('Pineapple', 50, 0.5, 13.1, 9.9, 0.1),
	('Raspberries', 52, 1.2, 11.9, 4.4, 0.7),
	('Strawberries', 32, 0.7, 7.7, 4.9, 0.3);

-- create smoothie_ingredients table and insert data.

CREATE TABLE smoothie_ingredients (
	smoothie_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
	smoothie_id INT,
	ingredient_id INT,
	quantity INT,
	FOREIGN KEY (smoothie_id) REFERENCES smoothies(smoothie_id),
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id));

INSERT INTO smoothie_ingredients (smoothie_id, ingredient_id, quantity) VALUES
	(1, 1, 2), (1, 2, 2), (1, 3, 11),
	(2, 1, 2), (2, 5, 3), (2, 9, 0.5),
	(3, 9, 0.5), (3, 10, 15), (3, 2, 2),
	(4, 1, 1), (4, 2, 1.5), (4, 3, 5), (4, 4, 10), (4, 5, 0.5), (4, 6, 0.25), (4, 7, 0.25), (4, 8, 5), (4, 9, 1), (4, 10, 10), (4, 11, 12),
	(5, 6, 4), (5, 1, 6), (5, 2, 6), (5, 5, 2),
	(6, 8, 4), (6, 10, 15), (6, 11, 15), (6, 2, 3),
	(7, 7, 5), (7, 2, 4), (7, 8, 2.5),
	(8, 3, 30), (8, 4, 35), (8, 2, 4),
	(9, 9, 1), (9, 2, 5), (9, 11, 8), (9, 3, 10),
	(10, 6, 2), (10, 1, 5), (10, 5, 1.75), (10, 10, 20);