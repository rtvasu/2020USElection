-- -----------------------------------------------------------------------------
--
-- 2020 Election Database
--
--
-- History: initial creation: 14 April 2021
-- 
-- GROUP MEMBERS:
-- Indraj Kang
-- Aarti Vasudevan
-- Aishwarya Srinivas



-- Note: THESE ARE EXAMPLES OF QUERIES WE USED IN PROJECT
-- In our program, each query is placed in a seperate function called by the main program.
-- '%s' appearing in the where clauses is replaced with the user's input


-- Example variables
SET @state_name := 'Delaware';
SET @county_name := 'Kent';
SET @party := 'DEM';
	
-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Check if state exists' as '';

SELECT * FROM States WHERE name = @state_name;



-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Check if county exists' as '';

SELECT * FROM County WHERE name = @county_name;



-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Check if party exists exists' as '';

SELECT * FROM Party WHERE name = @party or abbreviation = @party;




-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get list of counties under a state' as '';

SELECT c.name as countyName 
FROM County c

inner join States s on (c.stateid = s.stateid)
WHERE s.name = @state_name;





-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get total votes by state' as '';

SELECT  s.name as state ,
		sum(total_votes) as total_votes_2020
FROM VotesPerCounty v

inner join County c on (v.countyid = c.countyid)
inner join States s on (c.stateid = s.stateid)

group by s.name 
having s.name = @state_name
order by s.name asc;






-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get total votes by county' as '';

SELECT  s.name as state, 
		c.name as county ,
		sum(total_votes) as total_votes_2020
FROM VotesPerCounty v

inner join County c on (v.countyid = c.countyid)
inner join States s on (c.stateid = s.stateid)

group by c.name, s.name
having s.name = @state_name and c.name = @county_name
order by c.name asc;






-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Demographics of a state' as '';

select ss.name as 'States' ,
		ROUND(sum(pop_per_county),2) as 'population',
		ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
		ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
		ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
		ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
		ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
		ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
		ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
		ROUND(avg(income),2) as 'average_income'
from (
		 SELECT  c.name as county, 
				 c.countyid as countyid,
				 TotalPop as pop_per_county,
				 (cs.Men) as demographicMen,
				 (cs.Women) as demographicWomen,
				 (cs.White*TotalPop/100) as demographicWhite,
				 (cs.Black*TotalPop/100) as demographicBlack,
				 (cs.Hispanic*TotalPop/100) as demographicHispanic,
				 (cs.Asian*TotalPop/100) as demographicAsian,
				 (cs.Native*TotalPop/100) as demographicNative,
				 Income as income
		 FROM CountyStats cs
		 inner join County c on (cs.countyid = c.countyid)
) as Stats

inner join County co on (co.countyid = Stats.countyid)
inner join States ss on (ss.stateid = co.stateid)

group by ss.stateid
having ss.name = @state_name and ss.name != 'alaska'
order by ss.stateid asc;








-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Demographics of a county' as '';

select ss.name as 'States', 
		co.name as 'County', 
		ROUND(sum(pop_per_county),2) as 'population',
		ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
		ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
		ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
		ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
		ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
		ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
		ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
		ROUND(sum(income),2) as 'average_income'
from (
		 SELECT  c.name as county, 
				 c.countyid as countyid,
				 TotalPop as pop_per_county,
				 (cs.Men) as demographicMen,
				 (cs.Women) as demographicWomen,
				 (cs.White*TotalPop/100) as demographicWhite,
				 (cs.Black*TotalPop/100) as demographicBlack,
				 (cs.Hispanic*TotalPop/100) as demographicHispanic,
				 (cs.Asian*TotalPop/100) as demographicAsian,
				 (cs.Native*TotalPop/100) as demographicNative,
				 Income as income
		 FROM CountyStats cs
		 inner join County c on (cs.countyid = c.countyid)
) as Stats

inner join County co on (co.countyid = Stats.countyid)
inner join States ss on (ss.stateid = co.stateid)
group by ss.stateid, co.countyid
having ss.name = @state_name and co.name = @county_name  and ss.name != 'alaska'
order by ss.stateid asc;




-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get #TweetsBiden tweets' as '';

SELECT s.name, created_at, tweet, likes, retweets 
FROM TweetsBiden t
inner join States s on (t.stateid = s.stateid)
WHERE s.name = @state_name
ORDER BY t.likes DESC
limit 5;






-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get #TweetsTrump tweets' as '';

SELECT s.name, created_at, tweet, likes, retweets 
FROM TweetsTrump t
inner join States s on (t.stateid = s.stateid)
WHERE s.name = @state_name
ORDER BY t.likes DESC
limit 5;









-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get voting results for a state' as '';

SELECT  s.name as state, 
		p.name as party,
		sum(total_votes) as total_votes_2020,
		p.abbreviation as party
FROM VotesPerCounty v

inner join County c on (v.countyid = c.countyid)
inner join States s on (c.stateid = s.stateid)
inner join Party p on (p.partyid = v.partyid)

where won = 'True'
group by v.partyid, s.stateid
having s.name = @state_name
order by s.stateid asc limit 1;






-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get voting results for all states' as '';

with topVoted as (
	SELECT  s.name as state, s.stateid,
			p.name as party,
			sum(total_votes) as total_votes_2020
			FROM VotesPerCounty v

			inner join County c on (v.countyid = c.countyid)
			inner join States s on (c.stateid = s.stateid)
			inner join Party p on (p.partyid = v.partyid)
			where won = 'True'
			group by v.partyid, s.stateid
			order by s.stateid, sum(total_votes))
select state, party, total_votes_2020 from topVoted 
where total_votes_2020 in(
	select max(total_votes_2020) 
	from topVoted
	inner join States s on (s.stateid = topVoted.stateid)
	group by  s.stateid);
	
	
	
	
	
	
-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Get voting results for a county' as '';	
	
SELECT  s.name as state, 
		c.name as county, 
		p.name as party ,
		total_votes as total_votes_2020,
		p.abbreviation as party
FROM VotesPerCounty v

inner join County c on (v.countyid = c.countyid)
inner join States s on (c.stateid = s.stateid)
inner join Party p on (p.partyid = v.partyid)

where s.name = @state_name and c.name = @county_name and v.won = 'True'
order by c.countyid asc;








-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Inset comment for county and state' as '';

INSERT INTO electionComments (stateid, countyid, partyid, result) 
VALUES (9, 1, 1, 'Example comment for a state');





-- ------------------------------------------------------------------------------------------------------------------------------------------- 
select '----------------------------------------------------------------' as '';
select 'Prepare dataset of demographics + votinng results for the data mining exercise' as '';

select 
	ROUND(sum(pop_per_county),2) as 'population',
	ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
	ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
	ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
	ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
	ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
	ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
	ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
	ROUND(sum(income),2) as 'average_income',
	ROUND((sum(demographicPoverty)/sum(pop_per_county))*100,2) as 'poverty',
	ROUND((sum(demographicEmployed)/sum(pop_per_county))*100,2) as 'employed',
	ROUND((sum(demographicUnemployment)/sum(pop_per_county))*100,2) as 'unemployed',
	p.partyid as 'winning_party'
from (
		 SELECT  c.name as county, 
				 c.countyid as countyid,
				 TotalPop as pop_per_county,
				 (cs.Men) as demographicMen,
				 (cs.Women) as demographicWomen,
				 (cs.White*TotalPop/100) as demographicWhite,
				 (cs.Black*TotalPop/100) as demographicBlack,
				 (cs.Hispanic*TotalPop/100) as demographicHispanic,
				 (cs.Asian*TotalPop/100) as demographicAsian,
				 (cs.Native*TotalPop/100) as demographicNative,
				 Income as income,
				 (cs.Poverty*TotalPop/100) as demographicPoverty,
				 Employed as demographicEmployed,
				 (cs.Unemployment*TotalPop/100) as demographicUnemployment
		 FROM CountyStats cs
		 inner join County c on (cs.countyid = c.countyid)
) as Stats

inner join County co on (co.countyid = Stats.countyid)
inner join States ss on (ss.stateid = co.stateid)
inner join VotesPerCounty vpc on (vpc.countyid = Stats.countyid)
inner join Party p on (vpc.partyid = p.partyid)

group by ss.stateid, co.countyid, vpc.won, p.partyid 
having vpc.won  = 'True' and p.partyid = 1 or p.partyid = 2
order by ss.stateid asc;