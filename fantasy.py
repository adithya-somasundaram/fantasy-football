import urllib2
import re
from bs4 import BeautifulSoup

print "Fantasy Projection Collection App (Enter 'q', 'quit', or 'esc' at any time to quit)"
week = raw_input("Week: ")
while(1):
    if(week == "quit" or week == "q" or week == "esc"):
        exit()
    elif(not week.isdigit()):
        week = raw_input("Week: ")
    elif(int(week) < 1 or int(week) > 17):
        week = raw_input("Week: ")
    else:
        break

while(1):
    name = raw_input("Player: ")
    if(name == "quit" or name == "q" or name == "esc"):
        exit()

    flag = 0

    startIndex = 0
    quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + week + '&seasonId=2018&startIndex=' + str(startIndex)

    rank = 1

    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'lxml')
    thelink = 0
    test_box = soup.findAll('a', leagueid='0')
    while(1):
        for test in test_box:
            if test.find(text=re.compile(name)):
                thelink = test
                break
            rank+=1
        if thelink==0:
            startIndex += 40
            if startIndex > 1000:
                print "Player not found: " + name
                flag = 1
                break
            else:
                quote_page = 'http://games.espn.com/ffl/tools/projections?&scoringPeriodId=' + week + '&seasonId=2018&startIndex=' + str(startIndex)
                page = urllib2.urlopen(quote_page)
                soup = BeautifulSoup(page, 'lxml')
                thelink = 0
                test_box = soup.findAll('a', leagueid='0')
        else:
            x = "plyr" + thelink.attrs['playerid']
            point_box = soup.find('tr', id=x)
            opponent = point_box.find('div')
            points = point_box.find('td', attrs={'class':'playertableStat appliedPoints sortedCell'})
            print "Opponent: " + opponent.text
            print "ESPN: " + points.text + " Rank: " + str(rank)
            break

    if flag == 0:
        offset = 1
        quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(week)
        
        rank = 1

        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'lxml')
        thelink = 0
        test_box = soup.findAll('a', onclick= 'return false')
        while(1):
            for test in test_box:
                if test.find(text=re.compile(name)):
                    thelink = test
                    break
                rank+=1
            if thelink == 0:
                offset += 25
                if offset > 1000:
                    print "Player not found: " + name
                    break
                quote_page = 'http://fantasy.nfl.com/research/projections?offset='+ str(offset)+'&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek=' + str(week)
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
                    print "NFL: " + points.text + " Rank: " + str(int(rank))
                else:
                    print "NFL: not found" + " Rank: " + str(int(rank))
                break
        
        array = name.split()
        quote_page = 'https://football.fantasysports.yahoo.com/f1/1204137/playersearch?search='+ array[0] +'+' + array[1] + '&stat1=S_PW_' + str(week)
        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'lxml')
        points = soup.find('td', attrs={'style':'width: 30px;'})
        rank_zone = soup.find('td', attrs={'class':'Alt Ta-end'})
        rank = rank_zone.find('div')
        print "Yahoo: " + points.text + " Rank: " + rank.text