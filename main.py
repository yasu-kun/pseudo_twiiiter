from flask import Flask, render_template, request 
from flask_ngrok import run_with_ngrok
import sqlite3
from datetime import datetime, timedelta, timezone


app = Flask(__name__)
run_with_ngrok(app)

@app.route('/', methods=['GET'])
def tweet_get():
  #return 'Hello World!'
  #data=zip(tweet_list,date_list)
  con = sqlite3.connect('twitter_database.db') 
  cur = con.cursor()                                                                                                                      
  cur.execute('SELECT user_name,user_id,tweet,tweet_time,num_of_reply,num_of_retweet,num_of_heart FROM tweet_table')
  out = cur.fetchall()
  out.reverse()
  con.commit()                                                                                                                               
  con.close()

  return render_template('index.html',data=out, method='get')


@app.route('/', methods=['POST'])
def tweet_post():
  tweet = request.form['tweet']
  dt_utc = datetime.now(timezone.utc)

  # UTC -> JST
  #JST = timezone(timedelta(hours=+9))
  jst = dt_utc.astimezone(timezone(timedelta(hours=+9)))
  tweet_time = jst.strftime('%Y/%m/%d %H:%M:%S')

  user_name = 'default_user_name'
  user_id = 'default_user_id'
  
  con = sqlite3.connect('twitter_database.db') 
  cur = con.cursor()                                                                                                                   
  cur.execute("INSERT into tweet_table (user_name, user_id, tweet, tweet_time) VALUES ('%s', '%s', '%s', '%s')" % (user_name, user_id, tweet, tweet_time))

  cur.execute('SELECT user_name, user_id, tweet, tweet_time FROM tweet_table')
  out = cur.fetchall()
  out.reverse()

  con.commit()                                                                                                                               
  con.close()

  return render_template('index.html',data=out, method='post')

if __name__ == '__main__':
  app.run()
