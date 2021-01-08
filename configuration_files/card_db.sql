CREATE TABLE Player (
	Player_id SERIAL PRIMARY KEY,
	Username VARCHAR(50) NOT NULL UNIQUE,
	User_password VARCHAR(255) NOT NULL,
	Score INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE Room (
	Room_id SERIAL PRIMARY KEY,
	Host_id	INTEGER NOT NULL,
	Guest_id INTEGER DEFAULT NULL,
	Finished BOOLEAN NOT NULL DEFAULT '0',
	Field_size INTEGER NOT NULL DEFAULT 16,
	Time_limit INTEGER NOT NULL DEFAULT 60,
	JSON_name VARCHAR(255) NOT NULL UNIQUE,
	Game_result VARCHAR(4) DEFAULT 'DRAW',
	Host_score INTEGER NOT NULL DEFAULT 0,
	Guest_score INTEGER NOT NULL DEFAULT 0,
	FOREIGN KEY(Host_id) REFERENCES Player(Player_id),
	FOREIGN KEY(Guest_id) REFERENCES Player(Player_id),
	CHECK(Time_limit > 0),
	CHECK(Field_size > 0),
	CHECK(Game_result IN('Win', 'Lost', 'Draw', 'win', 'lost', 'draw', 'WIN', 'LOST', 'DRAW'))
);
