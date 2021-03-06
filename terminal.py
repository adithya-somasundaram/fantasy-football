import urllib2
import re
from bs4 import BeautifulSoup

result = ""

name = raw_input("Name: ")
week = raw_input("Week: ")
split = name.split()
quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/playersearch?search='+ split[0] +'+' + split[1] + '&stat1=S_PW_' + str(week)
page = urllib2.urlopen(quote_page) # open webpage
soup = BeautifulSoup(page, 'lxml')

a = soup.find('div', attrs={'id':'players-table'})
if a.text == "No players found.":
    result+= "RIP"
else:
    b = a.find('span', attrs={'class':'Fz-xxs'})
    c = a.find('span', attrs={'class':'ysf-game-status'})
    if c.text == " Bye":
        result+= "Player on bye week"
    else:
        pos  = b.text[len(b.text) - 2] + b.text[len(b.text) - 1]

        categoryID = 0
        if pos == "RB":
            categoryID = 2
        elif pos == "WR":
            categoryID = 4
        elif pos == "TE":
            categoryID = 6

        index = 0
        quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + str(week) + '&seasonId=2018&slotCategoryId='+ str(categoryID) +'&startIndex=' + str(index) # ESPN webpage
        rank = 1 # player rank counter
        page = urllib2.urlopen(quote_page) # open page
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0 # changes once player is found
        test_box = soup.findAll('a', leagueid='0') # begin searchinng

        while(1):
            for test in test_box: # check each player
                if test.find(text=re.compile(name)): # does name match
                    thelink = test # found correct player
                    break
                if len(test.text) > 0:
                    rank+=1 # increment ranking
            if thelink==0: # have not found player
                startIndex += 40 # next page
                quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + str(week) + '&seasonId=2018&slotCategoryId='+ str(categoryID) +'&startIndex=' + str(index) # ESPN webpage
                page = urllib2.urlopen(quote_page) # open page
                soup = BeautifulSoup(page, 'lxml')
                test_box = soup.findAll('a', leagueid='0') # begin searching
            else: # have correct player
                x = "plyr" + thelink.attrs['playerid'] # building ESPN player ID
                point_box = soup.find('tr', id=x) # find area where points and opponent are stored
                opponent = point_box.find('div') # find opponent
                points = point_box.find('td', attrs={'class':'playertableStat appliedPoints sortedCell'}) # find points
                result += "Opponent: " + opponent.text + "\n" # add results
                result += "ESPN: " + points.text + " Rank: " + str(rank) + "\n"
                break

        index = 0
        quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/players?status=ALL&pos=' + pos + '&cut_type=9&stat1=S_PW_'+ str(week)+ '&myteam=0&sort=PTS&sdir=1&count=' + str(index)
        rank = -2
        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0 # changes once player is found
        test_box = soup.findAll('tr') # begin searching

        while(1):
            for test in test_box: # check each player
                if test.find(text=re.compile(name)): # does name match
                    thelink = test # found correct player
                    break
                rank+=1 # increment ranking
            if thelink == 0:
                index += 25
                rank  = index - 2
                quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/players?status=ALL&pos=' + pos + '&cut_type=9&stat1=S_PW_6&myteam=0&sort=PTS&sdir=1&count=' + str(index)
                page = urllib2.urlopen(quote_page)
                soup = BeautifulSoup(page, 'lxml')
                test_box = soup.findAll('tr') # begin searching
            else:
                points = thelink.find('td', attrs={'style':'width: 30px;'})
                recs = points.find('td')
                result+= "Yahoo: PPR: " + points.text + " Rank: " + str(rank) + "\n"
                break
        
        if pos == "QB":
            categoryID = 1
        elif pos == "RB":
            categoryID = 2
        elif pos == "WR":
            categoryID = 3
        elif pos == "TE":
            categoryID = 4

        index = 1 # first page
        quote_page = 'http://fantasy.nfl.com/research/projections?position='+ str(categoryID) +'&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(week) + '&offset=' + str(index)
        rank = -1 # player ranking

        page = urllib2.urlopen(quote_page) # open page
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0
        test_box = soup.findAll('tr') # begin searching
        while(1):
            for test in test_box: # check each player name
                if test.find(text=re.compile(name)): # found correct player?
                    thelink = test # set thelink to that of player
                    break
                rank+=1 # increment rank
            if thelink == 0: # end of page
                index += 25 # flip to next page
                rank = index
                quote_page = 'http://fantasy.nfl.com/research/projections?position='+ str(categoryID) +'&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(week) + '&offset=' + str(index)
                page = urllib2.urlopen(quote_page) # open next page
                soup = BeautifulSoup(page, 'lxml')
                test_box = soup.findAll('tr') # begin searching
            else:
                points = thelink.find('td', attrs={'class':'stat projected numeric sorted last'}) # find points
                result += "NFL: " + points.text + " Rank: " + str(rank)
                break
        
print result