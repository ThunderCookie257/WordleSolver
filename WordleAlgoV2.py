from curses.ascii import isalpha
from multiprocessing.sharedctypes import Value
from re import I

# generates a static list of 5 letter words with raw score values  
class wordsList:
    # sets up custom word list 
    def __init__(self):
        self.words = []
        self.getAllWords()
        self.assignValues()


    # to iterate through the text file and get all words into the words variable 
    def getAllWords(self):
        with open('All_Words.txt') as allWords:
            for line in allWords:
                newWord = customWord(line)
                self.words.append(newWord)

    # assigns numerical values to each customWord in the list 
    def assignValues(self):
        for word in self.words:
            word.getValue()

# custom word that contains a score value 
class customWord:
    
    # create the custom word 
    def __init__(self, wordName):
        self.wordName = wordName 
        self.value = 0 # numerical value of each word
    
    # sets the numerical value of each word
    # max value = 15... 5 for vowelValue, 5 for spreadValue, 5 for commonValue
    def getValue(self):
        self.value = self.vowelValue() + self.spreadValue() + self.commonValue()
    
    # assigns score to word for vowel use (1 point per use) 
    def vowelValue(self):
        Value = 0
        if self.wordName.count("a") > 0:
            Value += 1
        if self.wordName.count("e") > 0:
            Value += 1
        if self.wordName.count("i") > 0:
            Value += 1
        if self.wordName.count("o") > 0:
            Value += 1
        if self.wordName.count("u") > 0:
            Value += 1
        return Value

    # assigns a score to word for number of distinct letters 
    def spreadValue(self):
        spreadVal = 5;
        for i in range(len(self.wordName)):
            if self.wordName.count(self.wordName[i]) > 1:
                spreadVal -= 1;
        if spreadVal < 0:
            spreadVal = 0
        return spreadVal
    
    # assigns a score to word for how common its letters are 
    def commonValue(self):
        Value = 0
        if self.wordName.count("a") > 0:
            Value += 0.425
        if self.wordName.count("b") > 0:
            Value += 0.1
        if self.wordName.count("c") > 0:
            Value += 0.225
        if self.wordName.count("d") > 0:
            Value += 0.165
        if self.wordName.count("e") > 0:
            Value += 0.55
        if self.wordName.count("f") > 0:
            Value += 0
        if self.wordName.count("g") > 0:
            Value += 0.12
        if self.wordName.count("h") > 0:
            Value += 0.15
        if self.wordName.count("i") > 0:
            Value += 0.375
        if self.wordName.count("j") > 0:
            Value += 0
        if self.wordName.count("k") > 0:
            Value += 0
        if self.wordName.count("l") > 0:
            Value += 0.27
        if self.wordName.count("m") > 0:
            Value += 0.15
        if self.wordName.count("n") > 0:
            Value += 0.33
        if self.wordName.count("o") > 0:
            Value += 0.355
        if self.wordName.count("p") > 0:
            Value += 0.155
        if self.wordName.count("q") > 0:
            Value += 0
        if self.wordName.count("r") > 0:
            Value += 0.38
        if self.wordName.count("s") > 0:
            Value += 0.285
        if self.wordName.count("t") > 0:
            Value += 0.345
        if self.wordName.count("u") > 0:
            Value += 0.18
        if self.wordName.count("v") > 0:
            Value += 0
        if self.wordName.count("w") > 0:
            Value += 0
        if self.wordName.count("x") > 0:
            Value += 0
        if self.wordName.count("y") > 0:
            Value += 0
        if self.wordName.count("z") > 0:
            Value += 0
        if Value > 5:
            Value = 5
        return Value

# optimizes list based on wordle information (grey, yellow, and green words)
class OptimizeList:

    def __init__(self, wordsList):
        self.wordLst = wordsList
        self.optimizedList = self.wordLst.words
        self.greyList = [] # grey letters
        self.yellowList = [] # yellow letters 
        self.greenList = []  # green letters and position

    # checks if given word has any of the grey letters
    def checkGreys(self, word):
        for letter in self.greyList:
            if letter in word.wordName:
                return False 
        return True


    # removes all words from optimized list that contain any grey letter 
    def optimizeGreys(self):
        removeGreys = filter(self.checkGreys, self.optimizedList)
        listWithoutGreys = list(removeGreys)
        self.optimizedList = listWithoutGreys


    # checks if given word has all of the yellow letters 
    def checkYellows(self, word):
        for letter in self.yellowList:
            if not letter[0] in word.wordName or word.wordName.find(letter[0]) == int(letter[1]):
                return  False
        return True
    

    # removes all words from optimized list that don't contain every yellow letter 
    def optimizeYellows(self):
        removeYellows = filter(self.checkYellows, self.optimizedList)
        listWithYellows = list(removeYellows)
        self.optimizedList = listWithYellows

    # checks if given word has green letters in place 
    def checkGreens(self, word):
        for letter in self.greenList:
            if word.wordName.find(letter[0]) != int(letter[1]):
                return False 
        return True

    # removes all words that dont have letter in correct position 
    def optimizeGreens(self):
        removeGreens = filter(self.checkGreens, self.optimizedList)
        listWithGreens = list(removeGreens)
        self.optimizedList = listWithGreens
    
    # sorts the list in order of descending value (insertion sort algorithm)
    def sortList(self):
        for i in range(len(self.optimizedList) - 1):
            self.slide(i)
    
    # helper slide function for sorter 
    def slide(self, i):
        temp = self.optimizedList[i]
        pos = i 
        while pos > 0 and self.optimizedList[pos - 1].value < temp.value:
            self.optimizedList[pos] = self.optimizedList[pos - 1]
            pos -= 1
        self.optimizedList[pos] = temp



rawWords = wordsList()
start = OptimizeList(rawWords)

print("Best First guess:")
start.sortList()
print(start.optimizedList[0].wordName)

x = 0
while x != 7: 
    anyGrey = input("Are there any grey letters (y/n) ")
    while anyGrey == "y":
        start.greyList.append(input("Enter grey letter now "))
        anyGrey = input("Are there any grey letters (y/n) ")

    anyYellow = input("Are there any yellow letters (y/n) ")
    while anyYellow == "y":
        start.yellowList.append(input("Enter yellow letter now  with index (no space) "))
        anyYellow = input("Are there any yellow letters (y/n) ")

    anyGreen = input("Are there any green letters (y/n) ")
    while anyGreen == "y":
        start.greenList.append(input("Enter green letter now with index (no space) "))
        anyGreen = input("Are there any green letters (y/n) ")

    start.optimizeGreys()
    start.optimizeYellows()
    start.optimizeGreens()

    print("List successfully optimized")
    print("Printing best options now!")

    print(start.optimizedList[0].wordName)
    print(start.optimizedList[1].wordName)
    print(start.optimizedList[2].wordName)

    x += 1