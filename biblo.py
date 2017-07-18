# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 17:27:07 2017

@author: NgWei
"""
#Satalkar, B. (2010, July 15). Water aerobics. Retrieved from http://www.buzzle.com
import os
import bs4
import urllib
import calendar

import requests
import dateparser

def findsoup(soup,string):
    for a in soup.find_all(string):
        print(a.get_text().strip())
    return(soup.find_all(text = string))

def getdate(string):
    date = dateparser.parse(string)
    date =  '(' + str(date.year) + ', ' + calendar.month_abbr[date.month] + ' ' + str(date.day) + ')'
    return date

def Biblo(webpage,author,date):
    if not 'http' in webpage:
        webpage = "http://" + webpage
    r  = requests.get(webpage)
    data = r.text
    soup = bs4.BeautifulSoup(data, "lxml")
    title = soup.find_all('title')[0].get_text().strip()
    if title[len(title)-1] != r'.':
        title = title + r'.'
    if not r'&' in author:
        lastn = author.split()[len(author.split())-1]
        firstn = author.split()[0][0] + '.'
        comb = lastn + ',' + firstn
    else:
        
        comb = ''
        for auth in author.split(' &'):
           lastn = auth.split()[len(auth.split())-1]
           firstn = auth.split()[0][0] + '.'
           name = lastn + ',' + firstn
           if comb != '':
               comb = comb + ' & '
           comb = comb + name
    
    return(comb + ' ' + getdate(date) + '. ' + title + ' Retrieved from ' + webpage + '.' )

        
        

