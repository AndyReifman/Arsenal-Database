#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ANDREW REIFMAN-PACKETT
# 2020.05.21 
# Set a match URL and create a query to add a team, add a match, add the players,
#   add the appearances, and add the goals.

import requests,re
from unidecode import unidecode
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH
matchID = "541578";
#!!IMPORTANT!! THIS SHOULD BE THE ONLY THING WE NEED TO UPDATE FOR EVERY MATCH

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
                        playertext += '!yellow '
                    if 'icon-soccer-goal' in playerInfo:
                        playertext += '!goal '
                    if 'icon-redcard' in playerInfo:
                        playertext += '!red '
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
                        playertext += '!yellow '
                    if 'icon-soccer-goal' in playerInfo:
                        playertext += '!goal '
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

    ### SHOULD ADD HOME/AWAY LOGIC HERE
    venue = re.findall('<div>VENUE: (.*?)<', line_html, re.DOTALL)
    if venue != []:
        venue = venue[0]
    team1Start,team1Sub,team2Start,team2Sub = getLineUps(matchID)
    opposition = team1fix if team2fix is "Arsenal" else team2fix
    if opposition == team1fix:
        home = "Away"
    #addGameQuery(ko_date, opposition,home,"premier league")
    #addPlayersQuery(team1Start,team2Start)
    addAppearancesQuery(ko_date,team1fix,team1Start,team2fix,team2Start)

def addGameQuery(date, opposition, home, comp):
    print(date)
    print(opposition)
    print("INSERT INTO games (date,opposition,`home/away`,competition)")
    print("VALUES")
    print("(\""+date+"\",(select id from clubs where name = '"+opposition+"'),\""+home+"\",(select id from competitions where competition = '"+comp+"'));")

def addPlayersQuery(team1,team2):
    query = "INSERT IGNORE INTO players (playerName)\n"
    query += "VALUES\n"
    for name in team1:
        name = re.sub('(!\w+\s)','',name)
        query += "(\""+name+"\"),\n"
    for name in team2:
        name = re.sub('(!\w+\s)','',name)
        query += "(\""+name+"\"),\n"
    print(query)

def addAppearancesQuery(date,team1Name,team1,team2Name,team2):
    query = "INSERT INTO appearances (game,player,club,sub)\n"
    query += "VALUES\n"
    for name in team1:
        sub = "0"
        if "!Sub" in name:
            sub = "1"
        name = re.sub('(!\w+\s)','',name)
        query += "((select id from games where date = '"+date+"'),(select id from players where playerName = '"+name+"'),(selec id from clubs where name = '"+team1Name+"'),"+sub+"),\n"
    print(query)

getMatchSite(matchID)
