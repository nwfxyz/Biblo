# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 17:27:07 2017

@author: NgWei
"""
#Satalkar, B. (2010, July 15). Water aerobics. Retrieved from http://www.buzzle.com
import os
import bs4
import calendar
from newspaper import Article
import requests
import dateparser
import logging

os.chdir(r'C:\Users\NgWei\OneDrive\Documents\GitHub\Biblo')
# Import pandas
import pandas as pd

# Assign spreadsheet filename to `file`
def findsoup(soup,string):
    for a in soup.find_all(string):
        print(a.get_text().strip())
    return(soup.find_all(text = string))

def getdate(string, parsed = False):
    try:
        date = dateparser.parse(string)
        date =  '(' + str(date.year) + ', ' + calendar.month_abbr[date.month] + ' ' + str(date.day) + ')'
    except: 
        if parsed:
            date = string
            date =  '(' + str(date.year) + ', ' + calendar.month_abbr[date.month] + ' ' + str(date.day) + ')'
        else:
            date = ''
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
    
    article = Article(webpage)
    article.download()
    article.parse()
    
    
    
    
    midn = ''
    try:
        if not r'&' in author:
            lastn = author.split()[len(author.split())-1]
            firstn = author.split()[0][0] + '.'
            if len(author.split()) >2 :
                midn = author.split()[1][0] + '.'
            comb = lastn + ',' + firstn + midn
        else:
            
            comb = ''
            for auth in author.split(' &'):
               lastn = auth.split()[len(auth.split())-1]
               firstn = auth.split()[0][0] + '.'
               if len(auth.split()) >2 :
                   midn = author.split()[1][0] + '.'
               name = lastn + ', ' + firstn
               if comb != '':
                   comb = comb + ' & '
               comb = comb + name
    except:
        comb = author
     
        
    return(comb + ' ' + getdate(date) + '. ' + title + ' Retrieved from ' + webpage )

        
   
        
def getauthor(self,author):
    midn = ''
    try:
        if not r'&' in author:
            lastn = author.split()[len(author.split())-1]
            firstn = author.split()[0][0] + '.'
            if len(author.split()) >2 :
                midn = author.split()[1][0] + '.'
            comb = lastn + ',' + firstn + midn
        else:
            
            comb = ''
            for auth in author.split(' &'):
               lastn = auth.split()[len(auth.split())-1]
               firstn = auth.split()[0][0] + '.'
               if len(auth.split()) >2 :
                   midn = author.split()[1][0] + '.'
               name = lastn + ', ' + firstn
               if comb != '':
                   comb = comb + ' & '
               comb = comb + name
    except:
        comb = author
    
    return comb

class reference:
         
    def __init__(self,webpage):
        self.webpage = webpage
        article = Article(webpage)
        article.download()
        article.parse()
        self.title = article.title
        try:
            self.author = getauthor(self,article.authors[0])
        except:
            self.author = ''
        try:
            self.date = getdate(article.publish_date,True)
        except:
            self.date = ''
            
        


    def getsource(self):
        source = self.author + ' ' + self.date + '. ' + self.title + ' Retrieved from ' + self.webpage
        return(source)



        
def main():
    file = 'Table.xlsx'
    
    # Load spreadsheet
    xl = pd.ExcelFile(file, index = False)
    
    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse('Sheet1',)
    BibloList = []
    for i in range(0,int(df1.shape[0])):
        print(i)
        ref = reference(
                df1.get_value(i,'Webpage')
                )
        BibloList.append(ref.getsource())
    Txtfile = open("Output.txt",'w')
    Txtfile.truncate()
    for item in BibloList:
        print(item)
        Txtfile.write("%s\n\n" % item)
    Txtfile.close()
        


    