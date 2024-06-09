from flask import Flask, render_template
import subprocess
import os
import datetime
import time

HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

TV_PATH = '/path/to/tv/series'

proc = None
app = Flask(__name__)

def list(path):
    os.chdir(path)
    files = filter(os.path.isfile, os.listdir(path))
    return files

def startPlayer(cmd):
    global proc
    proc = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)

def sendKey(key):
   global proc
   if not proc is None:
      try:
         proc.stdin.write(key)
      except:
         print('exception')

@app.route('/')
def home():
   return render_template('main.html', list=list(TV_PATH))

@app.route('/play/<file>')
def play(file):
   if not file is None:
      print ('playing: ' + file)
      path = os.path.join(TV_PATH, file)
      print ('path: ' + path)
      if os.path.exists(path):
         cmd = 'omxplayer -o hdmi ' + '"' + path + '"'
         print ('cmd: ' + cmd)
         sendKey('q')
         startPlayer(cmd)
      else:
         print ('path ' + path + ' does not exist')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/stop')
def stop():
   sendKey('q')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/volume/increase')
def up():
   sendKey('+')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/volume/decrease')
def down():
   sendKey('-')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/audio/previous')
def previousAudioStream():
   sendKey('j')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/audio/next')
def nextAudioStream():
   sendKey('k')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/subtitle/previous')
def previousSubtitleStream():
   sendKey('n')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/subtitle/next')
def nextSubtitleStream():
   sendKey('m')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/subtitle/show')
def showSubtitles():
   sendKey('s')
   return render_template('main.html', list=list(TV_PATH))

@app.route('/subtitle/hide')
def hideSubtitles():
   sendKey('x')
   return render_template('main.html', list=list(TV_PATH))

if __name__ == '__main__':
   app.run(host=HOST, port=PORT, debug=DEBUG)
