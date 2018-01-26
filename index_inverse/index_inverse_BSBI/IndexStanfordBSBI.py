from IndexInverse import *

class IndexStanfordBSBI(IndexInverse):
    def __init__(self):
        IndexInverse.__init__(self)
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()

    def removeStopWords(self,wordList):
        """Remove stop words from a list of words"""
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    def lemmatisation(self,wordList):
        return list(map(self.wl.lemmatize, wordList))
    
    def parseDoc(self, path_doc):
        """Function that returns a list of the terms in the doc after a linguistic process"""
        with open(path_doc, 'r') as f:
            wordList = []
            for line in f.readlines():
                wordList += line.split()
            wordList = self.removeStopWords(wordList)
            wordList = self.lemmatisation(wordList)
        return wordList
     
    def parseBlock(self, collection_path, block_number):
        """Function that takes a list of docs with tokens and returns a list of tuples (termid, frequency)"""
        #block_number is the number of the block
        start_time = time.time()
        termid_doc_f =[]
        path_temp = collection_path + str(block_number) + "/"
        for root, dirs, files in os.walk(path_temp):
            for file in files:
                filename = str(block_number) + file
                self.doc_docid[self.nb_doc] = filename
                path_file = path_temp + file
                wordDoc = self.parseDoc(path_file)
                for term in wordDoc:
                    if term not in self.term_termid.keys():
                        self.term_termid[term] = self.current_termid
                        termid_doc_f.append((self.term_termid[term], self.nb_doc))
                        self.current_termid += 1
                        
                    else:
                        termid_doc_f.append((self.term_termid[term], self.nb_doc))

                self.nb_doc += 1

        print("Parsing block " + str(block_number) + " : {} seconds ".format(time.time() - start_time))
        return termid_doc_f