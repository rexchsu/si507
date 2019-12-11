# si507

● Data sources used, including instructions for a user to access the data sources
  There are 2 data sources I used: Open Movie Database and Scraping the IMDb movie page
  When running the python file named "interaction.py", this file will get data from a database named "movie.db". 
  The database was created by another python file named "final_project.py", which cached data from OMDB and imdb database.
  
  After run the python file named "interaction.py", it will create:
  1. a SQLite3 database named "movie.db", which contains 2 tables: TOP100_MOVIE, TOP100_MOVIE_DETAIL
  2. a csv file named "movie_list.csv", which has 2 tables: Movie_Title, Production (by using command: "guess")
  3. three plotly graphs:
     3.1 The histogram graph of the box office.   (by using command: "guess")
     3.2 The pie chart of movie box office.       (by using command: "guess")
     3.2 The histogram graph of the movie rating. (by using command: "top100_movies")
     


● How to run the program:
  1.	Guess:
      a. Users will get a CSV file with the table contains 100 movie names and their production.
      b. Users need to input 5 movie names, guessing which one has the highest rating.
        (e.g., Based on the list, you can input Spiderman, Iron Lady, Iron Man, Toy Story 3, and Moonlight as 5 movies.
               You can put Moonlight at first, which imply the program that you think it has the best review.)
      c. Program will reveal the answer with:
         movie name, rating, the URL of the movie poster
      d. Open a new website page which displays a histogram graph of box office.
      e. Open a new website page which displays a pie chart of box office.

  2.	2018 Top 100 Movies:
      Open a new website page displays the histogram graph with top 100 movies ordered by ratings.

  3.	Help:
      Tell users how to play with this program.

  4.	Exit:
      End the program.
 

● Any other information needed to run the program:
  OMDB's API key


● The three major functions are:
  1. get_imdb_data: 
     Use this function to get scraping data from 100 imdb website.
  2. get_OMDB_data:
     Use this function to get OMDB movie data through API.
  3. process_command:
     Use this function to receive users' command, get data from database, and process the data in order to present
     
