/* In 13.sql, write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
   Your query should output a table with a single column for the name of each person.
   There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
   Kevin Bacon himself should not be included in the resulting list.
   Executing 13.sql results in a table with 1 column and 185 rows.*/

SELECT name
  FROM people
  JOIN stars ON people.id = stars.person_id
 WHERE movie_id IN
   (
   SELECT movie_id
     FROM stars
     JOIN people ON stars.person_id = people.id
    WHERE name = "Kevin Bacon"
      AND birth = 1958
   )
   AND name != "Kevin Bacon"
 GROUP BY name, person_id;