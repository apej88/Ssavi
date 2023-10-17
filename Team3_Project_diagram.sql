CREATE SCHEMA ssavi_db;

use ssavi_db;

CREATE TABLE `Albums` (
  `album_id` varchar(50) PRIMARY KEY NOT NULL,
  `album_name` varchar(150),
  `album_artist` varchar(50),
  `album_genre` varchar(50),
  `album_image` varchar(200),
  `album_release_date` date
);

CREATE TABLE `Tracks` (
  `track_id` varchar(50) PRIMARY KEY NOT NULL,
  `track_name` varchar(150),
  `album_id` varchar(50) NOT NULL,
  `album_name` varchar(150)
);

CREATE TABLE `Liked_Album` (
  `LA_id` integer PRIMARY KEY NOT NULL,
  `id` bigint NOT NULL,
  `album_id` varchar(50) NOT NULL
);

CREATE TABLE `Play_list` (
  `playlist_id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
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

ALTER TABLE `Tracks` ADD FOREIGN KEY (`album_id`) REFERENCES `Albums` (`album_id`);

ALTER TABLE `Liked_Album` ADD FOREIGN KEY (`id`) REFERENCES `users_app_user` (`id`);

ALTER TABLE `Liked_Album` ADD FOREIGN KEY (`album_id`) REFERENCES `Albums` (`album_id`);

ALTER TABLE `Play_list` ADD FOREIGN KEY (`track_id`) REFERENCES `Tracks` (`track_id`);

ALTER TABLE `Play_list` ADD FOREIGN KEY (`username`) REFERENCES `users_app_user` (`username`);

ALTER TABLE `audio_features` ADD FOREIGN KEY (`track_id`) REFERENCES `Tracks` (`track_id`);
