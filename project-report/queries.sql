SELECT userid 
FROM users 
WHERE username=(%s);

INSERT INTO users (username, password) VALUES (%s, %s)

SELECT password FROM users WHERE username=(%s)

UPDATE users SET logged_token=%s WHERE username=%s

DELETE FROM users where username=%s

SELECT userid, username FROM users WHERE logged_token=(%s)

SELECT * FROM recipes WHERE %s && ingredients

SELECT userid FROM users WHERE userid=%s

SELECT recipeid FROM recipes WHERE recipeid=%s

INSERT INTO comments (userid, recipeid, comment) VALUES (%s, %s, %s)

SELECT userid, comment FROM comments WHERE recipeid=%s

SELECT username FROM users WHERE userid=%s

(SELECT recipes FROM categories WHERE category=%s) 
UNION 
(SELECT recipes FROM categories WHERE category=%s)

SELECT * FROM recipes WHERE recipeid=%s

SELECT * FROM category_count

SELECT * FROM users WHERE userid=%s

UPDATE users SET password=%s WHERE userid=%s