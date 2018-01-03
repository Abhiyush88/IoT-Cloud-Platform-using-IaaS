# Import package
import paho.mqtt.client as mqtt

# Define Variables
MQTT_HOST = "ec2-34-208-211-241.us-west-2.compute.amazonaws.com"
MQTT_PORT = 1883
#MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "topic"
MQTT_MSG = "hello MQTT"


print "Hello World"
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
        print "In on_message"
	print "Topic: " + str(msg.topic)
	print "QoS: " + str(msg.qos)
	print "Payload: " + str(msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + 
	MQTT_MSG + " with QoS: " + str(granted_qos))

# Initiate MQTT Client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
#
mqttc.connect("ec2-34-208-211-241.us-west-2.compute.amazonaws.com", 1883, keepalive=60)

# Connect with MQTT Broker
# mqttc.connect(MQTT_HOST, MQTT_PORT)

# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
