#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ANDREW REIFMAN-PACKETT
# 2020.05.21 
# Set a match URL and create a query to add a team, add a match, add the players,
#   add the appearances, and add the goals.

import requests,re,subprocess,logging,time,traceback,datetime,os
import runSQL
from unidecode import unidecode
from bs4 import BeautifulSoup
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH
#matchID = "3491263"
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH

logging.basicConfig(filename="log.log",filemode='a',level=logging.INFO)

def updateName(name):
    newName= {
            "Aaron Wan Bissaka" : "Aaron Wan-Bissaka",
            "Ainsley Maitland Niles" : "Ainsley Maitland-Niles",
            "David De Gea" : "David De-Gea",
            "Edward Nketiah" : "Eddie Nketiah",
            "Pape Abou-Cisse" : "Pape Abou Cisse",
            "Pierre Emerick-Aubameyang" : "Pierre-Emerick Aubameyang",
            "Youssef El Arabi" : "Youssef El-Arabi"
    }
    name = unidecode(newName.get(name,name))
    if '\'' in name:
        name = re.sub("'", "\\'",name)
    return unidecode(newName.get(name,name))

def getSlug(name):
    newName= {
            "Ainsley Maitland-Niles" : "Maitland-Niles",
            "Pierre-Emerick Aubameyang" : "Aubameyang",
    }
    name = unidecode(newName.get(name,name))
    if '\'' in name:
        name = re.sub("'", "\\'",name)
    slug = name.replace(' ','-')
    return unidecode(newName.get(slug,slug))

def fixStadium(stadium):
    newStadium = {
            "Artemio Franchi" : "Stadio Artemio Franchi",
            "Commerzbank Arena" : "Commerzbank-Arena",
            "Hillsborough" : "Hillsborough Stadium",
            "Idraetsparken" : "Parken",
            "Knights Community Stadium" : "Gander Green Lane",
            "Johan Cruijff ArenA" : "Johan Cruyff Arena",
            "Olimpico di Roma" : "Stadio Olimpico",
            "Olympiako Stadio Athinas Spyros Louis" : "Athens Olympic Stadium",
            "Madejski" : "Madejski Stadium",
            "Maksimir" : "Stadion Maksimir",
            "Northern Commercials Stadium" : "Valley Parade",
            "Partizan Stadion" : "Partizan Stadium",
            "Stadio Georgios Karaiskakis" : "Karaiskakis Stadium",
            "Stadium mk" : "Plough Lane",
            "St Andrew\\'s Trillion Trophy Stadium" : "St. Andrew\'s Trillion Trophy Stadium",
            "St James\\' Park" : "St. James\' Park",
            "St Mary\\'s Stadium" : "St. Mary\'s Stadium",
            "Wembley Stadium (old)" : "Wembley Stadium"
            }
    stadium = newStadium.get(stadium,stadium)
    if '\'' in stadium:
        stadium = re.sub("'","\\'",stadium)
    return unidecode(stadium)

def fixTeam(team):
    newTeam = {
            "1. FC Köln" : "FC Cologne",
            "AC Sparta Praha" : "Sparta Prague",
            "AC Fiorentina" : "Fiorentina",
            "Arsenal FC" : "Arsenal",
            "Austria Vienna" : "FK Austria Wien",
            "Besiktas JK" : "Besiktas",
            "Blackpool FC" : "Blackpool",
            "Brentford FC" : "Brentford",
            "Burnley FC" : "Burnley",
            "Celtic FC" : "Celtic",
            "Chelsea FC" : "Chelsea",
            "Darlington FC (liq.)" : "Darlington FC",
            "Everton FC" : "Everton",
            "FC Barcelona" : "Barcelona",
            "FC Basel 1893" : "FC Basel",
            "FC Farnborough" : "Farnborough",
            "FC Schalke 04" : "Schalke 04",
            "FC Rouen 1899" : "FC Rouen",
            "FK Partizan Belgrade" : "Partizan Belgrade",
            "Fenerbahce SK" : "Fenerbahce",
            "Fulham FC" : "Fulham",
            "FC Internazionale" : "Internazionale",
            "HNK Hajduk Split" : "Hajduk Split",
            "Galatasaray SK" : "Galatasaray",
            "GNK Dinamo Zagreb" : "Dinamo Zagreb",
            "Grasshopper Club Zurich" : "Grasshopper",
            "Hamburger SV" : "Hamburg SV",
            "HSC Montpellier" : "Montpellier",
            "Liverpool FC" : "Liverpool",
            "Luton Town" : "Luton Town FC",
            "Middlesbrough FC" : "Middlesbrough",
            "Notts County" : "Notts County FC",
            "Olympiacos Piraeus" : "Olympiakos",
            "Olympique Lyon" : "Olympique Lyonnais",
            "Omonia Nicosia" : "AC Omonia",
            "PFK Ludogorets Razgrad" : "Ludogorets Razgrad",
            "Panathinaikos Athens" : "Panathinaikos FC",
            "PAOK Thessaloniki" : "PAOK FC",
            "Portsmouth FC" : "Portsmouth United",
            "Qarabağ Ağdam" : "FK Qarabag",
            "RC Lens" : "Lens",
            "RCD Mallorca" : "Mallorca",
            "RC Lüttich" : "RFC Liège",
            "RFC Lüttich" : "RFC Liège",
            "RSC Anderlecht" : "Anderlecht",
            "Reading FC" : "Reading",
            "Rosenborg BK" : "Rosenborg",
            "SC Braga" : "Braga",
            "SL Benfica" : "Benfica",
            "SK Slavia Prague" : "Slavia Prague",
            "SS Lazio" : "Lazio",
            "SSC Napoli" : "Napoli",
            "Stade Rennais FC" : "Stade Rennes",
            "Southampton FC" : "Southampton",
            "Sunderland AFC" : "Sunderland",
            "Twente Enschede FC" : "FC Twente",
            "Udinese Calcio" : "Udinese",
            "Valencia CF" : "Valencia",
            "Villarreal CF" : "Villarreal",
            "Vitória Guimarães SC" : "Guimaraes",
            "Vorskla Poltava" : "Vorskla",
            "Watford FC" : "Watford",
            "York City" : "York City FC"
            }
    return newTeam.get(team,team)

def convertTimestamp(time):
    time = time.split(":")[1].strip()[:-1]
    minute,ten = time.split(" ")
    minute = re.sub('px','',minute)
    ten = re.sub('px','',ten)
    minute = str(int((abs(int(minute)) / 36) + 1)) + "'"
    if int(minute[:-1]) > 9:
        ten = abs(int(ten)) + 36
        minute = minute[1:]
    ten = str(int(abs(int(ten)) / 36))
    time = ten + minute
    if int(ten) > 11:
        time = "-"
    return time


def getMonth(month):
    return {
            "Jan" : "01",
            "Feb" : "02",
            "Mar" : "03",
            "Apr" : "04",
            "May" : "05",
            "Jun" : "06",
            "Jul" : "07",
            "Aug" : "08",
            "Sep" : "09",
            "Oct" : "10",
            "Nov" : "11",
            "Dec" : "12",
            }[month]


def updateLeague(league):
    newLeagues = {
            "Barclays Premier League" : "Premier League",
            "English Carabao Cup" : "League Cup",
            "English Carling Cup" : "League Cup",
            "English Capital One Cup" : "League Cup",
            "Europa League" : "UEFA Europa League",
            "EFL Cup" : "League Cup",
            "Community Shield" : "English FA Community Shield",
            #"FA Cup" : "English FA Cup",
            "First Division (until 91/92)" : "First Division",
            #"League Cup" : "English Football League Cup",
            "UEFA Champions League Qualifying" : "UEFA Champions League",
            "UEFA-Cup" : "UEFA Cup"
            }
    league = unidecode(newLeagues.get(league,league))
    if '\'' in league:
        league = re.sub("'", "\\'",league)
    return league

def convertDate(date):
    if date.count(',') > 0:
        date = date[5:]
    try:
        date = date.split(" ")
        year = date[2]
        day = date[1].strip(',')
        month = getMonth(date[0])
    except IndexError:
        date = date[0].split("/")
        year = date[2]
        day = date[1]
        month = date[0]
    except:
        return date
    return year + '-' + month + '-'+day

def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t


def getTeams(soup):
    boxes = soup.find_all("div",{"class",re.compile("^large-6 columns")})
    teams = {}
    for i,box in enumerate(boxes):
        team = []
        try:
            #Default format for line up, aka just a table
            table = box.find("div",{"class","large-12 columns"})
            teamTable = table.find("table")
            for row in teamTable.find_all("tr")[:-1]:
                names = row.findAll("td")[1].text.strip().split(",")
                for name in names:
                    if name == ' Jr.':
                        team[-1] = team[-1] + name
                    else:
                        team.append(name.strip())
            teams[i] = (team)
        except:
            try:
                teamTable = box.find_all("div",{"class","large-7 columns"})[0]
                table = teamTable.find_all("tr")
                for row in table:
                    cols = row.find_all("a")
                    for name in cols:
                        team.append(name.text.strip())
                teams[i] = (team)
            except:
                teamTable = box.find_all("div",{"class","aufstellung-spieler-container"})
                names = []
                for row in teamTable:
                    for a in row.findAll('a',href=True):
                        name = a['href'].split('/',2)[1:2]
                        name = str(name[0].replace('-',' ')).title()
                        team.append(name.strip())
                teams[i] = (team)
    return teams[0],teams[1]

def getGoals(soup):
    team1goal = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-heim"})
    team2goal = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-gast"})
    team1goals = {}
    team2goals = {}
    if team1goal:
        for goal in team1goal:
            name = goal.findAll("a",{"class","wichtig"})[0].text
            timestamp = convertTimestamp(goal.find("span")["style"])
            if name not in team1goals:
                team1goals[name] = []
            team1goals[name].append(timestamp)
    if team2goal:
        for goal in team2goal:
            name = goal.findAll("a",{"class","wichtig"})[0].text
            timestamp = convertTimestamp(goal.find("span")["style"])
            if name not in team2goals:
                team2goals[name] = []
            team2goals[name].append(timestamp)
    return team1goals,team2goals

def getSubs(soup,team1,team2):
    team1Sub = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-heim"})
    team2Sub = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-gast"})
    team1subs = {}
    team2subs = {}
    if team1Sub:
        for sub in team1Sub:
            name = sub.findAll("a",{"class","wichtig"})[0].text
            outName = sub.findAll("a",{"class","wichtig"})[1].text
            timestamp = convertTimestamp(sub.find("span")["style"])
            try:
                team1subs[name].append(timestamp)
            except:
                team1subs[name] = timestamp
            index = team1.index(outName)
            team1[index] = outName + " " + timestamp
    if team2Sub:
        for sub in team2Sub:
            name = sub.findAll("a",{"class","wichtig"})[0].text
            outName = sub.findAll("a",{"class","wichtig"})[1].text
            timestamp = convertTimestamp(sub.find("span")["style"])
            try:
                team2subs[name].append(timestamp)
            except:
                team2subs[name] = timestamp
            index = team2.index(outName)
            team2[index] = outName + " " + timestamp
    return team1subs,team2subs,team1,team2

def getCards(soup):
    team1Card = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-heim"})
    team2Card = soup.find("div",{"class","sb-ereignisse"}).findAll("li",{"class","sb-aktion-gast"})
    team1cards = {}
    team2cards = {}
    if team1Card:
        for card in team1Card:
            name = card.findAll("a",{"class","wichtig"})[0].text
            timestamp = convertTimestamp(card.find("span")["style"])
            if "Red card" in card:
                name = "!Red " + name
            try:
                team1cards[name].append(timestamp)
            except:
                team1cards[name] = timestamp
    if team2Card:
        for card in team2Card:
            name = card.findAll("a",{"class","wichtig"})[0].text
            timestamp = convertTimestamp(card.find("span")["style"])
            if "Red card" in str(card):
                name = "!Red " + name
            try:
                team2cards[name].append(timestamp)
            except:
                team2cards[name] = timestamp
    return team1cards,team2cards

def getLineUps(matchID):
    team1subs,team1goals,team1cards,team2subs,team2goals,team2cards = ([] for i in range(6))
    try:
        # try to find line-ups
        #Is it always box 8?
        url = "https://www.transfermarkt.us/spielbericht/index/spielbericht/"+matchID
        lineWebsite = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        line_html = lineWebsite.text
        soup = BeautifulSoup(line_html,"lxml")
        for subsection in soup.findAll("div",{"class","large-12 columns"}):
            try:
                header = subsection.find("h2").text
                if header == "Line-Ups":
                    team1,team2 = getTeams(subsection)
                if header == "Goals":
                    team1goals,team2goals = getGoals(subsection)
                if header == "Substitutions":
                    team1subs,team2subs,team1,team2 = getSubs(subsection,team1,team2)
                if header == "Cards":
                    team1cards,team2cards = getCards(subsection)
            except:
                pass
    except:
        traceback.print_exc()
        print("Oh No. That Failed")
    
    try:
        team1
    except:
        return '','','','','','','',''

    return team1,team1subs,team1goals,team1cards,team2,team2subs,team2goals,team2cards



def getMatchSite(matchID):
    home = "Home"
    while True:
        try:
            url = "https://www.transfermarkt.us/spielbericht/index/spielbericht/"+matchID
            lineWebsite = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            line_html = lineWebsite.text
            soup = BeautifulSoup(line_html, "lxml")
            try:
                team1fix = soup.findAll("div",{"class","sb-team sb-heim hide-for-small"})[0].find("a",{"class","sb-vereinslink"}).text
                team2fix = soup.findAll("div",{"class","sb-team sb-gast hide-for-small"})[0].find("a",{"class","sb-vereinslink"}).text
            except:
                team1fix = soup.findAll("div",{"class","sb-team sb-heim"})[0].find("a",{"class","sb-vereinslink"}).text
                team2fix = soup.findAll("div",{"class","sb-team sb-gast"})[0].find("a",{"class","sb-vereinslink"}).text
            break
        except IndexError as e:
            time.sleep(10)

    if team1fix[-1]==' ':
        team1fix = team1fix[0:-1]
    if team2fix[-1]==' ':
        team2fix = team2fix[0:-1]    
        team2fix = fixTeam(team2fix)

    team1fix = fixTeam(team1fix)
    team2fix = fixTeam(team2fix)
    
    try: 
        #ko_date = soup.findAll("div",{"class","sb-spieldaten"})[0].findAll("a")[1].text.strip()
        ko_date = soup.findAll("div",{"class","sb-spieldaten"})[0].findAll("a")[1]['href'].rsplit('/',1)[-1]
        if len(ko_date) != 10:
            ko_date = soup.findAll("div",{"class","sb-spieldaten"})[0].findAll("a")[0]['href'].rsplit('/',1)[-1]
        if ko_date != []:
            ko_day = ko_date[:3]
            #ko_date = convertDate(ko_date)

    except:
        ko_date = soup.findAll("div",{"class","sb-spieldaten"})[0].findAll("a")[0].text.strip()
        if ko_date != []:
            ko_day = ko_date[:3]
            ko_date = convertDate(ko_date)

    comp = soup.find("div",{"class","spielername-profil"}).text.strip()

    ### SHOULD ADD HOME/AWAY LOGIC HERE
    venue = soup.findAll("div",{"class","sb-spieldaten"})[0].select("a[href*=stadion]")[0].text
    if '\'' in venue:
        venue = re.sub("'", "\\'",venue)
    team1Start,team1Sub,team1Goals,team1Cards,team2Start,team2Sub,team2Goals,team2Cards = getLineUps(matchID)
    opposition = team1fix if team2fix == "Arsenal" else team2fix
    if opposition == team1fix:
        home = "Away"
    addGameQuery(ko_date,opposition,home,comp,venue)
    if team1Start == []:
        return opposition
    addPlayersQuery(team1Start,team2Start,team1Sub,team2Sub)
    addAppearancesQuery(ko_date,team1fix,team1Start,team1Sub,team2fix,team2Start,team2Sub)
    addGoalsQuery(ko_date,team1Goals,team2Goals,team1fix,team2fix)
    addCardsQuery(ko_date,team1Cards,team2Cards)
    return opposition

def addGameQuery(date, opposition, home, comp,stadium):
    query = "INSERT INTO games (date,opposition,`home/away`,competition,stadium)\n"
    stadium = fixStadium(stadium)
    query += "VALUES\n"
    query += "(\""+date+"\",(select id from clubs where name = '"+opposition+"'),\""+home+"\",(select id from competitions where competition = '"+updateLeague(comp)+"'),(select id from stadiums where name = \""+stadium+"\"))\n"
    query += "ON DUPLICATE KEY UPDATE opposition = (select id from clubs where name ='"+opposition+"');"
    f = open("game.sql", "w")
    f.write(query)
    f.close()

def addPlayersQuery(team1,team2,team1subs,team2subs):
    query = "INSERT IGNORE INTO players (playerName,slug)\n"
    query += "VALUES\n"
    for name in team1:
        name = re.sub('\d.*','',name).rstrip()
        name = updateName(name)
        slug = getSlug(name)
        query += "(\""+name+"\",\""+slug+"\"),\n"
    for name in team1subs:
        name = re.sub('\d.*','',name).rstrip()
        ame = updateName(name)
        slug = getSlug(name)
        query += "(\""+name+"\",\""+slug+"\"),\n"
    for name in team2:
        name = re.sub('\d.*','',name).rstrip()
        name = updateName(name)
        slug = getSlug(name)
        query += "(\""+name+"\",\""+slug+"\"),\n"
    for name in team2subs:
        name = re.sub('\d.*','',name).rstrip()
        name = updateName(name)
        slug = getSlug(name)
        query += "(\""+name+"\",\""+slug+"\"),\n"
    query = ";".join(query.rsplit(",",1))
    f = open("players.sql", "w")
    f.write(query)
    f.close()

def addAppearancesQuery(date,team1Name,team1,team1sub,team2Name,team2, team2sub):
    query = "INSERT IGNORE INTO appearances (game,player,club,subIn,subOut)\n"
    query += "VALUES\n"
    sub = re.compile('\d+')
    for name in team1:
        if sub.search(name):
            subOut = re.findall('.*\s(\d.*)',name,re.IGNORECASE)[0]
            name = re.sub('(\d.*)','',name)
            name = updateName(name)
            query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team1Name+"'),\"\",\""+subOut+"\"),\n"
        else:
            name = updateName(name)
            query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team1Name+"'),\"\",\"\"),\n"
    for name in team1sub:
        subIn = team1sub[name]
        name = updateName(name)
        query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team1Name+"'),\""+subIn+"\",\"\"),\n"
    for name in team2:
        if sub.search(name):
            subOut = re.findall('.*\s(\d.*)',name,re.IGNORECASE)[0]
            name = re.sub('(\d.*)','',name)
            name = updateName(name)
            query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team2Name+"'),\"\",\""+subOut+"\"),\n"
        else:
            name = updateName(name)
            query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team2Name+"'),\"\",\"\"),\n"
    for name in team2sub:
        subIn = team2sub[name]
        name = updateName(name)
        query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team2Name+"'),\""+subIn+"\",\"\"),\n"
    query = ";".join(query.rsplit(",",1))
    f = open("appearance.sql", "w")
    f.write(query)
    f.close()

def addGoalsQuery(date,team1,team2,team1Name,team2Name):
    query = "INSERT IGNORE INTO goals (appearance,minute,club)\n"
    query += "VALUES\n"
    for name in team1:
        goal = team1[name]
        name = updateName(name)
        if not isinstance(goal,str):
            for g in goal:
                query+= "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+g+"\",(select id from clubs WHERE name=\'"+team1Name+"\')),\n"
        else:
            query+= "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+goal+"\",(select id from clubs WHERE name=\'"+team1Name+"\')),\n"
    for name in team2:
        goal = team2[name]
        name = updateName(name)
        if not isinstance(goal,str):
            for g in goal:
                query+= "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+g+"\",(select id from clubs WHERE name=\'"+team2Name+"\')),\n"
        else:
            query+= "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+goal+"\",(select id from clubs WHERE name=\'"+team2Name+"\')),\n"
    query = ";".join(query.rsplit(",",1))
    if ");" not in query:
        query = ""
    f = open("goals.sql", "w")
    f.write(query)
    f.close()

def addCardsQuery(date,team1,team2):
    query = "INSERT IGNORE INTO cards (appearance,yellow,red)\n"
    query += "VALUES\n"
    for name in team1:
        card = ""
        red = ""
        if "!Red" in name:
            red = ",\""+team1[name]+"\"),\n"
            name = re.sub('!Red\s+','',name)
        else:
            card = team1[name]
        name = updateName(name)
        query += "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+card+"\""
        query += red if red else ",\"\"),\n"
    for name in team2:
        card = ""
        red = ""
        if "!Red" in name:
            red = ",\""+team2[name]+"\"),\n"
            name = re.sub('!Red\s+','',name)
        else:
            card = team2[name]
        name = updateName(name)
        query += "((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+card+"\""
        query += red if red else ",\"\"),\n"
    query = ";".join(query.rsplit(",",1))
    if ");" not in query:
        query = ""
    f = open("cards.sql", "w")
    f.write(query)
    f.close()

def updateClubs(opposition):
    query = "INSERT INTO clubs (name)\n"
    query += "VALUES\n"
    query += ("(\""+opposition+"\");\n")
    f = open("clubs.sql", "w")
    f.write(query)
    f.close()
    subprocess.check_call("mysql -u root arsenal < clubs.sql", shell=True)


if __name__ == '__main__':
    m = open("matches.txt","r")
    #m = [matchID]
    failures = []
    queries = ['game.sql','players.sql','appearance.sql','cards.sql','goals.sql']
    for match in m:
        for query in queries:
            try:
                os.remove(query)
            except FileNotFoundError as e:
                pass
        opposition = getMatchSite(match.strip())
        rc = runSQL.main(match.strip())
