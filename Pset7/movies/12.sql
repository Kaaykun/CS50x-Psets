/* In 12.sql, write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
   Your query should output a table with a single column for the title of each movie.
   You may assume that there is only one person in the database with the name Johnny Depp.
   You may assume that there is only one person in the database with the name Helena Bonham Carter.
   Executing 12.sql results in a table with 1 column and 6 rows. */

SELECT title
  FROM people, stars, movies
 WHERE people.id = stars.person_id
   AND movies.id = stars.movie_id
   AND name = "Johnny Depp"

INTERSECT

SELECT title
  FROM people, stars, movies
 WHERE people.id = stars.person_id
   AND movies.id = stars.movie_id
   AND name = "Helena Bonham Carter";