# Import package
import RPi.GPIO as GPIO
import time
import os, json
import uuid
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

# Define Variables
MQTT_HOST = "ec2-34-208-211-241.us-west-2.compute.amazonaws.com"
MQTT_PORT = 1883
#MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "IOT"
#MQTT_MSG = "hello MQTT"

# Initiate MQTT Client
mqttc = mqtt.Client()

# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, rc):
    print "In Connect..subscribing.."
    mosq.subscribe(MQTT_TOPIC)
    print "Successful.."

# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
    print "Topic: " + str(msg.topic)
	print "QoS: " + str(msg.qos)
	print "Payload: " + str(msg.payload)
	command = str(msg.payload)
	if command == "On":
	    GPIO.output(17, True)
    elif command == "Off":
        GPIO.output(17, False)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + 
	MQTT_TOPIC + " with QoS: " + str(granted_qos))
		
# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe

# mqttc.connect(MQTT_HOST, MQTT_PORT)

# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
