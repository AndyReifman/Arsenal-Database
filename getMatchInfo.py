#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ANDREW REIFMAN-PACKETT
# 2020.05.21 
# Set a match URL and create a query to add a team, add a match, add the players,
#   add the appearances, and add the goals.

import requests,re
import runSQL
from unidecode import unidecode
from bs4 import BeautifulSoup
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH
matchID = "541641";
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH

def updateName(name):
    newName= {
            "Edward Nketiah" : "Eddie Nketiah",
            "Pape Abou-Cisse" : "Pape Abou Cisse",
            "Pierre Emerick-Aubameyang" : "Pierre-Emerick Aubameyang",
            "Youssef El Arabi" : "Youssef El-Arabi"
    }
    return newName.get(name,name)


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def getLineUps(matchID):
    try:
        # try to find line-ups
        lineAddress = "http://www.espnfc.us/lineups?gameId=" + matchID
        lineWebsite = requests.get(lineAddress, timeout=15)
        line_html = lineWebsite.text
        split = line_html.split('<div class="sub-module soccer">') # [0]:nonsense [1]:team1 [2]:team2
        
        if len(split) > 1:
            team1StartBlock = split[1].split('Substitutes')[0]
            if len(split[1].split('Substitutes')) > 1:
                team1SubBlock = split[1].split('Substitutes')[1]
            else:
                team1SubBlock = ''
            team2StartBlock = split[2].split('Substitutes')[0]
            if len(split[2].split('Substitutes')) > 1:
                team2SubBlock = split[2].split('Substitutes')[1]
            else:
                team2SubBlock = ''
            
            team1Start = []
            team2Start = []    
            team1Sub = []
            team2Sub = []
            
            t1StartInfo = re.findall('"accordion-item" data-id="(.*?)</div>', team1StartBlock, re.DOTALL)
            t1SubInfo = re.findall('"accordion-item" data-id="(.*?)</div>', team1SubBlock, re.DOTALL)
            t2StartInfo = re.findall('"accordion-item" data-id="(.*?)</div>', team2StartBlock, re.DOTALL)
            t2SubInfo = re.findall('"accordion-item" data-id="(.*?)</div>', team2SubBlock, re.DOTALL)

            for playerInfo in t1StartInfo:
                playerInfo = playerInfo.replace('\t','').replace('\n','')
                playerNum = playerInfo[0:6]
                if '%' not in playerNum:
                    playertext = ''
                    if 'icon-soccer-substitution-before' in playerInfo:
                        playertext += '!sub '
                    if 'icon-yellowcard' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        cards = soup.findAll("span",{"class","icon-yellowcard"})
                        playertext += '!yellow '
                        for card in cards:
                            playertext += card.text + ' '
                    if 'icon-soccer-goal' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        goals = soup.findAll("span",{"class","icon-soccer-goal-before"})
                        playertext += '!goal '
                        for goal in goals:
                            playertext += goal.text + ' '
                    if 'icon-redcard' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        reds = soup.findAll("span",{"class","icon-redcard"})
                        playertext += '!red '
                        for red in reds:
                            playertext += red.text + ' '
                    #playertext += re.findall('<span class="name">(?!<)(.*?)[<|&]', playerInfo, re.DOTALL)[0]
                    playertext += re.findall('<span class="name">.*href=".*/(.*?)"\sdata', playerInfo, re.DOTALL)[0]
                    playertext = unidecode(playertext).replace("-"," ", 1).title()
                    team1Start.append(playertext)
            for playerInfo in t1SubInfo:
                playerInfo = playerInfo.replace('\t','').replace('\n','')
                playerNum = playerInfo[0:6]
                if '%' not in playerNum:
                    playertext = ''
                    if 'icon-yellowcard' in playerInfo:
                        playertext += '!yellow '
                    if 'icon-soccer-goal' in playerInfo:
                        playertext += '!goal '
                    #playertext += re.findall('<span class="name">(?!<)(.*?)[<|&]', playerInfo, re.DOTALL)[0]
                    playertext += re.findall('<span class="name">.*href=".*/(.*?)"\sdata', playerInfo, re.DOTALL)[0]
                    playertext = unidecode(playertext).replace("-"," ", 1).title()
                    team1Sub.append(playertext)
            for playerInfo in t2StartInfo:
                playerInfo = playerInfo.replace('\t','').replace('\n','')
                playerNum = playerInfo[0:6]
                if '%' not in playerNum:
                    playertext = ''
                    if 'icon-soccer-substitution-before' in playerInfo:
                        playertext += '!sub '
                    if 'icon-yellowcard' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        cards = soup.findAll("span",{"class","icon-yellowcard"})
                        playertext += '!yellow '
                        for card in cards:
                            playertext += card.text + ' '
                    if 'icon-soccer-goal' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        goals = soup.findAll("span",{"class","icon-soccer-goal-before"})
                        playertext += '!goal '
                        for goal in goals:
                            playertext += goal.text + ' '
                    if 'icon-redcard' in playerInfo:
                        soup = BeautifulSoup(playerInfo, 'lxml')
                        reds = soup.findAll("span",{"class","icon-redcard"})
                        playertext += '!red '
                        for red in reds:
                            playertext += red.text + ' '
                    #playertext += re.findall('<span class="name">(?!<)(.*?)[<|&]', playerInfo, re.DOTALL)[0]
                    playertext += re.findall('<span class="name">.*href=".*/(.*?)"\sdata', playerInfo, re.DOTALL)[0]
                    playertext = unidecode(playertext).replace("-"," ", 1).title()
                    team2Start.append(playertext)                
            for playerInfo in t2SubInfo:
                playerInfo = playerInfo.replace('\t','').replace('\n','')
                playerNum = playerInfo[0:6]
                if '%' not in playerNum:
                    playertext = ''
                    if 'icon-yellowcard' in playerInfo:
                        playertext += '!yellow '
                    if 'icon-soccer-goal' in playerInfo:
                        playertext += '!goal '
                    #playertext += re.findall('<span class="name">(?!<)(.*?)[<|&]', playerInfo, re.DOTALL)[0]
                    playertext += re.findall('<span class="name">.*href=".*/(.*?)"\sdata', playerInfo, re.DOTALL)[0]
                    playertext = unidecode(playertext).replace("-"," ", 1).title()
                    team2Sub.append(playertext)
            # if no players found:
            if team1Start == []:
                team1Start = ["*Not available*"]
            if team1Sub == []:
                team1Sub = ["*Not available*"]
            if team2Start == []:
                team2Start = ["*Not available*"]
            if team2Sub == []:
                team2Sub = ["*Not available*"]
            return team1Start,team1Sub,team2Start,team2Sub
        
        else:
            team1Start = ["*Not available*"]
            team1Sub = ["*Not available*"]
            team2Start = ["*Not available*"]
            team2Sub = ["*Not available*"]
            return team1Start,team1Sub,team2Start,team2Sub
    except IndexError:
        logger.warning("[INDEX ERROR:]")
        team1Start = ["*Not available*"]
        team1Sub = ["*Not available*"]
        team2Start = ["*Not available*"]
        team2Sub = ["*Not available*"]
        return team1Start,team1Sub,team2Start,team2Sub

def getMatchSite(matchID):
    home = "Home"
    url = "https://www.espn.com/soccer/match?gameId=" + matchID
    lineWebsite = requests.get(url, timeout=15)
    line_html = lineWebsite.text
    team1fix = re.findall('<span class="long-name">(.*?)<', line_html, re.DOTALL)[0]
    team2fix = re.findall('<span class="long-name">(.*?)<', line_html, re.DOTALL)[1]

    if team1fix[-1]==' ':
        team1fix = team1fix[0:-1]
    if team2fix[-1]==' ':
        team2fix = team2fix[0:-1]    
    
    ko_date = re.findall('<span data-date="(.*?)T', line_html, re.DOTALL)
    if ko_date != []:
        ko_date = ko_date[0]
        ko_day = ko_date[8:]

    compfull = re.findall('<div class="game-details header">(.*?)<', line_html, re.DOTALL)
    if compfull != []:
        comp = re.sub('20.*? ','',compfull[0]).strip(' \n\t\r')
        if comp.find(',') != -1:
            comp = comp[0:comp.index(',')]
    else:
        comp = ''

    ### SHOULD ADD HOME/AWAY LOGIC HERE
    venue = re.findall('<div>VENUE: (.*?)<', line_html, re.DOTALL)
    if venue != []:
        venue = venue[0]
    team1Start,team1Sub,team2Start,team2Sub = getLineUps(matchID)
    opposition = team1fix if team2fix == "Arsenal" else team2fix
    if opposition == team1fix:
        home = "Away"
    addGameQuery(ko_date, opposition,home,comp)
    addPlayersQuery(team1Start,team2Start)
    addAppearancesQuery(ko_date,team1fix,team1Start,team2fix,team2Start)
    addGoalsQuery(ko_date,team1Start,team2Start)
    addCardsQuery(ko_date,team1Start,team2Start)

def addGameQuery(date, opposition, home, comp):
    query = "INSERT INTO games (date,opposition,`home/away`,competition)\n"
    query += "VALUES\n"
    query += "(\""+date+"\",(select id from clubs where name = '"+opposition+"'),\""+home+"\",(select id from competitions where competition = '"+comp+"'));\n"
    f = open("game.sql", "w")
    f.write(query)
    f.close()

def addPlayersQuery(team1,team2):
    query = "INSERT IGNORE INTO players (playerName)\n"
    query += "VALUES\n"
    for name in team1:
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        query += "(\""+name+"\"),\n"
    for name in team2[:-1]:
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        query += "(\""+name+"\"),\n"
    name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',team2[-1])
    name = updateName(name)
    query += "(\""+name+"\");\n"
    f = open("players.sql", "w")
    f.write(query)
    f.close()

def addAppearancesQuery(date,team1Name,team1,team2Name,team2):
    query = "INSERT INTO appearances (game,player,club,sub)\n"
    query += "VALUES\n"
    for name in team1:
        sub = "0"
        if "!Sub" in name:
            sub = "1"
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team1Name+"'),"+sub+"),\n"
    for name in team2[:-1]:
        sub = "0"
        if "!Sub" in name:
            sub = "1"
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team2Name+"'),"+sub+"),\n"
    sub = "0"
    if "!Sub" in name:
        sub = "1"
    name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',team2[-1])
    name = updateName(name)
    query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(select id from clubs where name = '"+team2Name+"'),"+sub+");\n"
    f = open("appearance.sql", "w")
    f.write(query)
    f.close()

def addGoalsQuery(date,team1,team2):
    query = "INSERT INTO goals (appearance,minute)\n"
    query += "VALUES\n"
    for name in team1:
        goals = re.findall('!Goal((?:\s\d+\'(?:\+\d+\')*)*)',name, re.IGNORECASE)
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        for goal in goals:
            goal = goal.strip()
            goal = goal.split(' ')
            for g in goal:
                query+="((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+g+"\"),\n"
    for name in team2:
        goals = re.findall('!Goal((?:\s\d+\'(?:\+\d+\')*)*)',name, re.IGNORECASE)
        name = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
        name = updateName(name)
        for goal in goals:
            goal = goal.strip()
            goal = goal.split(' ')
            for g in goal:
                query+="((select id from appearances where player = (SELECT id from players where playerName = '"+name+"') and game = (select id from games where date='"+date+"')),\""+g+"\"),\n"
    query = ";".join(query.rsplit(",",1))
    f = open("goals.sql", "w")
    f.write(query)
    f.close()

def addCardsQuery(date,team1,team2):
    query = "INSERT INTO cards (appearance,yellow,red)\n"
    query += "VALUES\n"
    hquery = ""
    for name in team1:
        c = 0
        if "!Yellow" in name:
            card = re.findall('!Yellow((?:\s\d+\'(?:\+\d+\')*)*)',name,re.IGNORECASE)[0].strip()
            temp = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
            temp = updateName(temp)
            hquery += "((select id from appearances where player = (SELECT id from players where playerName = '"+temp+"') and game = (select id from games where date='"+date+"')),\""+card+"\""
            c = 1
        if "!Red" in name:
            card = re.findall('!Red((?:\s\d+\'(?:\+\d+\')*)*)',name,re.IGNORECASE)[0].strip()
            if c == 1:
                hquery += ",\""+card+"\"),\n"
                c == 0
            else:
                temp = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
                temp = updateName(temp)
                hquery += "((select id from appearances where player = (SELECT id from players where playerName = '"+temp+"') and game = (select id from games where date='"+date+"')),\"\",\""+card+"\"),\n"
        if c == 1:
            hquery += ",\"\"),\n"
    aquery = ""
    for name in team2:
        c = 0
        if "!Yellow" in name:
            card = re.findall('!Yellow((?:\s\d+\'(?:\+\d+\')*)*)',name,re.IGNORECASE)[0].strip()
            temp = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
            temp = updateName(temp)
            aquery += "((select id from appearances where player = (SELECT id from players where playerName = '"+temp+"') and game = (select id from games where date='"+date+"')),\""+card+"\""
            c = 1
        if "!Red" in name:
            card = re.findall('!Red((?:\s\d+\'(?:\+\d+\')*)*)',name,re.IGNORECASE)[0].strip()
            if c == 1:
                aquery += ",\""+card+"\"),\n"
                c == 0
            else:
                temp = re.sub('(!\w+(?:\s\d+\'(?:\+\d+\')*)*\s)','',name)
                temp = updateName(temp)
                aquery += "((select id from appearances where player = (SELECT id from players where playerName = '"+temp+"') and game = (select id from games where date='"+date+"')),\"\",\""+card+"\"),\n"
        if c == 1:
            aquery += ",\"\"),\n"
    query += hquery + aquery
    query = ";".join(query.rsplit(",",1))
    f = open("cards.sql", "w")
    f.write(query)
    f.close()


getMatchSite(matchID)
