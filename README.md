# SeenOnIMDb
A simple IMDb scraper that tells you what movies you've seen people in.

You'll need an IMDb account to use this script. It determines what movies/shows you have watched from your ratings list (which must be public).

Instructions:

- Run imdbscrape.py from the command line.

- It will give you 3 options: use a new account, refresh your 'watched' data stored from previous use, or use the old saved data. On first use, you'll need to use the first option and input the URL of your IMDb account (this must be passed as a string, sorry). Afterwards, you can keep using your old saved data, but bear in mind it may become outdated as you rate new things.

- Once your watching data has been gathered, it will ask for a URL to check (and this has to be a string, too). This can be an actor/actress's IMDb page or a movie/show IMDb page.
     - If you give an actor/actress, it will tell you all the movies you've seen that person in.
     - If you give a movie/show, it will go through the top 20 listed names and tell you all the movies (if any) you've seen them in.

- Keep on putting in links if you want and seeing what all you've seen those vaguely recognizeable people in.

- Type "" to exit the loop.

Enjoy! I'll be trying to improve this hopefully soon, to be nicer and faster and maybe not require the quotes.
