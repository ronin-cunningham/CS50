import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        #allocated lists to load info into
        self.positivelist = []
        self.negativelist = []

        #load positive and negative words into lists
        with open("positive-words.txt") as positives:
            for line in positives:
                if line.startswith(";") != True:
                    self.positivelist.append(line.strip("\n"))

        with open("negative-words.txt") as negatives:
            for line in negatives:
                if line.startswith(";") != True:
                    self.negativelist.append(line.strip("\n"))



    def analyze(self, text):
        #split input command line text into tokens

        self.tokenizer = nltk.tokenize.TweetTokenizer()
        self.token = self.tokenizer.tokenize(text)

        #set score regarding the words in the token and return its value
        score = 0

        for words in self.token:
            if words.lower() in self.positivelist:
                score +=1
            elif words.lower() in self.negativelist:
                score -=1
            else:
                continue


        return score