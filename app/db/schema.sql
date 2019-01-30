DROP TABLE IF EXISTS replys;
DROP TABLE IF EXISTS comments;

DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS blogs;

DROP TABLE IF EXISTS options;

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS options (
  option_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  option_name VARCHAR(255) NOT NULL,
  option_values SMALLINT NOT NULL
)character set = utf8;

CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_email VARCHAR(40) NOT NULL,
  user_nickname VARCHAR(32) NOT NULL,
  user_telephonenumber INTEGER UNSIGNED,
  user_password VARCHAR(128) NOT NULL,
  user_exp INT UNSIGNED DEFAULT 0,
  user_permission TINYINT UNSIGNED DEFAULT 0,
  user_photo VARCHAR(128)
)character set = utf8;

CREATE TABLE IF NOT EXISTS users_info(
  user_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_ip VARCHAR(20) NOT NULL,
  user_birthday DATE,
  user_age TINYINT UNSIGNED,
  FOREIGN KEY (user_id) references users(user_id) ON DELETE CASCADE
)character set = utf8;


CREATE TABLE IF NOT EXISTS topics(
  topic_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  topic_title VARCHAR(64) NOT NULL,
  topic_text TEXT NOT NULL,
  topic_createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  topic_updatetime TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  topic_type INTEGER UNSIGNED,
  topic_view INTEGER UNSIGNED DEFAULT 0,
  user_id INTEGER UNSIGNED,
  topic_reply INTEGER UNSIGNED DEFAULT 0,
  topic_lastreply INTEGER UNSIGNED DEFAULT 0,
  FOREIGN KEY (user_id) references users(user_id)
)character set = utf8;


CREATE TABLE IF NOT EXISTS replys(
  reply_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  reply_text TEXT NOT NULL,
  reply_createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reply_updatetime TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  user_id INTEGER UNSIGNED NOT NULL,
  topic_id INTEGER UNSIGNED NOT NULL,
  reply_floor INTEGER UNSIGNED NOT NULL,
  FOREIGN KEY (user_id) references users(user_id),
  FOREIGN KEY (topic_id) references topics(topic_id)
)character set = utf8;


CREATE TABLE IF NOT EXISTS blogs(
  blog_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  blog_title TEXT NOT NULL,
  blog_createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  blog_updatetime TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  blog_view INTEGER UNSIGNED DEFAULT 0,
  blog_comment INTEGER UNSIGNED DEFAULT 0,
  user_id INTEGER UNSIGNED NOT NULL,
  FOREIGN KEY (user_id) references users(user_id)
)character set = utf8;

CREATE TABLE IF NOT EXISTS comments(
  comment_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  comment_title TEXT NOT NULL,
  comment_createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  blog_id INTEGER UNSIGNED NOT NULL,
  user_id INTEGER UNSIGNED NOT NULL,
  FOREIGN KEY (blog_id) references blogs(blog_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) references users(user_id)
)character set = utf8;

