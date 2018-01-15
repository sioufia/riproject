import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os



class IndexStanford:
    def __init__(self):
        # Dictionnaries to build
        self.dico_termID = {}  # {term:termID}
        self.dico_docID = {}  # {doc:docID}
        self.dico_index = {}  # {termID:docID}

        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()



    def removeStopWords(self,wordList): #Remove stop words from a list of words
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    @staticmethod
    def lineSplit(line): #Split a line of words into a list of words
        return line.split()

    def lemmatisation(self,wordList):
        return list(map(self.wl.lemmatize, wordList))

    def indexConstruction(self,path): #Construction of the index
        self.docID = 0
        self.termID = 0

        for i in range(0, 9):  # Browsing blocks
            print(i)
            path_temp = path + str(i) + "/"
            print("path_temp:" +  path_temp)
            for root, dirs, files in os.walk(path_temp):
                print("file:" +  files)
                for file in files:
                    print("file:" +  file)
                    filename = str(i) + file
                    self.dico_docID[self.docID] = filename

                    with open(path_temp + file, 'r') as f:

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        for w in self.wordList:
                            if not w in self.dico_termID.keys(): #Checking if the term already exists in the dictionnary
                                print('OK')
                                self.dico_termID[w] = self.termID
                                self.dico_index[self.termID] = [self.docID]
                                self.termID += 1
                            else:
                                self.dico_index[self.dico_termID[w]] += [self.docID]

                    self.docID += 1


#index = IndexStanford()
#index.indexConstruction("C:/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")


