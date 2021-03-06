DELETE FROM sqlite_sequence;

DROP TABLE IF EXISTS dogs_temperaments;

DROP TABLE IF EXISTS dogs_characteristics;

DROP TABLE IF EXISTS dogs;

DROP TABLE IF EXISTS activity_levels;

DROP TABLE IF EXISTS barking_levels;

DROP TABLE IF EXISTS characteristics;

DROP TABLE IF EXISTS coat_types;

DROP TABLE IF EXISTS dog_groups;

DROP TABLE IF EXISTS sheddings;

DROP TABLE IF EXISTS sizes;

DROP TABLE IF EXISTS temperaments;

DROP TABLE IF EXISTS trainabilities;

-- CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE "activity_levels" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `barking_levels` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `characteristics` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `coat_types` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE "dog_groups" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `sheddings` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `sizes` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE "temperaments" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

CREATE TABLE `trainabilities` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `desc` TEXT NOT NULL );

insert into dog_groups (desc)
values ('sporting group'), ('hound group'), ('working group'), ('terrier group'), ('toy group'), ('non-sporting group'), ('herding group'), ('miscellaneous class'), ('foundation stock service');

insert into activity_levels (desc)
values ('needs lots of activity'), ('regular exercise'), ('energetic'), ('calm');

insert into barking_levels (desc)
values ('when necessary'), ('infrequent'), ('medium'), ('frequent'), ('likes to be vocal');

-- insert into characteristics (desc)
-- values ('smallest dog breeds'), ('medium dog breeds'), ('largest dog breeds'), ('smartest dogs'), ('hypoallergenic dogs'), ('best family dogs'), ('best guard dogs'), ('best dog breeds for children'), ('best dogs for apartments dwellers'), ('hairless dog breeds');
insert into characteristics (desc)
values ('smallest dog breeds'), ('medium dog breeds'), ('largest dog breeds'), ('smartest dogs'), ('hypoallergenic dogs'), ('best family dogs'), ('best guard dogs'), ('best dogs for kids'), ('best dogs for apartments dwellers'), ('hairless dog breeds');

insert into coat_types (desc)
values ('hairless'), ('short'), ('medium'), ('long'), ('smooth'), ('wire');

insert into sheddings (desc)
values ('infrequent'), ('seasonal'), ('frequent'), ('occasional'), ('regularly');

insert into sizes (desc)
values ('xsmall'), ('small'), ('medium'), ('large'), ('xlarge');

insert into trainabilities (desc)
values ('may be stubborn'), ('agreeable'), ('eager to please'), ('independent'), ('easy training');

CREATE TABLE "dogs" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL, `desc` TEXT, `height_min` NUMERIC, `height_max` NUMERIC, `weight_min` NUMERIC, `weight_max` NUMERIC, `life_expectancy_min` INTEGER, `life_expectancy_max` INTEGER, `image` TEXT, `dog_group` INTEGER, `activity_level` INTEGER, `barking_level` INTEGER, `coat_type` INTEGER, `shedding` INTEGER, `size` INTEGER, `trainability` INTEGER, `popularity` INTEGER, `url` TEXT, FOREIGN KEY(`trainability`) REFERENCES `trainabilities`(`id`), FOREIGN KEY(`activity_level`) REFERENCES `activity_levels`(`id`), FOREIGN KEY(`shedding`) REFERENCES `sheddings`(`id`), FOREIGN KEY(`barking_level`) REFERENCES `barking_levels`(`id`), FOREIGN KEY(`dog_group`) REFERENCES `dog_groups`(`id`), FOREIGN KEY(`coat_type`) REFERENCES `coat_types`(`id`), FOREIGN KEY(`size`) REFERENCES `sizes`(`id`) );

CREATE TABLE `dogs_temperaments` ( `dog_id` INTEGER NOT NULL, `temperament_id` INTEGER NOT NULL, PRIMARY KEY(`dog_id`,`temperament_id`) );

CREATE TABLE `dogs_characteristics` ( `dog_id` INTEGER NOT NULL, `characteristic_id` INTEGER NOT NULL, PRIMARY KEY(`dog_id`,`characteristic_id`) );


-- Post processing

-- UPDATE `dogs` SET weight_min = 0 where weight_min > 99999;

-- UPDATE `dogs` SET height_min = 0 where height_min > 99999;

-- UPDATE `dogs` SET life_expectancy_min = 0 where life_expectancy_min > 99999;
