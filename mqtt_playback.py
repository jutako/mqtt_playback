#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

# To test this code:
# sudo apt install mosquitto-clients
# mosquitto_pub -h 'test.mosquitto.org' -t 'test/audio' -m 'star-wars-15.wav'

# import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
from playsound import playsound
import os


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #playsound(os.path.join(os.environ['HOME'],'Recordings','moikka.wav'))
    soundfile = os.path.join(os.path.dirname(__file__),'wav', msg.payload.decode("utf-8"))
    print(soundfile)
    playsound(soundfile)


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log

#ADAFRUIT_IO_USERNAME = ""
#ADAFRUIT_IO_KEY = ""
broker_address = "test.mosquitto.org"
pub_topic = "test/audio"

#mqttc.username_pw_set(ADAFRUIT_IO_USERNAME, password = ADAFRUIT_IO_KEY)
mqttc.connect(broker_address, port = 1883) #connect to broker
mqttc.subscribe(pub_topic, 0)

# mqttc.connect("m2m.eclipse.org", 1883, 60)
# mqttc.subscribe("$SYS/#", 0)

mqttc.loop_forever()
