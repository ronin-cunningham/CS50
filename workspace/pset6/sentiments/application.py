from flask import Flask, redirect, render_template, request, url_for
import os
import sys
from analyzer import Analyzer
import helpers
from helpers import get_user_timeline
import nltk

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    if get_user_timeline(screen_name) == None:
        return redirect(url_for("index"))
    else:
        tweets = str(get_user_timeline(screen_name))

    #tokenize tweets
    tokenizer = nltk.tokenize.TweetTokenizer()
    tokenlist = tokenizer.tokenize(tweets)
    #initialize analyzer
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positives, negatives)

    #set variables
    positivescore, negativescore, neutralscore = 0, 0, 0

    #analyze word in tweet tokenlist
    for word in tokenlist:
        wordscore = analyzer.analyze(word)
        if wordscore > 0.0:
            positivescore +=1
        elif wordscore < 0.0:
            negativescore += 1
        else:
            neutralscore += 1

    # generate chart
    chart = helpers.chart(positivescore, negativescore, neutralscore)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
