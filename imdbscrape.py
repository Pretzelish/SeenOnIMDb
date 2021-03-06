import urllib2
import string
import re
import pickle
import itertools
import os.path

MAXACTORS = 20

# actorsFilms returns a list of tuples of (movie/show IMDb ID, title, year(s))
def actorsFilms(nmid):
    acthtml = urllib2.urlopen("http://www.imdb.com/name/nm"+nmid).read()
    startidx = string.find(acthtml, "<div id=\"filmo-head-act")
    endidx = string.find(acthtml, "<div id=\"filmo-head", startidx+10)
    if (endidx == -1):
        endidx = string.find(acthtml, "<h2>Related Videos</h2>", startidx+10)
    filmography = acthtml[startidx:endidx]
    films = re.finditer(r"&nbsp;(.+)\n</span>\n<b><a href=\"/title/tt(\d+)/[^>]+>([^<]+)</a></b>", filmography, re.MULTILINE)
    seenlist = []
    filmlist = []
    for f in films:
        # f.group(1) : year(s) of actor's involvement in show/movie
        # f.group(2) : show/movie IMDb ID number
        # f.group(3) : title
        moviedict[f.group(2)] = f.group(3)
        filmlist.append((f.group(2), f.group(1)))
        if f.group(2) in tlist:
            seenlist.append((f.group(2), f.group(3), f.group(1)))
    actordict[nmid] = filmlist
    return seenlist

# usersFilms returns a list of IMDb IDs that have been rated by the given user
def usersFilms(uid):
    firstpage = urllib2.urlopen("http://www.imdb.com/user/ur" + uid + "/ratings?start=1&view=compact")
    pagehtml = firstpage.read()
    page = re.search(r"Page 1 of (\d+)", pagehtml)
    pg = 1
    if (page != None):
        pg = int(page.group(1))
    for i in range(1, pg):
        pagehtml += urllib2.urlopen("http://www.imdb.com/user/ur" + uid + "/ratings?start=" + str((250*i) + 1) + "&view=compact").read()
    titles = re.finditer(r"<td class=\"title\"><a href=\"/title/tt(\d+)/\">([^<]+)</a></td>\n<td class=\"year\">(\d+)</td>", pagehtml, re.MULTILINE)
    idlist = []
    for t in titles:
        # t.group(1) : movie/show IMDb ID number
        # t.group(2) : movie/show title
        # t.group(3) : (beginning) year of movie/show
        idlist.append(t.group(1))
        moviedict[t.group(1)] = re.sub("&#x27;", "'", t.group(2))
    if os.path.exists("imdbstore.dat"):
        os.remove("imdbstore.dat")
    pickle.dump((urid, idlist), open("imdbstore.dat",'a'))
    return idlist


if os.path.exists("actordata.dat"):
    actordict = pickle.load(open("actordata.dat",'r+'))
else:
    actordict = {}

if os.path.exists("moviedata.dat"):
    moviedict = pickle.load(open("moviedata.dat",'r+'))
else:
    moviedict = {}

save = input("New(0), Refresh (1), or Saved (2): ")
while True:
    if save == 0:
        user = input("Enter your profile URL on IMDb: ")
        urid = re.search(r"/ur(\d+)", user).group(1)
        tlist = usersFilms(urid)
        break
    elif save == 1 and os.path.exists("imdbstore.dat"):
        (urid, trash) = pickle.load(open("imdbstore.dat"))
        tlist = usersFilms(urid)
        break
    elif save == 2 and os.path.exists("imdbstore.dat"):
        (urid, tlist) = pickle.load(open("imdbstore.dat"))
        break
    else:
        save = input("Please enter 0 for new, 1 for refresh or 2 for saved: ")



while True:
    urlinput = input("Enter movie or actor/actress URL (type \"\" to exit): ")
    if urlinput == "":
        break
    urlid = re.search("(nm|tt)(\d+)",urlinput)
    # if found, urlid's groups will be as follows:
    # urlid.group(1) : 'nm' or 'tt' denoting whether the ID is for an actor or a title
    # urlid.group(2) : ID number
    if urlid == None:
        print("Invalid input.")
        continue
    if urlid.group(1) == "nm": # case for actor URL given
        seen = actorsFilms(urlid.group(2))
        print(str(len(seen)) + " titles seen with this actor:")
        for (a, b, c) in seen:
            # prints title and year(s) of actor's involvement in show/movie
            print(b + " (" + c + ")")
    else: # case for movie/show URL given
        # need to open movie's full credits list to access cast list
        urlhtml = urllib2.urlopen("http://www.imdb.com/title/" + urlid.group(0) + "/fullcredits").read()
        startidx = string.find(urlhtml, "<table class=\"cast_list\">")
        endidx = string.find(urlhtml, "<div class=", startidx+10)
        castlist = urlhtml[startidx:endidx]
        actors = re.finditer(r"/name/nm(\d+)/[^>]+>[^>]+>([^<]+)</span>", castlist)
        moviename = re.search(r"<h3 itemprop=\"name\">\n[^>]+>([^<]+)</a>", urlhtml, re.MULTILINE)
        showid = re.search(r"<h4 itemprop=\"name\">\n<a href=\"/title/tt(\d+)", urlhtml, re.MULTILINE)
        print("You have seen the following actors/actresses in " + moviename.group(1) + ":")
        for a in itertools.islice(actors, MAXACTORS):
            # a.group(1) : actor's IMDb ID
            # a.group(2) : actor's name
            seen = []
            for (x,y,z) in actorsFilms(a.group(1)):
                # only adds to seen if it is not the movie/show searched for
                # also filters out shows if the search is for an episode of the show
                if (not x == urlid.group(2)) and (showid == None or not x == showid.group(1)):
                    seen.append((y,z))
            if len(seen) > 0:
                print(a.group(2) + " (" + str(len(seen)) + " titles)")
                for (n, d) in seen:
                    # prints title and year(s) of actor's involvement in show/movie
                    print("  " + n + " (" + d + ")")
    pickle.dump(actordict, open("actordata.dat",'w'))
    pickle.dump(moviedict, open("moviedata.dat",'w'))