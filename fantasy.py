#Adithya Somasundaram fantasy football app
#Version 2.0

# Import necessary librarys for webscraping and display
import urllib2
import re
from bs4 import BeautifulSoup
from Tkinter import *

# webscraping function
def click():
    text1 = name.get() # player name from GUI
    text2 = week.get() # week number from GUI
    result = "" # final display

    flag = 0 # flag for if player is not found

    startIndex = 0 # start index for ESPN

    quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + text2 + '&seasonId=2018&startIndex=' + str(startIndex) # ESPN webpage
    rank = 1 # player rank counter
    page = urllib2.urlopen(quote_page) # open page
    soup = BeautifulSoup(page, 'lxml')
    thelink = 0 # changes once player is found
    test_box = soup.findAll('a', leagueid='0') # begin searchinng

    while(1):
        for test in test_box: # check each player
            if test.find(text=re.compile(text1)): # does name match
                thelink = test # found correct player
                break
            rank+=1 # increment ranking
        if thelink==0: # have not found player
            startIndex += 40 # next page
            if startIndex > 1000: # out of pages
                result += "Player not found: " + text1
                flag = 1 # player not found flag
                break
            else:
                quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + text2 + '&seasonId=2018&startIndex=' + str(startIndex) # next ESPN page
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
    
    if flag == 0: # player found before
        offset = 1 # first page
        quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(text2) # NFL webpage
        
        rank = 1 # player ranking

        page = urllib2.urlopen(quote_page) # open page
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0
        test_box = soup.findAll('a', onclick= 'return false') # begin searching
        while(1):
            for test in test_box: # check each player name
                if test.find(text=re.compile(text1)): # found correct player?
                    thelink = test # set thelink to that of player
                    break
                rank+=1 # increment rank
            if thelink == 0: # end of page
                offset += 25 # flip to next page
                if offset > 1000: # out of players
                    result+= "Player not found: " + text1
                    break
                quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(text2) # next webpage
                page = urllib2.urlopen(quote_page) # open next page
                soup = BeautifulSoup(page, 'lxml')
                test_box = soup.findAll('a', onclick= 'return false') # begin searching
            else:
                # construct player ID
                player_id = ""
                i = 0
                while(i < len(thelink.attrs['class'][3])):
                    if (i < 6 or i > 11):
                        player_id += thelink.attrs['class'][3][i]
                    i+= 1

                p = soup.find('tr', attrs={'class':player_id}) # area where points are found
                points = p.find('span', attrs={'class':'playerWeekProjectedPts'}) # find points
                # add results
                if hasattr(points, 'text'):
                    result+= "NFL: " + points.text + " Rank: " + str(int(rank)) + "\n"
                else:
                    result+= "NFL: not found" + " Rank: " + str(int(rank)) + "\n"
                break

        array = text1.split() # split name into first name and last name
        quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/playersearch?search='+ array[0] +'+' + array[1] + '&stat1=S_PW_' + str(text2) # Yahoo webpage
        page = urllib2.urlopen(quote_page) # open webpage
        soup = BeautifulSoup(page, 'lxml')
        points = soup.find('td', attrs={'style':'width: 30px;'}) # find points
        rank_zone = soup.find('td', attrs={'class':'Alt Ta-end'}) # find area where rank is stored
        rank = rank_zone.find('div') # find rank
        result+= "Yahoo: " + points.text + " Rank: " + rank.text # add results

    output.delete(0.0, END) # clear output
    output.insert(END, result) # display new output

# new window and properties
window = Tk() 
window.title("Fantasy App")
window.geometry("500x300")

Label (window, text="Fantasy Football Application", fg="black", font="none 12") .grid(row=0, column=1, sticky=W) # title
Label (window, text="Week:", fg="black", font="none 12") .grid(row=1, column=0, sticky=W) # week text box
week = Entry(window, width=2) # input 1
week.grid(row = 1, column = 1, sticky=W)

Label (window, text="Enter the player's name:", fg="black", font="none 12") .grid(row=2, column=0, sticky=W) # name text box
name = Entry(window, width=15) # input 2
name.grid(row = 2, column = 1, sticky=W)

Button(window, text="GO", width=2,  command = click) .grid(row=3, column=0, sticky=W) # GO button, runs function

output = Text(window, width=20, height=4, wrap=WORD) # output box
output.grid(row=4, column=0, sticky=W)
window.mainloop() # run