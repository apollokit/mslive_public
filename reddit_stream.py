import datetime
from unidecode import unidecode
import time

import mysql.connector
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from file_utils import unyaml_thing

creds = unyaml_thing('creds_mod.yml')

analyzer = SentimentIntensityAnalyzer()

#Initialize reddit api here
reddit = praw.Reddit(
     client_id=creds['praw_client_id'],
     client_secret=creds['praw_client_secret'],
     user_agent=creds['praw_user_agent']
 )

#connect to a mysql server
mydb = mysql.connector.connect(
host =creds['mysql_host'],
user =creds['mysql_user'],
passwd =creds['mysql_passwd']
)

mycursor = mydb.cursor()

# Create a database for storing reddit data
mycursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

# Title and body would be used for the sentiment analysis and for counting the number of times a particular ticker is mentioned
mycursor.execute("""CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment
                (date_time DATETIME,
                subreddit VARCHAR(500),
                title VARCHAR(500),
                body VARCHAR(2000),
                author VARCHAR(500),
                sentiment DECIMAL(5,4)
                )
                """)

# pushing the data to the database
sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (date_time, subreddit, title, body, author, sentiment) VALUES (%s, %s, %s, %s, %s, %s)"

## Streaming comments from reddit
comment_count = 0
while True:
    try:
    # list of subreddits to be tracked -- you can add the ones you think are important to track
        subreddit = reddit.subreddit("wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading")
        for comment in subreddit.stream.comments(skip_existing=True):
                current_time = datetime.datetime.now()
                subreddit = str(comment.subreddit)
                author = str(comment.author)
                title = str(comment.link_title)
                body = str(comment.body)
                if len(body) < 2000:
                    body = body
                elif len(body) > 2000:
                    body = "data is too large" ## very rare situation - less than 0.1% of the cases have comment more than 2000 characters
                vs = analyzer.polarity_scores(unidecode(body))
                sentiment = vs['compound']
                db = (current_time,subreddit,title,body,author,sentiment)
                mycursor.execute(sqlFormula, db)
                mydb.commit()
                comment_count += 1
                print(comment_count)
    # Keep an exception so that in case of error you dont hit the api multiple times and also your code wont crash on the vm
    except Exception as e:
        print('Exception')
        print(str(e))
        time.sleep(10)
