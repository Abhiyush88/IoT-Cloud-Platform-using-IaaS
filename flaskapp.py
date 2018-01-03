from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import MySQLdb
import logging

app = Flask(__name__)

db = MySQLdb.connect("localhost", "root", "lab4", "RaspberryIOT")

MQTT_HOST = "ec2-34-208-211-241.us-west-2.compute.amazonaws.com"
MQTT_PORT = 1883
MQTT_TOPIC = "IOT"
#MQTT_MSG = "hello MQTT"

#logging.basicConfig(filename='events.log', level=logging.DEBUG)

@app.route('/')
def login():
  #logging.basicConfig(filename='events.log', level=logging.DEBUG)
  logging.info('User is trying to login')
  return render_template('Login.html')

@app.route('/showSignup')
def showSignup():
  #logging.info('User is not registered. Wants to signup..')
  return render_template('signup.html')

@app.route('/welcome')
def welcome():
  return render_template('welcome.html')

@app.route('/viewDevice', methods=['GET', 'POST'])
def viewDevice():
  url = request.referrer

  if 'showSignup' in url:
    try:
	global uName
        fName = request.form['inputFName']
        lName = request.form['inputLName']
        eMail = request.form['inputEmail']
        uName = request.form['inputUName']
        pswd = request.form['inputPassword']
        curs=db.cursor()
        results = curs.execute("SELECT * FROM UserLogin WHERE userName = %s",[uName])
        if results>0:
	   #logging.info('User already exists..')
           return render_template('signup.html')
        else:
           curs.execute("""INSERT INTO UserSignup VALUES (%s,%s,%s,%s,%s)""",(fName,lName,eMail,uName,pswd))
	   curs.execute("""INSERT INTO UserLogin VALUES (%s,%s)""",(uName,pswd))
           db.commit()
           #logging.info('User %s added succesfully', uName)
           return manageDevice(uName)
    except Exception as e:
      #logging.warning('Caught in exception %s', str(e))
      return("catch 1"+str(e))

  else:
    try:
	global uName
        uName = request.form['inputUName']
        pswd = request.form['inputPassword']
        curs = db.cursor()
        results = curs.execute("SELECT * FROM UserLogin WHERE userName = %s AND password = %s",[uName,pswd])
        # curs.execute("INSERT into UserLogin values(%s,%s)",(uName,pswd))
        if results == 1:
           #logging.info('User logged in successfully..Can manage its devices..')
           return manageDevice(uName)
        else:
          # tkMessageBox.showwarning('alert title', 'Bad things happened!')
	   #logging.warning('Login unsuccessful..Try to login with correct credentials.')
           return render_template('Login.html')
    except Exception as e:
        #logging.warning('Caught in exception %s', str(e))
        return("catch 2" + str(e))

def manageDevice(username):
    global uName
    uName = username
    curs = db.cursor()
    curs.execute("SELECT * FROM AddDevice Where userName = %s",[username])
    #return jsonify(data=curs.fetchall())
    items = [dict(Device_Id=row[0],Device_Type=row[1],Date_Time=row[2],userName=row[3]) for row in curs.fetchall()]
   # items = curs.fetchall()
   # logging.info('Device list for the user %s',username)
    return render_template('viewDevices.html', items=items)

@app.route('/AddOrDeleteDevice', methods=['GET', 'POST'])
def AddOrDeleteDevice():
  try:
    curs = db.cursor()
    global deviceId
    deviceId = request.form['deviceId']
    option = request.form['action']
    row_results=curs.execute("SELECT * FROM AddDevice WHERE userName=%s AND Device_Id=%s",[uName,deviceId])
    if option == 'Add Device':
       try:
           curs.execute("""INSERT INTO AddDevice (Device_Id,userName) VALUES(%s,%s)""",(deviceId,uName))
           db.commit()
           return manageDevice(uName)
       except Exception as e:
          return("catch 2" + str(e))
    elif option == 'Delete Device':
       if row_results>0:
          try:
             curs.execute("DELETE FROM AddDevice WHERE Device_Id=%s",[deviceId])
	     db.commit()
             return manageDevice(uName)
	  except Exception as e:
             return("catch 3" + str(e))
    elif option == 'Operate Device':
       if row_results>0:
          return render_template('operateDevice.html')
    else:
       try:
          return render_template('addDevice.html')
       except Exception as e:
          return("catch 4" + str(e))
  except Exception as e:
        return("catch 1" + str(e))

@app.route('/operateDevice')
def operateDevice():
    if request.form['submit'] == 'On':
       mqttc = mqtt.Client()
       mqttc.connect(MQTT_HOST, MQTT_PORT)
       mqttc.publish(MQTT_TOPIC, 'On')
       return render_template('operateDevice.html', status='On')
    elif request.form['submit'] == 'Off':
       mqttc = mqtt.Client()
       mqttc.connect(MQTT_HOST, MQTT_PORT)
       mqttc.publish(MQTT_TOPIC, 'Off')
       return render_template('operateDevice.html', status='Off')
    else:
       return render_template('operateDevice.html', status='error')
    
@app.route('/addDevice')
def addDevice():
    return render_template('addDevice.html')

if __name__ == '__main__':
  app.run()

