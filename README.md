# TwitterStockSentimentAnalyzer_webApp
Python Flask web app to analyze market sentiment for equities using Twitter API

● Created a Flask application which connects to Twitter API using Python tweepy package and fetched top 1000 tweets for a stock the user
entered into web form

● Used WTForms to take the user inputted data and pass it to backend to trigger the analysis

● Used pandas and textblob to analyze the tweets and measure the subjectivity and polarity of each tweet

● Displayed the data on a word cloud, plot graph, and bar graph using mathplotlib. This allowed users to construct a long/short thesis based
on the data

● Deployed the application using AWS Elastic Beanstalk and CodePipeline for continuous delivery
