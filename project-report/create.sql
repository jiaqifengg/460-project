CREATE TABLE IF NOT EXISTS users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    logged_token VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS comments(
    userid INT UNIQUE,
    recipeid INT UNIQUE,
    comment TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (recipeid) REFERENCES recipes(recipeid)
);

COPY persons(first_name, last_name, dob, email)
FROM 'C:...\CSE 460\Project\460-project\460-project\project-report\recipes.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS recipes(
    recipeid SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT[] NOT NULL,
    directions TEXT[],
    from_source TEXT DEFAULT NULL,
    from_link TEXT,
    ner TEXT[]
);

SELECT userid FROM users WHERE userid=1;
INSERT INTO users (username, password) VALUES ('Administrator', 'cse460temp');
ALTER TABLE recipes DROP COLUMN IF EXISTS from_link;
ALTER TABLE recipes RENAME COLUMN ingredients TO ingredients_amount;
ALTER TABLE recipes RENAME COLUMN ner TO ingredients;
ALTER TABLE recipes ADD COLUMN IF NOT EXISTS userid INT NOT NULL DEFAULT 1;

ALTER TABLE recipes ADD CONSTRAINT recipe_userid_reference_user FOREIGN KEY (userid) REFERENCES users(userid);

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