from flask import Flask, request, jsonify
import json
import requests
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'carson.tennis.tracker@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = 'carson.tennis.tracker@gmail.com'

scheduler = BackgroundScheduler()
scheduler.start()

mail = Mail(app)

def check_for_opening():
  # see: https://classes.cornell.edu/content/FA25/api-details
  url = "https://classes.cornell.edu/api/2.0/search/classes.json"
  # PE1446 11:30 
  classNbr = 10155
  params = {
      'roster': 'FA25',
      'subject': 'PE'
  }

  try:
    response = requests.get(url, params=params)
    data = response.json()
    all_classes = data.get('data', {}).get('classes', [])
        
    tennis_data = None
    for cls in all_classes:
      for enrollGroup in cls.get('enrollGroups', []):
        for classSection in enrollGroup.get('classSections', []):
                if classSection.get('classNbr') == classNbr:
                  tennis_data = classSection
                  break
    if tennis_data: 
      if tennis_data["openStatus"] == "O":
        send_open_notif()
  except Exception as e:
    raise e



def send_open_notif():
   pass

def create_app():
   return app

if __name__ =='__main__':
   app = create_app()
   with app.app_context():
      check_for_opening()
      app.run(port=3000)