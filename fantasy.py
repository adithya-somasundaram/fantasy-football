import urllib2
import re
from bs4 import BeautifulSoup
from Tkinter import *

def click():
    text1 = name.get()
    text2 = week.get()
    result = ""

    flag = 0
    startIndex = 0
    quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + text2 + '&seasonId=2018&startIndex=' + str(startIndex)
    rank = 1
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'lxml')
    thelink = 0
    test_box = soup.findAll('a', leagueid='0')

    while(1):
        for test in test_box:
            if test.find(text=re.compile(text1)):
                thelink = test
                break
            rank+=1
        if thelink==0:
            startIndex += 40
            if startIndex > 1000:
                result += "Player not found: " + text1
                flag = 1
                break
            else:
                quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + text2 + '&seasonId=2018&startIndex=' + str(startIndex)
                page = urllib2.urlopen(quote_page)
                soup = BeautifulSoup(page, 'lxml')
                thelink = 0
                test_box = soup.findAll('a', leagueid='0')
        else:
            x = "plyr" + thelink.attrs['playerid']
            point_box = soup.find('tr', id=x)
            opponent = point_box.find('div')
            points = point_box.find('td', attrs={'class':'playertableStat appliedPoints sortedCell'})
            result += "Opponent: " + opponent.text + "\n"
            result += "ESPN: " + points.text + " Rank: " + str(rank) + "\n"
            break
    
    if flag == 0:
        offset = 1
        quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(text2)
        
        rank = 1

        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0
        test_box = soup.findAll('a', onclick= 'return false')
        while(1):
            for test in test_box:
                if test.find(text=re.compile(text1)):
                    thelink = test
                    break
                rank+=1
            if thelink == 0:
                offset += 25
                if offset > 1000:
                    result+= "Player not found: " + text1
                    break
                quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(text2)
                page = urllib2.urlopen(quote_page)
                soup = BeautifulSoup(page, 'lxml')
                thelink = 0
                test_box = soup.findAll('a', onclick= 'return false')
            else:
                player_id = ""
                i = 0
                while(i < len(thelink.attrs['class'][3])):
                    if (i < 6 or i > 11):
                        player_id += thelink.attrs['class'][3][i]
                    i+= 1

                p = soup.find('tr', attrs={'class':player_id})
                points = p.find('span', attrs={'class':'playerWeekProjectedPts'})
                if hasattr(points, 'text'):
                    result+= "NFL: " + points.text + " Rank: " + str(int(rank)) + "\n"
                else:
                    result+= "NFL: not found" + " Rank: " + str(int(rank)) + "\n"
                break

        array = text1.split()
        quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/playersearch?search='+ array[0] +'+' + array[1] + '&stat1=S_PW_' + str(text2)
        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'lxml')
        points = soup.find('td', attrs={'style':'width: 30px;'})
        rank_zone = soup.find('td', attrs={'class':'Alt Ta-end'})
        rank = rank_zone.find('div')
        result+= "Yahoo: " + points.text + " Rank: " + rank.text

    output.delete(0.0, END)
    output.insert(END, result)

window = Tk()
window.title("Hello")
window.geometry("500x300")
Label (window, text="Fantasy Football Application", fg="black", font="none 12") .grid(row=0, column=1, sticky=W)
Label (window, text="Week:", fg="black", font="none 12") .grid(row=1, column=0, sticky=W)
week = Entry(window, width=2)
week.grid(row = 1, column = 1, sticky=W)
Label (window, text="Enter the player's name:", fg="black", font="none 12") .grid(row=2, column=0, sticky=W)
name = Entry(window, width=15)
name.grid(row = 2, column = 1, sticky=W)
Button(window, text="GO", width=2,  command = click) .grid(row=3, column=0, sticky=W)

output = Text(window, width=20, height=4, wrap=WORD)
output.grid(row=4, column=0, sticky=W)
window.mainloop()