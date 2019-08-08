# Downloads and creates source directory for problem (C++)

from bs4 import BeautifulSoup
import os
import wget
import shutil
import urllib
import sys


def getChallengeNames(domainLink):
    challengeNames = []

    page = urllib.request.urlopen(domainLink)
    soup = BeautifulSoup(page)

    # <a ... data-analytics="ChallengeListChallengeName" ... data-attr1="two-strings" ...>

    all_links = soup.find_all("a")
    for link in all_links:
        if link.get("data-analytics") == "ChallengeListChallengeName":
            challengeNames.append(link.get("data-attr1"))

    return challengeNames


def getChallengeCppCode(challengeLink):

    page = urllib.request.urlopen(challengeLink)
    
    html = page.read()
    html = html.decode("utf-8")
    
    text = html[html.find("cpp_template"):(html.find("java_template")-7)]
    text = text.replace('cpp_template', '')
    text = text.replace('%22:%22', '')
    text = text.replace('%22', '')
    text = text.replace('%20', ' ')
    text = text.replace('%3C', '<')
    text = text.replace('%3E', '>')
    text = text.replace('%5C%5C%5Cn%5C', '\"\\n"')
    text = text.replace('%5C%5Cn', '\\n')
    text = text.replace('%7B', '{')
    text = text.replace('%7D', '}')
    text = text.replace('%5B', '[')
    text = text.replace('%5D', ']')
    text = text.replace('%5Cn', '\n')
    text = text.replace('%5Ct', '\t')
    text = text.replace(',_head', '')
    text = text.replace(',_tail', '')
    text = text.replace('and', '&&')
    text = text.replace('#include <bits/stdc++.h>', '')
    text = text.replace('using namespace std;', '')
    text = text.replace('%5C', '\"')

    codeLines = text.split('\n')

    for i in range(len(codeLines)):
        codeLines[i] = codeLines[i] + "\n"

    codeLines.insert(0, '#include \"bits/stdc++.h\"\n')
    codeLines.insert(1, 'using namespace std;\n\n\n')

    return codeLines


def getChallenge(challengeName):

    challengeLink = "https://www.hackerrank.com/challenges/" + challengeName + "/problem"
    challengePDFLink = "https://www.hackerrank.com/rest/contests/master/challenges/" + \
        challengeName + "/download_pdf?language=English"

    wget.download(challengePDFLink)

    # main.cpp
    lines = getChallengeCppCode(challengeLink)

    with open("main.cpp", mode="w") as f:
        f.writelines(lines)

    # CMakeLists.txt
    lines = []
    lines.append("cmake_minimum_required (VERSION 3.14.0)\n")
    lines.append("project(main)\n")
    lines.append("add_executable(main main.cpp bits/stdc++.h)\n")

    with open("CMakeLists.txt", mode="w") as f:
        f.writelines(lines)


if __name__ == "__main__":

    # tested: count-triplets-1
    # tested: ctci-ransom-note
    # tested: sherlock-and-anagrams

    getChallenge(sys.argv[1])