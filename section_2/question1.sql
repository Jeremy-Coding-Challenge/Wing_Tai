/* tested on https://www.db-fiddle.com/ using MySQL v8.0 */


/* Schema SQL */
CREATE TABLE users (
  user_id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  gender varchar(10) NOT NULL,
  PRIMARY KEY (user_id)
  );
 

CREATE TABLE actions (
  action_id int NOT NULL AUTO_INCREMENT,
  action_type varchar(255) NOT NULL,
  PRIMARY KEY (action_id)
  );
  
  
 CREATE TABLE user_action (
   user_action_id int NOT NULL AUTO_INCREMENT,
   user_id INT NOT NULL,
   action_id INT NOT NULL,
   created_at DATETIME  NOT NULL,
   PRIMARY KEY (user_action_id),
   FOREIGN KEY (user_id) REFERENCES users(user_id),
   FOREIGN KEY (action_id) REFERENCES actions(action_id)
  );
  
  
  
INSERT INTO users (name, gender) VALUES ("John", "Male");
INSERT INTO users (name, gender) VALUES ("Jane", "Female");
INSERT INTO users (name, gender) VALUES ("Peter", "Male");

INSERT INTO actions (action_type) VALUES ("Login");
INSERT INTO actions (action_type) VALUES ("Logout");
INSERT INTO actions (action_type) VALUES ("Add to Cart");
INSERT INTO actions (action_type) VALUES ("Checkout");

INSERT INTO user_action (user_id, action_id, created_at) VALUES (1, 1, '2019-01-01 00:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (2, 3, '2019-01-01 02:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (1, 3, '2019-01-01 03:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (2, 2, '2019-01-01 04:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (2, 1, '2019-01-01 05:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (1, 4, '2019-01-01 06:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (1, 2, '2019-01-01 07:00:00');
INSERT INTO user_action (user_id, action_id, created_at) VALUES (2, 2, '2019-01-01 08:00:00');



/* QUERY SQL */
SELECT name, gender, last_action, last_action_time, second_last_action, second_last_action_time
FROM (
    users 
    LEFT JOIN (
        SELECT 
            b.user_id,
            MAX(CASE WHEN b.rnum = 1 THEN b.action_type END) "last_action",
            MAX(CASE WHEN b.rnum = 1 THEN b.created_at END) "last_action_time",
            MAX(CASE WHEN b.rnum = 2 THEN b.action_type END) "second_last_action",
            MAX(CASE WHEN b.rnum = 2 THEN b.created_at END) "second_last_action_time"
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY a.user_id ORDER BY a.created_at DESC) AS rnum
            FROM (
                SELECT ua.user_id, a.action_type, ua.created_at
                FROM user_action ua INNER JOIN actions a 
                ON ua.action_id = a.action_id
                ) a
        ) b
        GROUP BY b.user_id
    ) last_actions ON users.user_id = last_actions.user_id 
);