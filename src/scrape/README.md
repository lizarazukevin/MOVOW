Data scraper for TMDB which works by traversing the database using the ID values 
assigned for each movie on the website

ID values are *int* type

Currently obtains the following information about a movie:

	- Title
	- Release Date
	- Genres
	- Runtime
	- Cast members and corresponding character(s)
	- Crew members and corresponding role(s)

------------------------------------------------------------------
To run scraaaaaaaaaaape.py:

python3 .\scraaaaaaaaaaape.py [*starting ID*] [*ending ID*]

Example: python3 .\scraaaaaaaaaaape.py 0 10

