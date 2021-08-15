#used to access API
import tweepy
#used for sentiment analyzes 
from textblob import TextBlob
#used to create word cloud
from wordcloud import WordCloud
#analyze data 
import pandas as pd
#math operations
import numpy as np
#suports regular exp
import re 
#used to plot graphs
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import os
from configparser import ConfigParser
from datetime import datetime

class TwitterAnalyzer:
    """description of class"""
    plotGraph = None

    def __init__(self, ticker):
        self.ticker = ticker 
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        print(configdir)
        config = ConfigParser()
        config.read(configdir)
        print(config.sections())
        consumerKey = config['keys']['APIKey']
        consumerSecretKey = config['keys']['APISecretKey']
        accessToken = config['keys']['AccessToken']
        accessTokenSecret = config['keys']['AccessTokenSecret']
        authenticate = tweepy.OAuthHandler(consumerKey,consumerSecretKey)
        authenticate.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(authenticate, wait_on_rate_limit = True )

        posts = api.search(q= ticker, count = 100, lang = "en", tweet_mode="extended") 
        df = pd.DataFrame([msg.full_text for msg in posts], columns = ['Tweets'])
        df['Tweets'] = df['Tweets'].apply(self.cleanText)
        df['Subjectivity'] = df['Tweets'].apply(self.getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(self.getPolarity)
        df['Analysis'] = df['Polarity'].apply(self.getAnalysis)
        allWords = ''.join([twts for twts in df['Tweets']])
        self.getWordCloud(allWords)
        self.getPlotGraph(df,ticker)
        self.getBarGraph(df,ticker)
        print(df)

    #Create a function to clean the tweets
    def cleanText(self, text):
        text = re.sub(r'@[A-Za-z0-9]+' ,'', text) # Remove @mentions
        text = re.sub(r'#', '', text) #Removing the '#' symbol
        text = re.sub(r'RT[\s]+', '', text) #Removing RT
        text = re.sub(r'https?:\/\/\S+', '', text) #Remove the hyper link
        return text
 
    #polarity: negative vs. positive    (-1.0 => +1.0)
    def getSubjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity 

    #subjectivity: objective vs. subjective (+0.0 => +1.0)
    def getPolarity(self, text):
        return TextBlob(text).sentiment.polarity

    #Compute negative, neutral, and positive analysis 
    def getAnalysis(self, score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def getFileName(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        imagedir = '/'.join([path,'static/images/'+ name +'.png'])
        return imagedir

    def getWordCloud(self, allWords):
        wordCloud =  WordCloud(width = 1000, height = 600, random_state= 21, max_font_size = 200).generate(allWords)
        path = os.path.dirname(os.path.realpath(__file__))
        #imagedir = '/'.join([path,'static/images/wordCloud.png'])
        imagedir = self.getFileName('wordCloud')
        print(imagedir)
        wordCloud.to_file(imagedir)
        #plt.savefig(imagedir)

    def getPlotGraph(self,df,ticker):
        #plot the polarity and subjectivity 
        plt.figure(figsize=(8,6))
        path = os.path.dirname(os.path.realpath(__file__))
        #imagedir = '/'.join([path,'static/images/plotGraph.png'])
        imagedir = self.getFileName('plotGraph')
        print(imagedir)
        #print(os.listdir(imagedir))
        for i in range(0,df.shape[0]):
            plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color = 'Blue')

        plt.title('Sentiment Analysis '+ ticker)
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity')
        plt.tight_layout()
        plt.savefig(imagedir)

    def getBarGraph(self,df,ticker):
        path = os.path.dirname(os.path.realpath(__file__))
        #imagedir = '/'.join([path,'static/images/barGraph.png'])
        imagedir = self.getFileName('barGraph')
        df['Analysis'].value_counts()
        plt.title('Sentiment Analysis ' + ticker)
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df['Analysis'].value_counts().plot(kind='bar')
        plt.tight_layout()
        plt.savefig(imagedir)
        






