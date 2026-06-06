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
