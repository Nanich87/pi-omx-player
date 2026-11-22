from flask import Flask, render_template, redirect, url_for
import subprocess
import os
import signal
import datetime
import time

HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

TV_PATH = '/path/to/tv/series'

proc = None
current = None
app = Flask(__name__)

def list(path):
    os.chdir(path)
    files = filter(os.path.isfile, os.listdir(path))
    return files

def isRunning():
   return proc is not None and proc.poll() is None

def startPlayer(path):
   global proc, current
   current = os.path.basename(path)
   proc = subprocess.Popen(['omxplayer', '-o', 'hdmi', path], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)

def stopPlayer():
   global proc, current
   current = None
   if proc is None:
      return
   if proc.poll() is None:
      sendKey('q')
      try:
         proc.wait(timeout=5)
      except subprocess.TimeoutExpired:
         try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=5)
         except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
               os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
               pass
            proc.wait()
   proc = None

def sendKey(key):
   if isRunning():
      try:
         proc.stdin.write(key.encode())
         proc.stdin.flush()
      except (BrokenPipeError, OSError) as e:
         print('sendKey failed: ' + str(e))

@app.route('/')
def home():
   return render_template('main.html', list=list(TV_PATH), current=current if isRunning() else None)

@app.route('/play/<file>')
def play(file):
   path = os.path.join(TV_PATH, file)
   if os.path.isfile(path):
      print('playing: ' + path)
      stopPlayer()
      startPlayer(path)
   else:
      print('path ' + path + ' does not exist')
   return redirect(url_for('home'))

@app.route('/stop')
def stop():
   stopPlayer()
   return redirect(url_for('home'))

@app.route('/volume/increase')
def up():
   sendKey('+')
   return redirect(url_for('home'))

@app.route('/volume/decrease')
def down():
   sendKey('-')
   return redirect(url_for('home'))

@app.route('/audio/previous')
def previousAudioStream():
   sendKey('j')
   return redirect(url_for('home'))

@app.route('/audio/next')
def nextAudioStream():
   sendKey('k')
   return redirect(url_for('home'))

@app.route('/subtitle/previous')
def previousSubtitleStream():
   sendKey('n')
   return redirect(url_for('home'))

@app.route('/subtitle/next')
def nextSubtitleStream():
   sendKey('m')
   return redirect(url_for('home'))

@app.route('/subtitle/show')
def showSubtitles():
   sendKey('s')
   return redirect(url_for('home'))

@app.route('/subtitle/hide')
def hideSubtitles():
   sendKey('x')
   return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(host=HOST, port=PORT, debug=DEBUG)
