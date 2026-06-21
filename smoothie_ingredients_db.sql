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
	grams DECIMAL(6,2),
	FOREIGN KEY (smoothie_id) REFERENCES smoothies(smoothie_id) ON DELETE CASCADE,
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE);

INSERT INTO smoothie_ingredients (smoothie_id, ingredient_id, grams) VALUES
	(1, 1, 200), (1, 2, 300), (1, 3, 250),
	(2, 1, 200), (2, 5, 100), (2, 9, 450),
	(3, 9, 450), (3, 10, 150), (3, 2, 300),
	(4, 1, 200), (4, 2, 300), (4, 3,250), (4, 4, 125), (4, 5, 100), (4, 6, 50), (4, 7, 300), (4, 8, 150), (4, 9, 450), (4, 10, 150), (4, 11, 400),
	(5, 6, 50), (5, 1, 200), (5, 2, 350), (5, 5, 100),
	(6, 8, 150), (6, 10, 150), (6, 9, 450), (6, 2, 300),
	(7, 7, 300), (7, 2, 300), (7, 8, 150),
	(8, 3, 250), (8, 4, 125), (8, 2, 300),
	(9, 9, 450), (9, 2, 300), (9, 11, 400), (9, 3, 250),
	(10, 6, 50), (10, 1, 200), (10, 5, 100), (10, 10, 150);

select * from smoothies;
select * from ingredients;
drop table smoothie_ingredientsd;
drop table ingredients;
drop table smoothies;
drop database smoothie_ingredients_db;

DELETE FROM ingredients WHERE ingredient_id = 2;
