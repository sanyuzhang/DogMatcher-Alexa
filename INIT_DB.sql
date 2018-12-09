CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE "activity_levels" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `barking_levels` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `characteristics` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `coat_types` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE "groups" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `sheddings` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `sizes` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE "temperaments" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `trainabilities` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

INSERT INTO groups (desc)
VALUES ('Sporting Group'), ('Hound Group'), ('Working Group'), ('Terrier Group'), ('Toy Group'), ('Non-Sporting Group'), ('Herding Group'), ('Miscellaneous Class'), ('Foundation Stock Service');

INSERT INTO activity_levels (desc)
VALUES ('Needs Lots Of Activity'), ('Regular Exercise'), ('Energetic'), ('Calm');

INSERT INTO characteristics (desc)
VALUES ('Smallest Dog Breeds'), ('Medium Dog Breeds'), ('Largest Dog Breeds'), ('Smartest Dogs'), ('Hypoallergenic Dogs'), ('Best Family Dogs'), ('Best Guard Dogs'), ('Best Dog Breeds For Children'), ('Best Dogs For Apartments Dwellers'), ('Hairless Dog Breeds');

INSERT INTO coat_types (desc)
VALUES ('Hairless'), ('Short'), ('Medium'), ('Long'), ('Smooth'), ('Wire');

INSERT INTO sheddings (desc)
VALUES ('Infrequent'), ('Seasonal'), ('Frequent'), ('Occasional'), ('Regularly');

INSERT INTO sizes (desc)
VALUES ('XSmall'), ('Small'), ('Medium'), ('Large'), ('XLarge');

INSERT INTO trainabilities (desc)
VALUES ('May Be Stubborn'), ('Agreeable'), ('Eager To Please'), ('Independent'), ('Easy Training');

CREATE TABLE "dogs" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL, `desc` TEXT, `height_min` NUMERIC, `height_max` NUMERIC, `weight_min` NUMERIC, `weight_max` NUMERIC, `life_expectancy_min` INTEGER, `life_expectancy_max` INTEGER, `image` TEXT, `group` INTEGER, `activity_level` INTEGER, `barking_level` INTEGER, `characteristics` INTEGER, `coat_type` INTEGER, `shedding` INTEGER, `size` INTEGER, `trainability` INTEGER, `popularity` INTEGER, `url` TEXT, FOREIGN KEY(`trainability`) REFERENCES `trainabilities`(`id`), FOREIGN KEY(`activity_level`) REFERENCES `characteristics`(`id`), FOREIGN KEY(`characteristics`) REFERENCES `characteristics`(`id`), FOREIGN KEY(`shedding`) REFERENCES `sheddings`(`id`), FOREIGN KEY(`barking_level`) REFERENCES `barking_levels`(`id`), FOREIGN KEY(`group`) REFERENCES `groups`(`id`), FOREIGN KEY(`coat_type`) REFERENCES `coat_types`(`id`), FOREIGN KEY(`size`) REFERENCES `sizes`(`id`) );

CREATE TABLE `dogs_temperaments` ( `dog_id` INTEGER NOT NULL, `temperament_id` INTEGER NOT NULL, PRIMARY KEY(`dog_id`,`temperament_id`) );