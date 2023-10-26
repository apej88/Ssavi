CREATE SCHEMA ssavi_db;

use ssavi_db;

CREATE TABLE `Albums` (
  `album_id` varchar(50) PRIMARY KEY NOT NULL,
  `album_name` varchar(150),
  `album_artist` varchar(50),
  `album_genre` varchar(50),
  `album_image` varchar(150),
  `album_release_date` date
);

CREATE TABLE `Tracks` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `track_name` varchar(150),
  `track_preview` varchar(150),
  `album_id` varchar(50) NOT NULL
);

CREATE TABLE `Liked_Album` (
  `LA_no` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id` bigint NOT NULL,
  `album_id` varchar(50) NOT NULL
);

CREATE TABLE `Play_list` (
  `playlist_no` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id` bigint NOT NULL,
  `track_id` varchar(50) NOT NULL
);

CREATE TABLE `audio_features` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `kwd_search` (
  `search_no` bigint NOT NULL AUTO_INCREMENT,
  `id` bigint NOT NULL,
  `album_kw` varchar(100),
  `track_kw` varchar(100),
  `genre_kw` varchar(100),
  `artist_kw` varchar(100),
  PRIMARY KEY (`search_no`, `id`)
);

CREATE TABLE `Latin` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `KPOP` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Jazz` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `RnB` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Rock` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Hiphop` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Electro` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Indiepop` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `alternative` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

CREATE TABLE `Jpop` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `acousticness` float,
  `danceability` float,
  `energy` float,
  `loudness` float,
  `speechiness` float,
  `tempo` float,
  `valence` float
);

ALTER TABLE `Tracks` ADD FOREIGN KEY (`album_id`) REFERENCES `Albums` (`album_id`);

ALTER TABLE `Liked_Album` ADD FOREIGN KEY (`id`) REFERENCES `users_app_user` (`id`);

ALTER TABLE `Liked_Album` ADD FOREIGN KEY (`album_id`) REFERENCES `Albums` (`album_id`);

ALTER TABLE `Play_list` ADD FOREIGN KEY (`track_id`) REFERENCES `Tracks` (`track_id`);

ALTER TABLE `Play_list` ADD FOREIGN KEY (`id`) REFERENCES `users_app_user` (`id`);

ALTER TABLE `kwd_search` ADD FOREIGN KEY (`id`) REFERENCES `users_app_user` (`id`);

ALTER TABLE `audio_features` ADD FOREIGN KEY (`track_id`) REFERENCES `Tracks` (`track_id`);

-- Liked_Track 생성 구문

CREATE TABLE `Liked_Track` (
	`LT_no` int primary key not null auto_increment,
	`track_id` varchar(50) NOT NULL,
    `id` bigint
);

ALTER TABLE `Liked_Track` ADD FOREIGN KEY (`track_id`) REFERENCES `Tracks` (`track_id`);
ALTER TABLE `Liked_Track` ADD FOREIGN KEY (`id`) REFERENCES `users_app_user` (`id`);