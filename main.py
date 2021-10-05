from flask import Flask, render_template, request 
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def hello():
  #return 'Hello World!'
  return render_template('index.html')

if __name__ == '__main__':
  app.run()
