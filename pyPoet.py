import random
import nltk
from nltk.tokenize import word_tokenize
from urllib.request import urlopen




partsOfSpeech = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]



# 1. Choose an arbitrary poem from poems.txt
# 2. Extract grammatical structure
# 3. Use Datamuse API to fill in the structure with related words of varying degree


# Step 1: Choosing arbitary poem

def choosePoem():
    poemsFile = open("poems.txt", "r")
    poems = poemsFile.readlines()
    lineNum = random.randint(0, 19917)
    while poems[lineNum] == "\n" or poems[lineNum + 1] == "\n" or poems[lineNum + 2] == "\n":
        lineNum += 1
    templatePoem = [line.rstrip() for line in poems[lineNum:lineNum+3]]
    return templatePoem

templatePoem = choosePoem()
# print(templatePoem)

# Step 2: Extract grammatical structure using nltk library

def extractPOS(templatePoem):
    for i in range(len(templatePoem)):
        line = nltk.pos_tag(word_tokenize(templatePoem[i]))
        line = [pair[1] for pair in line]
        templatePoem[i] = line
    return

extractPOS(templatePoem)
# print(templatePoem)

#Step 3: Use Datamuse API to craft poem

CREATIVITY = 40 # Determines how loosely the program chooses related words... implement later

def findNounLocs(templatePoem):
    nounLocations = []
    for lineNum in range(len(templatePoem)):
        for wordIndex in range(len(templatePoem[lineNum])):
            pos = templatePoem[lineNum][wordIndex]
            if pos[:2] == "NN":
                nounLocations.append([lineNum, wordIndex])
    return nounLocations





def chooseRandomWord(pos):
    poemsFile = open("poems.txt", "r")
    poems = poemsFile.readlines()
    word = "."
    while nltk.pos_tag([word])[0][1] != pos or word == "\n" or word == " ":
        # print(word, nltk.pos_tag([word])[0][1])
        lineNum = random.randint(0, 19917)
        word = random.choice(poems[lineNum].split(" "))
    return word.rstrip()





def generateHaiku(templatePoem):

    # First, we determine where the nouns will be placed
    nounLocations = findNounLocs(templatePoem)

    # Now choose one to be the 'primary' noun
    primaryNounIndex = random.choice(nounLocations)
    primaryNounType = templatePoem[primaryNounIndex[0]][primaryNounIndex[1]]

    primaryNoun = chooseRandomWord(primaryNounType)
    # primaryNoun = "writing"   

    retPoem = templatePoem.copy()
    retPoem[primaryNounIndex[0]][primaryNounIndex[1]] = primaryNoun
    # templatePoem[primaryNounIndex[0]].pop(primaryNounIndex[1])

    listOfNouns = [primaryNoun]
    listOfAdjs = []
    listOfVerbs = []

    for i in range(3):
        for j in range(len(templatePoem[i])):
            pos = templatePoem[i][j]
            if retPoem[i][j] == pos:
                # print(retPoem)
                fillWord(pos, listOfNouns, listOfAdjs, templatePoem, retPoem, i, j)
    
    print()
    for i in range(len(retPoem)):
        print(" ".join(retPoem[i]))





def fillWord(pos, listOfNouns, listOfAdjs, templatePoem, retPoem, i, j):
    if "NN" in pos: # NOUN
        retPoem[i][j] = findMatchingNoun(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j)
    if "JJ" in pos: # ADJECTIVE
        retPoem[i][j] = findMatchingAdj(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j)
    if "IN" in pos: # PREPOSITION
        retPoem[i][j] = findMatchingPrep(templatePoem, retPoem, i, j)
    if "DT" in pos: # DETERMINER
        retPoem[i][j] = findMatchingDet(templatePoem, retPoem, i, j)
    if "V" in pos: # VERB
        retPoem[i][j] = findMatchingVerb(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j)
    if pos == "TO": # TO
        retPoem[i][j] = "to"
    if "CD" in pos: # CARDINAL DIGIT
        retPoem[i][j] = chooseRandomWord(pos)
    if "PRP" in pos: # PRONOUN
        retPoem[i][j] = chooseRandomWord(pos)
    if pos == "POS": # POSSESSIVE PRONOUN
        retPoem[i][j] = chooseRandomWord("NN") + "'s"
    if pos == "PDT": # PREDETERMINER
        retPoem[i][j] = "all"
    if "RB" in pos: # ADVERB
        retPoem[i][j] = findMatchingAdv(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j)
    if "CC" in pos: # CONJUNCTION
        retPoem[i][j] = findMatchingCC(templatePoem, retPoem, i, j)
    if "RP" == pos: # PARTICLE
        retPoem[i][j] = chooseRandomWord(pos)
    if "." == pos or "," == pos or "-" == pos or "?" == pos: # PUNCTUATION
        retPoem[i][j] = pos
    if ":" == pos or ";" == pos: # PUNCTUATION
        retPoem[i][j] = "-"
    if "UH" in pos: # INTERJECTION
        retPoem[i][j] = chooseRandomWord(pos)
    if "FW" in pos: # FOREIGN WORD
        retPoem[i][j] = chooseRandomWord(pos)
    if "EX" in pos: # EXISTENTIAL 
        retPoem[i][j] = chooseRandomWord(pos)
    if pos[0] == "W": # MORE PRONOUN
        retPoem[i][j] = chooseRandomWord(pos)
    if "MD" in pos: # MODAL 
        retPoem[i][j] = chooseRandomWord(pos)
    if "SYM" in pos: # SYMBOL 
        retPoem[i][j] = chooseRandomWord(pos)





def findMatchingNoun(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    query = "https://api.datamuse.com/words?"
    if listOfNouns:
        query += "topics=" + ",".join(listOfNouns) # Associate noun with other nouns (could switch this to primaryNoun to see difference...)
        # print(templatePoem)
        if j > 0 and "JJ" in nltk.pos_tag([retPoem[i][j-1]])[0][1] and templatePoem[i][j-1] not in partsOfSpeech: # Check if previous word is an adjective
            query += "&rel_jja=" + retPoem[i][j-1].replace(' ', '')
        elif j > 0:
            query += "&rel_bga=" + retPoem[i][j-1].replace(' ', '')
        # print(query)
        html = extractText(query)
        if html == ['[]']:
            html = extractText("https://api.datamuse.com/words?" + "topics=" + listOfNouns[0].replace(' ', ''))
            if html == ['[]']:
                word = chooseRandomWord(pos)
                # print("chose random noun here: " + word)
                return word
        randomWord = []
        counter = 0
        while counter < min(len(html), 1000) and (randomWord == [] or nltk.pos_tag([randomWord[3]])[0][1] != pos or randomWord[3] in listOfNouns):
            randomWord = html[counter].split('"')
            counter += 1
            # print(randomWord)
        if counter == 1000 or counter == len(html):
            word = chooseRandomWord(pos)
            # print("chose random noun: " + word)
            listOfNouns.append(word)
            return word
        randomWord = randomWord[3]
    listOfNouns.append(randomWord)
    return randomWord





def findMatchingAdj(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    html = "meep"
    query = "https://api.datamuse.com/words?"
    if j > 0:
        query += "rel_bga=" + retPoem[i][j-1] + "&topics=" + listOfNouns[0].replace(' ', '')
        html = extractText(query)
        if j < len(templatePoem[i]) - 1 and "NN" in nltk.pos_tag([retPoem[i][j+1]])[0][1] and templatePoem[i][j+1] not in partsOfSpeech:
            query += "&rel_jjb=" + templatePoem[i][j+1].replace(' ', '')
        html = extractText(query)
    elif j < len(templatePoem[i]) - 1 and "NN" in nltk.pos_tag([retPoem[i][j+1]])[0][1] and templatePoem[i][j+1] not in partsOfSpeech:
            query += "rel_jjb=" + templatePoem[i][j+1].replace(' ', '')
    if html == ['[]']:
        query = "https://api.datamuse.com/words?" + "rel_jjb=" + listOfNouns[0].replace(' ', '')
        html = extractText(query)
    randomWord = []
    counter = 0
    # print(query)
    while counter < min(len(html), 1000) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
            randomWord = html[counter].split('"')
            counter += 1
            # print(randomWord)
    if counter == 1000 or counter == len(html):
        word = chooseRandomWord(pos)
        listOfAdjs.append(word)
        return word
    randomWord = randomWord[3]
    listOfAdjs.append(randomWord)
    return randomWord
    



def findMatchingPrep(templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    html = "meep"
    query = "https://api.datamuse.com/words?"
    if j > 0:
        query += "rel_bga=" + retPoem[i][j-1].replace(' ', '')
        html = extractText(query)
        randomWord = []
        counter = 0
        while counter < min(len(html), 100) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
            randomWord = html[counter].split('"')
            counter += 1
        if counter == 100 or counter == len(html):
            word = chooseRandomWord(pos)
            return word
        randomWord = randomWord[3]
    else:
        randomWord = chooseRandomWord(pos)
    return randomWord



def findMatchingDet(templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    html = "meep"
    query = "https://api.datamuse.com/words?"
    if j > 0:
        query += "rel_bga=" + retPoem[i][j-1].replace(' ', '')
        html = extractText(query)
        randomWord = []
        counter = 0
        while counter < min(len(html), 100) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
            randomWord = html[counter].split('"')
            counter += 1
        if counter == 100 or counter == len(html):
            word = chooseRandomWord(pos)
            return word
        randomWord = randomWord[3]
    else:
        randomWord = chooseRandomWord(pos)
    return randomWord




def findMatchingVerb(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    query = "https://api.datamuse.com/words?"
    query += "topics=" + ",".join(listOfNouns)
    if j > 0:
        query += "&rel_bga=" + retPoem[i][j-1].replace(' ', '')
    html = extractText(query)
    randomWord = []
    counter = 0
    while counter < min(len(html), 1000) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
        randomWord = html[counter].split('"')
        counter += 1
    if counter == 1000 or counter == len(html):
        if j > 0:
            query += "https://api.datamuse.com/words?" + "rel_bga=" + retPoem[i][j-1].replace(' ', '')
            html = extractText(query)
            randomWord = []
            counter = 0
            while counter < min(len(html), 1000) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
                randomWord = html[counter].split('"')
                counter += 1
        if counter == 1000 or counter == len(html):
            if j > 0 and retPoem[i][j-1].lower() == "i":
                return "am"
            elif j > 0 and (retPoem[i][j-1].lower() == "we" or retPoem[i][j-1].lower() == "they"):
                return "are"
            elif j > 0 and (retPoem[i][j-1].lower() == "she" or retPoem[i][j-1].lower() == "he"):
                return "is"
            word = chooseRandomWord(pos)
            # print("chose random verb: " + word)
            return word
    randomWord = randomWord[3]
    randomWord = chooseRandomWord(pos)
    return randomWord



def findMatchingAdv(listOfNouns, listOfAdjs, templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    query = "https://api.datamuse.com/words?"
    query += "topics=" + listOfNouns[0].replace(' ', '')
    if j > 0:
        query += "&rel_bga=" + retPoem[i][j-1].replace(' ', '')
    elif j < len(templatePoem[i]) - 1 and templatePoem[i][j+1] not in partsOfSpeech:
        query += "&rel_bgb=" + retPoem[i][j+1].replace(' ', '')
    html = extractText(query)
    randomWord = []
    counter = 0
    while counter < min(len(html), 1000) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
        randomWord = html[counter].split('"')
        counter += 1
    if counter == 1000 or counter == len(html):
        word = chooseRandomWord(pos)
        return word
    randomWord = randomWord[3]
    randomWord = chooseRandomWord(pos)
    return randomWord



def findMatchingCC(templatePoem, retPoem, i, j):
    pos = templatePoem[i][j]
    randomWord = "meep"
    html = "meep"
    query = "https://api.datamuse.com/words?"
    if j > 0:
        query += "rel_bga=" + retPoem[i][j-1].replace(' ', '')
        html = extractText(query)
        randomWord = []
        counter = 0
        while counter < min(len(html), 100) and (randomWord == [] or len(randomWord) < 4 or nltk.pos_tag([randomWord[3]])[0][1] != pos):
            randomWord = html[counter].split('"')
            counter += 1
        if counter == 100 or counter == len(html):
            word = chooseRandomWord(pos)
            return word
        randomWord = randomWord[3]
    else:
        randomWord = chooseRandomWord(pos)
    return randomWord


def extractText(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8").split("},{")
    return html

# Main body of program:
generateHaiku(templatePoem)
