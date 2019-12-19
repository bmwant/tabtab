CREATE TABLE IF NOT EXISTS meme(
  id SERIAL PRIMARY KEY,
  active INTEGER DEFAULT 0,
  alias VARCHAR(200) NOT NULL,
  file_id VARCHAR(200) NOT NULL,
  url VARCHAR(400) NOT NULL
);


CREATE TABLE IF NOT EXISTS topic(
  id SERIAL PRIMARY KEY,
  alias VARCHAR(200) NOT NULL,
  text VARCHAR(1000) NOT NULL
);
