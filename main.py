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
  con = sqlite3.connect('data.db') 
  cur = con.cursor()                                                                                                                      
  cur.execute('SELECT * FROM tweet_table')
  out = cur.fetchall()
  out.reverse()
  con.commit()                                                                                                                               
  con.close()

  return render_template('index.html',data=out)


@app.route('/', methods=['POST'])
def tweet_post():
  tweet = request.form['tweet']
  dt_utc = datetime.now(timezone.utc)

  # UTC -> JST
  #JST = timezone(timedelta(hours=+9))
  jst = dt_utc.astimezone(timezone(timedelta(hours=+9)))
  tweet_time = jst.strftime('%Y/%m/%d %H:%M:%S')
  
  con = sqlite3.connect('data.db') 
  cur = con.cursor()                                                                                                                   
  cur.execute("INSERT into tweet_table (tweet, tweet_time) VALUES ('%s', '%s')" % (tweet, tweet_time))

  cur.execute('SELECT * FROM tweet_table')
  out = cur.fetchall()
  out.reverse()

  con.commit()                                                                                                                               
  con.close()

  return render_template('index.html',data=out)

if __name__ == '__main__':
  app.run()
