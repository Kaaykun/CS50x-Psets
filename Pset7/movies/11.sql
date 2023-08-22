/* In 11.sql, write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
   Your query should output a table with a single column for the title of each movie.
   You may assume that there is only one person in the database with the name Chadwick Boseman.
   Executing 11.sql results in a table with 1 column and 5 rows. */

  SELECT title
    FROM people, stars, movies, ratings
   WHERE people.id = stars.person_id
     AND movies.id = stars.movie_id
     AND ratings.movie_id = stars.movie_id
     AND name = "Chadwick Boseman"
ORDER BY rating DESC
   LIMIT 5;