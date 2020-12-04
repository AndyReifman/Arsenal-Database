#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ANDREW REIFMAN-PACKETT
# 2020.12.03
#Grab all the MatchIDs from transfermarkt based on a given year.

import requests,re,subprocess,sys
from unidecode import unidecode
from bs4 import BeautifulSoup

def scrape(year):
    f = open("matches.txt", "w")
    url = "https://www.transfermarkt.us/arsenal-fc/spielplandatum/verein/11/plus/0?saison_id="+str(year)+"&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-"
    yearWebsite = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    year_html = yearWebsite.text
    soup = BeautifulSoup(year_html, "lxml")
    table = soup.find("div",{"class","responsive-table"})
    for row in table.findAll("tr")[2:]:
        match = row.findAll("td")[9].findAll('a')[0]['href'].rsplit('/', 1)[-1]
        f.write(match + '\n')
    f.close()




if __name__ == '__main__':
    scrape(sys.argv[1])
