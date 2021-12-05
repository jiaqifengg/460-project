CREATE VIEW category_count AS
SELECT category, cardinality(recipes)
FROM categories
GROUP BY category
ORDER BY cardinality(recipes) DESC

INSERT INTO users (username, password) VALUES (%s, %s)

SELECT password FROM users WHERE username=(%s)

UPDATE users SET logged_token=%s WHERE username=%s

SELECT userid, username FROM users WHERE logged_token=(%s)

SELECT * FROM recipes WHERE %s && ingredients

SELECT userid FROM users WHERE userid=%s

SELECT recipeid FROM recipes WHERE recipeid=%s

INSERT INTO comments (userid, recipeid, comment) VALUES (%s, %s, %s)
SELECT username FROM users WHERE userid=%s

SELECT recipes FROM categories WHERE category=%s
UNION
SELECT recipes FROM categories WHERE category=%s

SELECT * FROM recipes WHERE recipeid=%s

UPDATE users SET password=%s WHERE userid=%s