CREATE TABLE IF NOT EXISTS users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    logged_token VARCHAR(512)
);


CREATE TABLE IF NOT EXISTS recipes(
	recipeid SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT[] NOT NULL,
    directions TEXT[],
    from_source TEXT DEFAULT NULL,
    from_link TEXT,
	ner TEXT[]
);

CREATE TABLE IF NOT EXISTS comments(
	userid INT,
	recipeid INT,
	comment TEXT NOT NULL,
	FOREIGN KEY (recipeid) REFERENCES recipes(recipeid)
);

CREATE TABLE IF NOT EXISTS categories(
	category VARCHAR(50) PRIMARY KEY,
	recipes integer[]
);

COPY recipes(recipeid, title, ingredients, directions, from_source, from_link, ner)
FROM 'project-report\recipes.csv'
DELIMITER ','

SELECT userid FROM users WHERE userid=1;

INSERT INTO users (username, password) VALUES ('Administrator', 'cse460temp');

ALTER TABLE recipes 
DROP COLUMN IF EXISTS from_link;

ALTER TABLE recipes 
RENAME COLUMN ingredients TO ingredients_amount;

ALTER TABLE recipes 
RENAME COLUMN ner TO ingredients;

ALTER TABLE recipes 
ADD COLUMN IF NOT EXISTS userid INT NOT NULL DEFAULT 1;

ALTER TABLE recipes 
ADD CONSTRAINT recipe_userid_reference_user
FOREIGN KEY (userid) 
REFERENCES users(userid);


ALTER TABLE users ALTER COLUMN password TYPE character varying(512);


UPDATE users 
SET password=('hashed_password') 
WHERE username = 'Administrator';


select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,chicken,%'
INSERT INTO categories (category, recipes) VALUES ('Chicken', %s);

select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,beef,%'
INSERT INTO categories (category, recipes) VALUES ('Beef', %s);

select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,fish,%'
INSERT INTO categories (category, recipes) VALUES ('Fish', %s);

select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,pork,%'
INSERT INTO categories (category, recipes) VALUES ('Pork', %s);

select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,tofu,%'
INSERT INTO categories (category, recipes) VALUES ('Tofu', %s)


CREATE VIEW category_count AS
SELECT category, cardinality(recipes)
FROM categories
GROUP BY category
ORDER BY cardinality(recipes) DESC

ALTER TABLE recipes DROP CONSTRAINT recipe_userid_reference_user;

CREATE OR REPLACE FUNCTION userid_delete() RETURNS TRIGGER AS 
$BODY$
BEGIN
	DELETE FROM comments
	WHERE comments.userid=OLD.userid;
	RETURN NULL;
END;
$BODY$
language plpgsql;

CREATE trigger useid_check
AFTER DELETE ON users
FOR EACH ROW 
EXECUTE PROCEDURE userid_delete();
