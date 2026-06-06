-- create and use smoothie_ingredients_db.

CREATE database IF NOT EXISTS smoothie_ingredients_db;

use smoothie_ingredients_db;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- create smoothies table and insert data.

CREATE TABLE smoothies (
	smoothie_id INT auto_increment PRIMARY KEY,
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- create ingredients table and insert data.

CREATE TABLE ingredients (
	ingredient_id INT auto_increment PRIMARY KEY,
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

