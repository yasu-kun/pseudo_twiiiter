from flask import Flask, render_template, request 
from flask_ngrok import run_with_ngrok
import sqlite3

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def hello():
  #return 'Hello World!'
  #data=zip(tweet_list,date_list)
  con = sqlite3.connect('data.db') 
  cur = con.cursor()                                                                                                                      
  cur.execute('SELECT * FROM tweet_table')
  out = cur.fetchall()

  con.commit()                                                                                                                               
  con.close()

  return render_template('index.html',data=out)

if __name__ == '__main__':
  app.run()
