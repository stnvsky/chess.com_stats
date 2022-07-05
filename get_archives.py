#!/usr/bin/env python3

# chess.com API -> https://www.chess.com/news/view/published-data-api
# The API has been used to download monthly archives for a user using a Python3 program.
# This program works as of 03.07.22

import urllib
import urllib.request
import os
import sys

if (len(sys.argv) != 2):
   print('Pass the username')
   exit(0)

username = sys.argv[1]
baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
archivesUrl = baseUrl + "archives"

#read the archives url and store in a list
f = urllib.request.urlopen(archivesUrl)
archives = f.read().decode("utf-8")
archives = archives.replace("{\"archives\":[\"", "\",\"")
archivesList = archives.split("\",\"" + baseUrl)
archivesList[len(archivesList)-1] = archivesList[len(archivesList)-1].rstrip("\"]}")

#download all the archives
for i in range(len(archivesList)-1):
    url = baseUrl + archivesList[i+1] + "/pgn"
    filename = archivesList[i+1].replace("/", "-")
    if (not os.path.isdir(username)):
        os.mkdir(username)
    urllib.request.urlretrieve(url, "./" + username + "/" + filename + ".pgn")
    print(filename + ".pgn has been downloaded.")
print ("All files have been downloaded.")

print("\nTime spent on the games:\n")
os.system("python3 ./get_times.py " + username)
