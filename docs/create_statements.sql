CREATE TABLE user (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	role VARCHAR NOT NULL,
	password VARCHAR NOT NULL,
	registered_dt DATETIME,
	PRIMARY KEY (id)
);


CREATE TABLE "RankingList" (
	id INTEGER NOT NULL,
	name VARCHAR,
	genders TEXT,
	age_cap_hi INTEGER,
	age_cap_lo INTEGER,
	PRIMARY KEY (id)
);


CREATE TABLE "Player" (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	gender VARCHAR NOT NULL,
	dateofbirth DATETIME NOT NULL,
	placeofbirth VARCHAR NOT NULL,
	registered_dt DATETIME,
	created_by INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(created_by) REFERENCES user (id)
);


CREATE TABLE "Tournament" (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	date DATETIME NOT NULL,
	venue VARCHAR NOT NULL,
	ranking_list_id INTEGER NOT NULL,
	is_published BOOLEAN,
	is_completed BOOLEAN,
	PRIMARY KEY (id),
	FOREIGN KEY(ranking_list_id) REFERENCES "RankingList" (id),
	CHECK (is_published IN (0, 1)),
	CHECK (is_completed IN (0, 1))
);


CREATE TABLE "Ranking" (
	id INTEGER NOT NULL,
	player_id INTEGER,
	list_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(player_id) REFERENCES "Player" (id),
	FOREIGN KEY(list_id) REFERENCES "RankingList" (id)
);


CREATE TABLE "TournamentPlayer" (
	id INTEGER NOT NULL,
	tournament_id INTEGER,
	player_id INTEGER,
	position INTEGER DEFAULT '-1',
	PRIMARY KEY (id),
	FOREIGN KEY(tournament_id) REFERENCES "Tournament" (id)
);


CREATE TABLE "TournamentPrize" (
	id INTEGER NOT NULL,
	tournament_id INTEGER,
	position INTEGER,
	prize_money FLOAT,
	ranking_points INTEGER,
	player_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(tournament_id) REFERENCES "Tournament" (id),
	FOREIGN KEY(player_id) REFERENCES "Player" (id)
);


CREATE TABLE "RankingRecord" (
	id INTEGER NOT NULL,
	ranking_id INTEGER,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	score INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(ranking_id) REFERENCES "Ranking" (id)
);


CREATE TABLE "Match" (
	id INTEGER NOT NULL,
	tournament_id INTEGER,
	player1_id INTEGER,
	player2_id INTEGER,
	winner INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(tournament_id) REFERENCES "Tournament" (id),
	FOREIGN KEY(player1_id) REFERENCES "TournamentPlayer" (id),
	FOREIGN KEY(player2_id) REFERENCES "TournamentPlayer" (id),
	FOREIGN KEY(winner) REFERENCES "TournamentPlayer" (id)
);


CREATE TABLE "TournamentMatch" (
	id INTEGER NOT NULL,
	tournament_id INTEGER,
	match_id INTEGER,
	prize_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(tournament_id) REFERENCES "Tournament" (id),
	FOREIGN KEY(match_id) REFERENCES "Match" (id),
	FOREIGN KEY(prize_id) REFERENCES "TournamentPrize" (id)
);