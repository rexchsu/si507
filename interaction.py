import sqlite3
import json
import csv
import sys
import plotly
import plotly.graph_objects as go


### Create sqlite3 database ###
# Part 1: Read data JSON into a new database called choc.db
DBNAME = 'movie.db'
IMDB_2018TOP100_JSON = 'imdb_dict.json'
OMDB_MOVIE_JSON = 'omdb_dict.json'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# Drop the tables if they already exist so they can be made again
statement = '''
    DROP TABLE IF EXISTS 'TOP100_MOVIE';
'''
cur.execute(statement)
conn.commit()

# Create the IMDB_2018_Top100_Movie table
statement = '''
    CREATE TABLE "TOP100_MOVIE" (
    	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    	"Name"	TEXT NOT NULL,
    	"Rating"	INTEGER NOT NULL,
    	"Storyline"	TEXT NOT NULL,
    	"IMDB_Id"	TEXT NOT NULL
    );
'''

cur.execute(statement)
conn.commit()

## Fill the IMDB_2018_Top100_Movie table with data from IMDB_2018TOP100_JSON ##
movies_str = open(IMDB_2018TOP100_JSON, 'r')
top100_movies = json.load(movies_str)
movies_str.close()

for movie in top100_movies:
    # print(movie)
    insertion = (None, top100_movies[movie]['name'], top100_movies[movie]['rating'], top100_movies[movie]['stroyline'], top100_movies[movie]['imdb_id'])
    statement = 'INSERT INTO TOP100_MOVIE VALUES (?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
conn.commit()



# Drop the tables if they already exist so they can be made again
statement = '''
    DROP TABLE IF EXISTS 'TOP100_MOVIE_DETAIL';
'''
cur.execute(statement)
conn.commit()

# Create the Top100_Movie_Detail table
statement = '''
    CREATE TABLE "TOP100_MOVIE_DETAIL" (
    	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    	"Title"	TEXT NOT NULL,
    	"Rating"	INTEGER NOT NULL,
    	"BoxOffice"	TEXT NOT NULL,
        "Production"	TEXT NOT NULL,
    	"Poster"	TEXT NOT NULL
    );
'''

cur.execute(statement)
conn.commit()


## Fill the Top100_Movie_Detail table with data from OMDB_MOVIE_JSON ##
omdb_movies_str = open(OMDB_MOVIE_JSON, 'r')
movies_detail = json.load(omdb_movies_str)
movies_str.close()

for a_movie in movies_detail:
    # print(a_movie)
    insertion = (None, a_movie['Title'], a_movie['imdbRating'], a_movie['BoxOffice'], a_movie['Production'], a_movie['Poster'])
    statement = 'INSERT INTO TOP100_MOVIE_DETAIL VALUES (?, ?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
conn.commit()



# ## Implement logic to process user commands
def process_command(command):
    # Connect to the database
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # If the command is 'guess'
    if command == "guess":
        statement = '''SELECT D.Title, D.Rating, D.Boxoffice, D.Production, D.Poster FROM TOP100_MOVIE_DETAIL AS D ORDER BY D.Rating ASC'''
        result = cur.execute(statement).fetchall()
        return result

    # If the command is '2018 top 100 movies'
    if command == "top100_movies":
        statement = '''SELECT T.Name, T.Rating FROM TOP100_MOVIE AS T ORDER BY T.Rating ASC'''
        # Fetch the results
        result = cur.execute(statement).fetchall()
        return result
#
#
    conn.close()
    # return result


def load_help_text():
    with open('final_project_help.txt') as f:
        return f.read()


## Implement interactive prompt.
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while True:
        response = input("Please enter command (or “help” for options): ")

        results = process_command(response)
        # If it was the 2018 top 100 movies command
        if response == 'top100_movies':
            # print(type(results))
            name_lst = []
            rating_lst = []
            for a_movie in results:
                name_lst.append(a_movie[0])
                rating_lst.append(a_movie[1])
            # Use textposition='auto' for direct text

            fig = go.Figure(data=[go.Bar(
                        x=name_lst, y=rating_lst,
                        text=rating_lst,
                        textposition='auto',
                    )])
            fig.show()

        # If it was the guess command
        elif response == 'guess':
            with open('movie_list.csv', 'w', newline='') as csvfile:
                # movie_dic = {}
                movie_lst = []
                rat_lst = []
                prod_lst = []
                poster_lst = []
                for one_movie_name in results:
                    # movie_dic["name"] = one_movie_name[0]
                    # movie_dic["rating"] = one_movie_name[3]
                    movie_lst.append(one_movie_name[0])
                    rat_lst.append(one_movie_name[1])
                    prod_lst.append(one_movie_name[3])
                    poster_lst.append(one_movie_name[4])

                fieldnames = ['Movie_Title','Production']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for name in movie_lst:
                    writer.writerow({'Movie_Title': name})
                for prod in prod_lst:
                    writer.writerow({'Production': prod})


            guess_rating_movie1 = input("OK! It's time to play a game!" + "\n" +
            "You just get a movie list with top 100 movies name with their production in 2018" + "\n" +
            "Please enter the 1st movie that you think has the 1st highest rating:")
            guess_rating_movie2 = input("Now! Please enter the 2nd movie that you think has the 2nd highest rating:")
            guess_rating_movie3 = input("Now! Please enter the 3rd movie that you think has the 3rd highest rating:")
            guess_rating_movie4 = input("Now! Please enter the 4th movie that you think has the 4th highest rating:")
            guess_rating_movie5 = input("Now! Please enter the 5th movie that you think has the 5th highest rating:")

            #reveal the movie who has 1st rating
            if guess_rating_movie1 != str(movie_lst[-1]):
                print("\n" + "Sorry,You are wrong..." + "\n" +
                "The 1st movie rating in 2018 is: " + str(movie_lst[-1]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-1]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-1]))
                print("\n")

            elif guess_rating_movie1 == str(movie_lst[-1]):
                print("\n" + "Congrats! You are correct!" + "\n" +
                "The 1st movie rating in 2018 is: " + str(movie_lst[-1]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-1]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-1]))
                print("\n")

            else:
                print("Sorry, I didn't get" + guess_rating_movie1)

            #reveal the movie who has 2nd rating
            if guess_rating_movie2 != str(movie_lst[-2]):
                print("\n" + "Sorry,You are wrong..." + "\n" +
                "The 2nd movie rating in 2018 is: " + str(movie_lst[-2]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-2]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-2]))
                print("\n")

            elif guess_rating_movie2 == str(movie_lst[-2]):
                print("\n" + "Congrats! You are correct!" + "\n" +
                "The 2nd movie rating in 2018 is: " + str(movie_lst[-2]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-2]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-2]))
                print("\n")

            else:
                print("Sorry, I didn't get" + guess_rating_movie2)

            #reveal the movie who has 3rd rating
            if guess_rating_movie3 != str(movie_lst[-3]):
                print("\n" + "Sorry,You are wrong..." + "\n" +
                "The 3rd movie rating in 2018 is: " + str(movie_lst[-3]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-3]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-3]))
                print("\n")

            elif guess_rating_movie3 == str(movie_lst[-3]):
                print("\n" + "Congrats! You are correct!" + "\n" +
                "The 3rd movie rating in 2018 is: " + str(movie_lst[-3]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-3]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-3]))
                print("\n")

            else:
                print("Sorry, I didn't get" + guess_rating_movie3)

            #reveal the movie who has 4th rating
            if guess_rating_movie4 != str(movie_lst[-4]):
                print("\n" + "Sorry,You are wrong..." + "\n" +
                "The 4th movie rating in 2018 is: " + str(movie_lst[-4]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-4]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-4]))
                print("\n")

            elif guess_rating_movie4 == str(movie_lst[-4]):
                print("\n" + "Congrats! You are correct!" + "\n" +
                "The 4th movie rating in 2018 is: " + str(movie_lst[-4]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-4]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-4]))
                print("\n")

            else:
                print("Sorry, I didn't get" + guess_rating_movie4)
            #reveal the movie who has 5th rating
            if guess_rating_movie5 != str(movie_lst[-5]):
                print("\n" + "Sorry,You are wrong..." + "\n" +
                "The 5th movie rating in 2018 is: " + str(movie_lst[-5]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-5]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-5]))
                print("\n")

            elif guess_rating_movie5 == str(movie_lst[-5]):
                print("\n" + "Congrats! You are correct!" + "\n" +
                "The 5th movie rating in 2018 is: " + str(movie_lst[-5]) + "!" + "\n" +
                "Its rating is: " + str(rat_lst[-5]) + "!" + "\n" +
                "The movie poster link is: " + str(poster_lst[-5]))
                print("\n")

            else:
                print("Sorry, I didn't get" + guess_rating_movie5)

            # histogram of all movies' ratings
            print("\n" + "This program also gives you a bar graph with movies that have box office!")
            name_lst = []
            box_office_lst = []
            for guess_movie in results:
                name_lst.append(guess_movie[0])
                if guess_movie[2] != 'N/A':
                    box_office_lst.append(guess_movie[2])

            fig = go.Figure(data=[go.Bar(
                        x=name_lst, y=box_office_lst,
                        text=box_office_lst,
                        textposition='auto',
                    )])
            fig.show()
            # end of histogram of all movies' ratings

            # piechart of all movies' box office
            title_lst = []
            box_lst = []
            final_box_lst = []
            for title in results:
                title_lst.append(title[0])
            # print(title_lst)
            for box_office in results:
                box_lst.append(box_office[2])
                # print(box_lst)
            for a_box in box_lst:
                if a_box == 'N/A':
                    final_box_lst.append(int(0))
                elif a_box != 'N/A':
                    a = a_box.strip('$')
                    b = a.replace(',','')
                    final_box_lst.append(int(b))
                            # box_lst.append(int(a_box))
            # print(final_box_lst)

            fig = go.Figure(data=[go.Pie(labels=title_lst, values=final_box_lst)])
            fig.show()
            # end of piechart of all movies' box office

        elif response.lower() == 'help':
            print(help_text)

        elif response.lower() == 'exit':
            print("Bye!")
            break

        elif response.lower() != 'exit':
            print('Command not recognized: ' + response)
            print("\n")


if __name__=="__main__":
    interactive_prompt()


# back_up plan
# results = process_command('top100_movies')
#
# def text(results):
#
#     name_lst = []
#     rating_lst = []
#     for a_movie in results:
#         name_lst.append(a_movie[0])
#         rating_lst.append(a_movie[1])
#     # Use textposition='auto' for direct text
#
#     fig = go.Figure(data=[go.Bar(
#                 x=name_lst, y=rating_lst,
#                 text=rating_lst,
#                 textposition='auto',
#             )])
#     fig.show()
#
# text(results)

# results = process_command('guess')
# def text(results):
#     name_lst = []
#     box_office_lst = []
#     for guess_movie in results:
#         name_lst.append(guess_movie[0])
#         if guess_movie[2] != 'N/A':
#             box_office_lst.append(guess_movie[2])
#
#     fig = go.Figure(data=[go.Bar(
#                 x=name_lst, y=box_office_lst,
#                 text=box_office_lst,
#                 textposition='auto',
#             )])
#     fig.show()
#
# text(results)
