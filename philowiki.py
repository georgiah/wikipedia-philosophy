# -*- coding: utf-8 -*-
import urllib
import pickle
import os
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

def getExceptionSiteList():
    f = open('docs/index.html', 'r')
    text = f.read()
    f.close()
    parsedHtml = BeautifulSoup(text, 'html.parser')
    parsedHtml = parsedHtml.find('ul', {'id': 'exceptions-sites'})
    exceptions = []
    for child in parsedHtml.children:
        if child.string == '\n':
            continue
        exceptions.append((child.string).strip())

    return exceptions

def exceptionFound(hist):
    newString = ''
    for item in list(set(hist) - set(exceptions)):
        newString += '<li><a href="https://wikipedia.org' + item + '">"' + item + '</a></li>\n'
    writeToHTML(newString)

def writeToHTML(newString):
    newSoup = BeautifulSoup(newString, 'html.parser')
    f = open('docs/index.html', 'r')
    text = f.read()
    f.close()
    oldSoup = BeautifulSoup(text, 'html.parser')
    oldSoup.find('ul', {'id': 'exceptions-sites'}).append(newSoup)
    f = open('docs/index.html', 'w')
    f.write(oldSoup.prettify())
    f.close()
    commitCmd = 'git commit -a -m "Updated HTML file"'
    pushCmd = 'git push'
    os.system(commitCmd)
    os.system(pushCmd)

def bracketParser(parsedString):
    ob = 0
    cb = 0
    start = 0
    cuts = []
    ot = 0
    skip = 0
    for i in range(0, len(parsedString)):
        if skip:
            if parsedString[i] == '>':
                skip = 0
        else:
            if ot == 1:
                if parsedString[i] == 'a' and ob == 0:
                    skip = 1
                ot = 0
            if parsedString[i] == '<':
                ot = 1
            if parsedString[i] == '(':
                ob += 1
                if start == 0:
                    start = i
            if parsedString[i] == ')' and ob != 0:
                cb += 1
                if cb == ob:
                    cuts.append([start, i])
                    start = 0
                    ob = 0
                    cb = 0

    for cut in cuts[::-1]:
        parsedString = parsedString[:cut[0]] + parsedString[cut[1] + 1:]
    return parsedString

def validate(history):
    if len(history) != len(set(history)):
        print('\nEntered a loop')
        exceptionFound(history[1:])
        return 0
    if goal in history:
        print('\nReached Philosophy in %d steps' % (len(history) - 1))
        return 0
    return 1

# constants
classes = ['hatnote', 'thumb', 'IPA', 'boilerplate']
ids = ['coordinates']
suffixes = ['.png', '.PNG', '.svg', '.SVG', '.gif', '.GIF', '.jpg', 'JPG', '.jpeg', '.JPEG']

urlBase = "https://en.wikipedia.org"
goal = "/wiki/Philosophy"

while True:
    # load the site dictionary
    try:
        sites = pickle.load(open('wikidict.p', 'rb'))
    except:
        sites = {}
        pickle.dump(sites, open('wikidict.p', 'wb'))

    exceptions = getExceptionSiteList()

    # start with a random article
    history = ['/wiki/Special:Random']

    while validate(history):
        # if we already know where this page links, look it up
        try:
            history.append(sites[history[-1]])
            print(history[-1])
            continue
        # otherwise, generate a new URL
        except:
            url = urlBase + history[-1]

        # open the URL and parse the data
        data = urllib.urlopen(url)
        parsedHtml = BeautifulSoup(data, "html.parser")

        # find the div where the content starts and remove text in brackets
        parsedHtml = parsedHtml.find('div', {'class': 'mw-parser-output'})
        parsedString = parsedHtml.prettify().encode('utf-8')
        parsedString = bracketParser(parsedString)

        # parse the resulting html and find all the link
        parsedHtml = BeautifulSoup(parsedString, "html.parser")
        links = parsedHtml.find_all('a')

        # if there aren't any links, the game's over
        if len(links) == 0:
            print('\nNo available links')
            exceptionFound(history[1:])
            break

        for link in links:
            tabled = False

            # if there isn't a URL to reference, skip to the next link
            try:
                a = link['href']
            except:
                continue

            # if the link isn't internal, or is an image, skip to the next link
            if (a[:6] != '/wiki/' or any(x in a for x in suffixes) or a[:16] == '/wiki/Wikipedia:'):
                continue

            for parent in link.parents:
                try:
                    clss = parent['class']
                except:
                    clss = ''
                try:
                    d = parent['id']
                except:
                    d = ''

                # if the link has a parent that signifies it isn't in the main
                # content body, set the tabled flag and skip to the next link
                if (parent.name == 'table' or any(x in d for x in ids) or
                any(x in clss for x in classes)):
                    tabled = True
                    break
            if tabled:
                continue

            # if the link jumps to a section, remove that section from the URL
            pos = a.find('#')
            if pos != -1:
                a = a[:pos]

            # add the new link to the history and update the dictionary
            history.append(a)
            print(history[-1])
            if len(history) > 2:
                sites[history[-2]] = history[-1]
            break

    # save the dictionary
    pickle.dump(sites, open('wikidict.p', 'wb'))
