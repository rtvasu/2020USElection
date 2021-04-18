-- -----------------------------------------------------------------------------
--
-- 2020 Election Database
--
--
-- History: initial creation: 14 March 2021
-- 
-- GROUP MEMBERS:
-- Indraj Kang
-- Aarti Vasudevan
-- Aishwarya Srinivas



-- use project_1;

-- Our Tables
drop table if exists electionComments ;
drop table if exists VotesPerCounty ;
drop table if exists TweetsTrump ;
drop table if exists TweetsBiden ;
drop table if exists CountyStats ; 
drop table if exists PresidentialCandidate ; 
drop table if exists Party ;
drop table if exists County ;
drop table if exists States ;

	
-- ------------------------------------------------------------------------------------------------------------------------------------------- STATES
select '----------------------------------------------------------------' as '';
select 'Create States' as '';

-- create table
create table States (abbreviation varchar (5),
					name varchar(100) not null);

-- load data
-- load data infile '/var/lib/mysql-files/05-2020-Election/president_state.csv' ignore into table States 
--      fields terminated by ','
--      enclosed by '"'
--      lines terminated by '\n'
--      ignore 1 lines
--      (name,@total_votes);
	 

-- insert states	 
INSERT INTO States (abbreviation, name) VALUES
('AL', 'Alabama'),
('AK', 'Alaska'),
('AL', 'Alabama'),
('AZ', 'Arizona'),
('AR', 'Arkansas'),
('CA', 'California'),
('CO', 'Colorado'),
('CT', 'Connecticut'),
('DE', 'Delaware'),
('DC', 'District of Columbia'),
('FL', 'Florida'),
('GA', 'Georgia'),
('HI', 'Hawaii'),
('ID', 'Idaho'),
('IL', 'Illinois'),
('IN', 'Indiana'),
('IA', 'Iowa'),
('KS', 'Kansas'),
('KY', 'Kentucky'),
('LA', 'Louisiana'),
('ME', 'Maine'),
('MD', 'Maryland'),
('MA', 'Massachusetts'),
('MI', 'Michigan'),
('MN', 'Minnesota'),
('MS', 'Mississippi'),
('MO', 'Missouri'),
('MT', 'Montana'),
('NE', 'Nebraska'),
('NV', 'Nevada'),
('NH', 'New Hampshire'),
('NJ', 'New Jersey'),
('NM', 'New Mexico'),
('NY', 'New York'),
('NC', 'North Carolina'),
('ND', 'North Dakota'),
('OH', 'Ohio'),
('OK', 'Oklahoma'),
('OR', 'Oregon'),
('PA', 'Pennsylvania'),
('PR', 'Puerto Rico'),
('RI', 'Rhode Island'),
('SC', 'South Carolina'),
('SD', 'South Dakota'),
('TN', 'Tennessee'),
('TX', 'Texas'),
('UT', 'Utah'),
('VT', 'Vermont'),
('VA', 'Virginia'),
('WA', 'Washington'),
('WV', 'West Virginia'),
('WI', 'Wisconsin'),
('WY', 'Wyoming');
	
-- add incrementing primary key: stateid	
ALTER TABLE States ADD stateid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (stateid);



	 
-- ------------------------------------------------------------------------------------------------------------------------------------------ COUNTY
select '----------------------------------------------------------------' as '';
select 'Create County' as '';

-- create table
create table County (`state` varchar(125),
				   name varchar(125)
);

-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/president_county.csv' ignore into table County
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (state,name, @current_votes, @total_votes,	@percent);

-- remove the word 'County' from county names
UPDATE County 
SET 
    name = substring(name,1,LOCATE("County", name)-2)
WHERE
    LOCATE("County", name) > 0;	 
	 

-- add primary key countyid
ALTER TABLE County ADD countyid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (countyid);

-- add foreign key - stateid
ALTER TABLE County ADD stateid INT AFTER countyid;
UPDATE County c
INNER JOIN States s ON s.name = c.state
SET c.stateid = s.stateid;
ALTER TABLE County add foreign key (stateid) references States(stateid);

-- remove duplicate records
DELETE c1 FROM County c1
INNER JOIN County c2 
WHERE 
    c1.countyid < c2.countyid AND 
    c1.state = c2.state AND
	c1.name = c2.name;



-- ---------------------------------------------------------------------------------------------------------------------------------------------- PARTY 
select '----------------------------------------------------------------' as '';
select 'Create Party ' as '';

-- create temp table
create table temp_party (abbreviation varchar(20),
						 name varchar(100)
);

-- create actual table	
create table Party (abbreviation varchar(20),
					name varchar(100)
);

-- load data
INSERT INTO Party
(abbreviation, name)
VALUES('DEM', 'Democratic');
INSERT INTO Party
(abbreviation, name)
VALUES('REP', 'Republican');
INSERT INTO Party
(abbreviation, name)
VALUES('LIB', 'Libertarian');
INSERT INTO Party
(abbreviation, name)
VALUES('GRN', 'Green');
INSERT INTO Party
(abbreviation, name)
VALUES('WRI', 'Write In');
INSERT INTO Party
(abbreviation, name)
VALUES('PSL', 'Party for Socialism and Liberation');
INSERT INTO Party
(abbreviation, name)
VALUES('IND', 'Independant');
INSERT INTO Party
(abbreviation, name)
VALUES('ALI', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('CST', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('ASP', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('OTH', 'Other');
INSERT INTO Party
(abbreviation, name)
VALUES('UTY', 'United Utah');
INSERT INTO Party
(abbreviation, name)
VALUES('LLC', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('SWP', 'Socialist Workers');
INSERT INTO Party
(abbreviation, name)
VALUES('BAR', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('PRO', 'Progressive');
INSERT INTO Party
(abbreviation, name)
VALUES('NON', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('PRG', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('UNA', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('BMP', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('GOP', 'Republican');
INSERT INTO Party
(abbreviation, name)
VALUES('BFP', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('APV', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('IAP', 'Independant American');
INSERT INTO Party
(abbreviation, name)
VALUES('LLP', NULL);
INSERT INTO Party
(abbreviation, name)
VALUES('SEP', 'Socialist Equality');

-- insert unique values into correct table
INSERT INTO Party (abbreviation,name)
SELECT DISTINCT abbreviation,name FROM temp_party;

DROP TABLE temp_party ;

-- add primary key partyid
ALTER TABLE Party ADD partyid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (partyid);



-- --------------------------------------------------------------------------------------------------------------------------------- PRESIDENTCANDIDATE
select '----------------------------------------------------------------' as '';
select 'Create PresidentialCandidate ' as '';

-- create temp table
create table temp_pres_candidiate (fullname varchar(100),
						abbreviation varchar(20)
);

-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/president_county_candidate.csv' ignore into table temp_pres_candidiate
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@state, @county, fullname, abbreviation, @total_votes, @won);
	
-- create actual table	
create table PresidentialCandidate (fullname varchar(100),
									abbreviation varchar(20)
);

-- insert unique values into correct table
INSERT INTO PresidentialCandidate (fullname, abbreviation)
SELECT DISTINCT fullname, abbreviation FROM temp_pres_candidiate;

DROP TABLE temp_pres_candidiate ;

-- add primary key candidateid
ALTER TABLE PresidentialCandidate ADD candidateid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (candidateid);

-- add froeign key partyid
ALTER TABLE PresidentialCandidate ADD partyid INT AFTER abbreviation;
UPDATE PresidentialCandidate c
INNER JOIN Party p ON p.abbreviation = c.abbreviation
SET c.partyid = p.partyid;
ALTER TABLE PresidentialCandidate 
add foreign key (partyid) references Party(partyid);









-- -------------------------------------------------------------------------------------------------------------------------------- VOTESPERCOUNTY 
select '----------------------------------------------------------------' as '';
select 'Create VotesPerCounty  ' as '';
-- ------------------------------------------------------------------------------

-- create table
create table VotesPerCounty (`state` varchar(100),
					county varchar(100),
				   candidate varchar(100),
				   party varchar(20),
				   total_votes int,
				   won varchar(20)
);

-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/president_county_candidate.csv' ignore into table VotesPerCounty
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (state, county, candidate, party, total_votes, won);

-- remove the word 'County' from county names
UPDATE VotesPerCounty 
SET 
    county = substring(county,1,LOCATE("County", county)-2)
WHERE
    LOCATE("County", county) > 0;	 

-- add primary key voteid
ALTER TABLE VotesPerCounty ADD voteid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (voteid);

-- add foreign key countyid
ALTER TABLE VotesPerCounty ADD countyid INT AFTER county;
UPDATE VotesPerCounty c
INNER JOIN County p ON (p.name = c.county and p.state = c.state)
SET c.countyid = p.countyid;
ALTER TABLE VotesPerCounty 
add foreign key (countyid) references County(countyid);

-- add foreign key candidateid
ALTER TABLE VotesPerCounty ADD candidateid INT AFTER candidate;
UPDATE VotesPerCounty c
INNER JOIN PresidentialCandidate p ON p.fullname = c.candidate
SET c.candidateid = p.candidateid;
ALTER TABLE VotesPerCounty 
add foreign key (candidateid) references PresidentialCandidate(candidateid);

-- add foreign key partyid
ALTER TABLE VotesPerCounty ADD partyid INT AFTER party;
UPDATE VotesPerCounty c
INNER JOIN Party p ON p.abbreviation = c.party 
SET c.partyid = p.partyid;
ALTER TABLE VotesPerCounty 
add foreign key (partyid) references Party(partyid);






-- ------------------------------------------------------------------------------------------------------------------------------- TWEETSTRUMP 
select '----------------------------------------------------------------' as '';
select 'Create TweetsTrump  ' as '';
-- ------------------------------------------------------------------------------

-- create temp table
create table temp_TweetsTrump (created_at datetime,
						tweet varchar(140),
						likes int,
						retweets int,
						user_followers_count int,
						country  varchar(140),
						`state`  varchar(140)
);

-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/hashtag_donaldtrump.csv' ignore into table temp_TweetsTrump
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (created_at,
	 @tweet_id,
	 tweet,
	 likes,
	 retweets,
	 @source,
	 @user_id,
	 @user_name,
	 @user_screen_name,
	 @user_description,
	 @user_join_date,
	 user_followers_count,
	 @user_location,
	 @lat,
	 @long,
	 @city,
	 country,
	 @continent,
	 `state`,
	 @state_code,
	 @collected_at
);

-- create actual table
create table TweetsTrump (created_at datetime,
						tweet varchar(140),
						likes int,
						retweets int,
						user_followers_count int,
						country  varchar(140),
						`state`  varchar(140)
);

-- add only tweets from the US into actual table
INSERT INTO TweetsTrump
SELECT * FROM temp_TweetsTrump t
where t.country = 'United States of America';

DROP TABLE temp_TweetsTrump ;

-- add primary key voteid
ALTER TABLE TweetsTrump ADD voteid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (voteid);

-- add foreign key stateid
ALTER TABLE TweetsTrump ADD stateid INT AFTER `state`;
UPDATE TweetsTrump t
INNER JOIN States s ON t.`state` = s.name
SET t.stateid = s.stateid;
ALTER TABLE TweetsTrump 
add foreign key (stateid) references States(stateid);
	 


	 
	 
	 
	 
	 
	 
	 
	 
	 
-- -------------------------------------------------------------------------------------------------------------------------------------- TWEETSBIDEN
select '----------------------------------------------------------------' as '';
select 'Create TweetsTrump  ' as '';
-- ------------------------------------------------------------------------------

-- create temp table
create table temp_TweetsBiden (created_at datetime,
						tweet varchar(140),
						likes int,
						retweets int,
						user_followers_count int,
						country  varchar(140),
						`state`  varchar(140)
);

-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/hashtag_joebiden.csv' ignore into table temp_TweetsBiden
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (created_at,
	 @tweet_id,
	 tweet,
	 likes,
	 retweets,
	 @source,
	 @user_id,
	 @user_name,
	 @user_screen_name,
	 @user_description,
	 @user_join_date,
	 user_followers_count,
	 @user_location,
	 @lat,
	 @long,
	 @city,
	 country,
	 @continent,
	 `state`,
	 @state_code,
	 @collected_at
);

-- create actual table
create table TweetsBiden (created_at datetime,
						tweet varchar(140),
						likes int,
						retweets int,
						user_followers_count int,
						country  varchar(140),
						`state`  varchar(140)
);

-- add only tweets from the US into actual table
INSERT INTO TweetsBiden
SELECT * FROM temp_TweetsBiden t
where t.country = 'United States of America';

DROP TABLE temp_TweetsBiden ;

-- add primary key voteid
ALTER TABLE TweetsBiden ADD voteid INT NOT NULL AUTO_INCREMENT FIRST,
add primary key (voteid);

-- add foreign key stateid
ALTER TABLE TweetsBiden ADD stateid INT AFTER `state`;
UPDATE TweetsBiden t
INNER JOIN States s ON t.`state` = s.name
SET t.stateid = s.stateid;
ALTER TABLE TweetsBiden 
add foreign key (stateid) references States(stateid);








-- ------------------------------------------------------------------------------------------------------------------------ COUNTYSTATS
select '----------------------------------------------------------------' as '';
select 'Create CountyStats  ' as '';
-- ------------------------------------------------------------------------------

-- create table
create table CountyStats (
		stat_id	int,
	 	county varchar(100),
		`state` varchar(100),
		percentage16_Donald_Trump	double,
		percentage16_Hillary_Clinton	double,
		total_votes16	double,
		votes16_Donald_Trump	double,
		votes16_Hillary_Clinton	double,
		percentage20_Donald_Trump	double,
		percentage20_Joe_Biden	double,
		total_votes20	double,
		votes20_Donald_Trump	double,
		votes20_Joe_Biden	double,
		lat	double,
		`long`	double,
		cases	double,
		deaths	double,
		TotalPop	double,
		Men	double,
		Women	double,
		Hispanic	double,
		White	double,
		Black	double,
		Native	double,
		Asian	double,
		Pacific	double,
		VotingAgeCitizen	double,
		Income	double,
		IncomeErr	double,
		IncomePerCap	double,
		IncomePerCapErr	double,
		Poverty	double,
		ChildPoverty	double,
		Professional	double,
		Service	double,
		Office	double,
		Construction	double,
		Production	double,
		Drive	double,
		Carpool	double,
		Transit	double,
		Walk	double,
		OtherTransp	double,
		WorkAtHome	double,
		MeanCommute	double,
		Employed	double,
		PrivateWork	double,
		PublicWork	double,
		SelfEmployed	double,
		FamilyWork	double,
		Unemployment 	double
);


-- load data
load data infile '/var/lib/mysql-files/05-2020-Election/county_statistics.csv' ignore into table CountyStats
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines;
	 
	 
-- add primary key voteid
ALTER TABLE CountyStats add primary key (stat_id);


-- add foreign key countyid
ALTER TABLE CountyStats ADD countyid INT AFTER county;
UPDATE CountyStats c
inner join States s on (s.abbreviation = c.state)
INNER JOIN County p ON (p.name like concat('%',c.county,'%') and p.state = s.name)
SET c.countyid = p.countyid;
ALTER TABLE CountyStats 
add foreign key (countyid) references County(countyid);

-- delete rows that have no info abt Alaska
DELETE cs FROM CountyStats cs
inner join County c on (cs.countyid = c.countyid)
inner join States s on (s.stateid = c.stateid)
where s.name = 'Alaska'




-- -------------------------------------------------------------------------------------------------------------------------- WINSANDLOSSES 
select '----------------------------------------------------------------' as '';
select 'Create electionComments  ' as '';
-- ------------------------------------------------------------------------------

-- create table
create table electionComments (winId int NOT NULL AUTO_INCREMENT,
						 `stateid` int,
						 `countyid` int,
						  partyid int,
						  result varchar(100),
PRIMARY KEY (`winId`),
FOREIGN KEY (`stateid`) REFERENCES `States` (`stateid`),
FOREIGN KEY (`countyid`) REFERENCES `County` (`countyid`),
FOREIGN KEY (`partyid`) REFERENCES `Party` (`partyid`)
);




-- ------------------------------------------------------------------------------------------------- drop unnecessary columns from all tables
ALTER TABLE County DROP COLUMN `state`;

ALTER TABLE PresidentialCandidate DROP COLUMN `abbreviation`;

ALTER TABLE VotesPerCounty DROP COLUMN `state`;
ALTER TABLE VotesPerCounty DROP COLUMN `county`;
ALTER TABLE VotesPerCounty DROP COLUMN `candidate`;
ALTER TABLE VotesPerCounty DROP COLUMN `party`;

ALTER TABLE TweetsTrump DROP COLUMN `country`;	 
ALTER TABLE TweetsTrump DROP COLUMN `state`;	

ALTER TABLE TweetsBiden DROP COLUMN `country`;	 
ALTER TABLE TweetsBiden DROP COLUMN `state`;	

ALTER TABLE CountyStats
DROP COLUMN county,
DROP COLUMN `state`,
DROP COLUMN percentage16_Donald_Trump,
DROP COLUMN percentage16_Hillary_Clinton,
DROP COLUMN total_votes16,
DROP COLUMN votes16_Donald_Trump,
DROP COLUMN votes16_Hillary_Clinton,
DROP COLUMN percentage20_Donald_Trump,
DROP COLUMN percentage20_Joe_Biden,
DROP COLUMN total_votes20,
DROP COLUMN votes20_Donald_Trump,
DROP COLUMN votes20_Joe_Biden,
DROP COLUMN lat,
DROP COLUMN `long`,
DROP COLUMN cases,
DROP COLUMN deaths,
DROP COLUMN Pacific,
DROP COLUMN VotingAgeCitizen,
DROP COLUMN IncomeErr,
DROP COLUMN IncomePerCap,
DROP COLUMN IncomePerCapErr,
DROP COLUMN ChildPoverty,
DROP COLUMN Professional,
DROP COLUMN Service,
DROP COLUMN Office,
DROP COLUMN Construction,
DROP COLUMN Production,
DROP COLUMN Drive,
DROP COLUMN Carpool,
DROP COLUMN Transit,
DROP COLUMN Walk,
DROP COLUMN OtherTransp,
DROP COLUMN WorkAtHome,
DROP COLUMN MeanCommute,
DROP COLUMN PrivateWork,
DROP COLUMN PublicWork,
DROP COLUMN SelfEmployed,
DROP COLUMN FamilyWork;
