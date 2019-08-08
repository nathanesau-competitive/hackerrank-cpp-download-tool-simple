# Downloads and creates source directory for problem (C++)

from bs4 import BeautifulSoup
import os
import wget
import shutil
import urllib
import sys
from zipfile import ZipFile

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

    # find + replace bad characters
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
    text = text.replace("getenv(\"OUTPUT_PATH\")", "\"output.txt\"")

    codeLines = text.split('\n')

    # insert code after int main()
    for i in range(len(codeLines)):
        if codeLines[i] == "int main()":
            codeLines.insert(i+2, "    //inserted code")
            codeLines.insert(
                i+3, "    string inputFName = \"input/input00.txt\";")
            codeLines.insert(
                i+4, "    string outputFName = \"output/output00.txt\";")
            codeLines.insert(i+5, "    std::ifstream in(inputFName);")
            codeLines.insert(i+6, "    std::ofstream out(\"output.txt\");")
            codeLines.insert(i+7, "    std::cin.rdbuf(in.rdbuf());")
            codeLines.insert(i+8, "    std::cout.rdbuf(out.rdbuf());")
            codeLines.insert(
                i+9, "    auto comparator = make_unique<TextComparator>(outputFName, out);")
            codeLines.insert(i+10, "    //end inserted code")
            break

    codeLinesKeep = []

    # remove double blank lines
    prevLineBlank = False
    for i in range(len(codeLines)):
        if prevLineBlank is True:
            if codeLines[i] == "":
                continue  # do not keep this line
            else:
                prevLineBlank = False
                codeLinesKeep.append(codeLines[i])
        else:
            codeLinesKeep.append(codeLines[i])
            if codeLines[i] == "":
                prevLineBlank = True

    for i in range(len(codeLinesKeep)):
        codeLinesKeep[i] += "\n"

    # insert code at top of file
    codeLinesKeep.insert(0, '#include \"bits/stdc++.h\"\n')
    codeLinesKeep.insert(1, '#include \"bits/textComparator.h\"\n')
    codeLinesKeep.insert(2, 'using namespace std;\n\n')

    return codeLinesKeep


def getChallenge(challengeName):

    challengeLink = "https://www.hackerrank.com/challenges/" + challengeName + "/problem"
    challengePDFLink = "https://www.hackerrank.com/rest/contests/master/challenges/" + \
        challengeName + "/download_pdf?language=English"
    testCasesLink = "https://www.hackerrank.com/rest/contests/master/challenges/" + \
        challengeName + "/download_testcases"

    wget.download(challengePDFLink)
    wget.download(testCasesLink)

    # unzip
    with ZipFile(challengeName + '-testcases.zip', 'r') as zipObj:
        zipObj.extractall()

    # main.cpp
    lines = getChallengeCppCode(challengeLink)
    lines.insert(0, "// " + challengeLink + "\n")

    with open("main.cpp", mode="w") as f:
        f.writelines(lines)

    # CMakeLists.txt
    lines = []
    lines.append("cmake_minimum_required (VERSION 3.14.0)\n")
    lines.append("project(main)\n")
    lines.append(
        "add_executable(main main.cpp bits/stdc++.h bits/textComparator.h)\n")

    with open("CMakeLists.txt", mode="w") as f:
        f.writelines(lines)

    # modify env variables
    os.environ["OUTPUT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    

if __name__ == "__main__":

    # tested
    #
    # ctci-ransom-note
    # count-triplets-1
    # sherlock-and-anagrams

    getChallenge(sys.argv[1])
