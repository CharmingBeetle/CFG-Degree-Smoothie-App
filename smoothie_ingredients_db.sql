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

-- create smoothie_ingredients table and insert data.

CREATE TABLE smoothie_ingredients (
	smoothie_ingredient_id INT auto_increment PRIMARY KEY,
	smoothie_id INT,
	ingredient_id INT,
	quantity INT,
	FOREIGN KEY (smoothie_id) REFERENCES smoothies(smoothie_id),
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id));

INSERT INTO smoothie_ingredients (smoothie_id, ingredient_id, quantity) VALUES
	(1, 1, 2), (1, 2, 2), (1, 3, 11), -- INSERT for 'Append and Blend' -- x2 apples, x2 bananas, x11 blackcurrants
	(2, 1, 2), (2, 5, 3), (2, 9, 0.5), -- INSERT for 'Debug and Detox' -- x2 apples, x3 kiwis, x0.5 pineapple
	(3, 9, 0.5), (3, 10, 15), (3, 2, 2), -- INSERT for 'Flask and Fruit'-- x0.5 pineapple, x15 raspberries, x2 bananas
	(4, 1, 1), (4, 2, 1.5), (4, 3, 5), (4, 4, 10), (4, 5, 0.5), (4, 6, 0.25), (4, 7, 0.25), (4, 8, 5), (4, 9, 1), (4, 10, 10), (4, 11, 12), -- INSERT for 'Infinite Fruit Loop' -- x1 apple, x1.5 bananas, x5 blackcurrants, x10 blueberries, x0.5 kiwi, x0.5 lime, x0.25 mangos, x5 oranges, x1 pineapple, x10 raspberries, x12 strawberries
	(5, 6, 4), (5, 1, 6), (5, 2, 6), (5, 5, 2), -- INSERT for Lambda and Lime -- x4 limes, x6 apples, x6 bananas, x2 kiwis
	(6, 8, 4), (6, 10, 15), (6, 11, 15), (6, 2, 3), -- INSERT for '__main__ Squeeze' -- x4 oranges, x15 raspberries, x15 strawberries, x3 bananas
	(7, 7, 5), (7, 2, 4), (7, 8, 2.5), -- INSERT for 'Mutable Mango' -- x5 mangos, x4 bananas, x2.5 oranges
	(8, 3, 30), (8, 4, 35), (8, 2, 4), -- INSERT for 'Return Smoothie' -- x30 blackcurrants, x35 blueberries, x4 bananas
	(9, 9, 1), (9, 2, 5), (9, 11, 8), (9, 3, 10), -- INSERT for 'Smooth Operator' -- x1 pineapple, x5 bananas, x8 strawberries, x10 blackcurrants
	(10, 6, 2), (10, 1, 5), (10, 5, 1.75), (10, 10, 20); -- INSERT for 'Smooth Operator' -- x2 limes, x5 apples, x1.75 kiwis, x20 raspberries
		
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- code for viewing all tables individually.

select * from smoothies order by smoothie_id asc;
select * from ingredients order by ingredient_id asc;
select * from smoothie_ingredients order by smoothie_ingredient_id;

-- code for viewing joined tables.
SELECT 
	s.smoothie_name,
	i.ingredient_name,
	quantity
FROM smoothie_ingredients si
JOIN smoothies s
ON si.smoothie_id = s.smoothie_id
JOIN ingredients i
ON si.ingredient_id = i.ingredient_id
GROUP BY
	s.smoothie_name, 
	i.ingredient_name,
	quantity
ORDER BY 
	s.smoothie_name,
	i.ingredient_name;

-- code to drop tables and database.
DROP TABLE smoothies;
DROP TABLE ingredients;
DROP TABLE smoothie_ingredients;
DROP database smoothie_ingredients_db;