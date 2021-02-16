#!/usr/bin/python
# currentcost2mqtt.py

# there may be a few libraries that need installing. 
import untangle
import serial
import paho.mqtt.client as mqtt

COM_PORT = "INSERT_COM_PORT_HERE"			# Something like /dev/ttyUSB0 or COM1 or /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
MQTT_Host = "INSERT_BROKER_IP_HERE"			# IP Address of the MQTT broker
MQTT_Port = "INSERT_PORT_HERE"				# Port of the MQTT broker, for example 1883
MQTT_User = "INSERT_USERNAME_HERE"			# Username to authenticate into the MQTT broker
MQTT_Password = "INSERT_PASSWORD_HERE"			# Password to authenticate into the MQTT broker
MQTT_Topic = "INSERT_TOPIC_HERE"			# Topic for publish data
MQTT_QoS = 0						# Quality Of Service level (0, 1 or 2)
MQTT_Retain = True					# Retain flag (True or False)

def get_data(port=COM_PORT, verbose=False):
	# port: the port that the CurrentCost meter is attached to. Something like /dev/ttyUSB0 or COM1 or /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
	# Returns:
	# (temperature, sensorNumber, sensorType, sensorChannel, sensorValue), with sensor as the number of the interface a device is assigned to, temperature in degrees C, and value in Watts

	# Read serial data
	ser = serial.Serial(port, 57600)
	xmldata = ser.readline().decode('utf-8').strip()
	if verbose:
		print(xmldata)
	ser.close()

	# Ignore the message if it's not complete
	if (xmldata.find('<msg>') != 0):
		return [0, 0, 0, 0, 0]
	if (xmldata.find('</msg>') != (len(xmldata) - 6)):
		return [0, 0, 0, 0, 0]

	# Parse the message to xml object
	p = untangle.parse(xmldata)

	# Process the message
	if ('hist' in dir(p.msg)):
		# Ignore hist messages
		return [0, 0, 0, 0, 0]
	else:
		# Process real-time output
		if ('tmpr' in dir(p.msg)):
			temperature = float(p.msg.tmpr.cdata)
		elif ('tmprF' in dir(p.msg)):
			temperature =  (float(p.msg.tmprF.cdata) - 32) * 5/9
			temperature = round(temperature, 1)
		else:
			temperature = 0;
		sensorNumber = int(p.msg.sensor.cdata)
		sensorType = int(p.msg.type.cdata)			# 1 = Electricity; 2 =  Electricity meter; 3 =  Gas meter; 4 = Water meter
		if (sensorType == 1):
			# Process "Watt" sensors
			if ('ch3' in dir(p.msg)):
				sensorChannel = 3
				sensorValue = int(p.msg.ch3.watts.cdata)
			elif ('ch2' in dir(p.msg)):
				sensorChannel = 2
				sensorValue = int(p.msg.ch2.watts.cdata)
			elif ('ch1' in dir(p.msg)):
				sensorChannel = 1
				sensorValue = int(p.msg.ch1.watts.cdata)
			else:
				return [0, 0, 0, 0, 0]
			return [temperature, sensorNumber, sensorType, sensorChannel, sensorValue]
		elif ((sensorType == 2) | (sensorType == 3) | (sensorType == 4)):
			# Process "Meter Impulse" sensors
			if ('imp' in dir(p.msg)):
				impulseCount = int(p.msg.imp.cdata)
			else:
				impulseCount = 0
			if ('ipu' in dir(p.msg)):
				impulsesPerUnit = int(p.msg.ipu.cdata)
			else:
				impulsesPerUnit = 0
			return [temperature, sensorNumber, sensorType, impulseCount, impulsesPerUnit]
		else:
			return [temperature, sensorNumber, sensorType, 0, 0]


client = mqtt.Client("P1") # must be unique on MQTT network
client.username_pw_set(str(MQTT_User),str(MQTT_Password))
client.connect(MQTT_Host, port=int(MQTT_Port))
client.loop_start()

while(True):
	try:
		CCData = get_data()
		
		if not ((CCData[0] == 0) & (CCData[1] == 0) & (CCData[2] == 0) & (CCData[3] == 0) & (CCData[4] == 0)):
			
			# Temperature
			client.publish(MQTT_Topic + '/CurrentCost/Temperature', '{"state":"'+ str(CCData[0]) +'","unit_of_measurement":"°C"}', qos=MQTT_QoS, retain=MQTT_Retain)

			# "Watt" sensor
			if (CCData[2] == 1):
				if (CCData[1] == 0):
					# If channel #0 is total power
					print ("Temperature: " + str(CCData[0]) + " °C - Total power ch" + str(CCData[3]) + ": " + str(CCData[4]) + " W")
					client.publish(MQTT_Topic + '/CurrentCost/Power/Total/Ch' + str(CCData[3]), '{"state":"' + str(CCData[4]) + '","unit_of_measurement":"W"}', qos=MQTT_QoS, retain=MQTT_Retain)
				else:
					# Else is appliance power
					print ("Temperature: " + str(CCData[0]) + " °C - Appliance " + str(CCData[1]) + " ch" + str(CCData[3]) + ": " + str(CCData[4]) + " W")
					client.publish(MQTT_Topic + '/CurrentCost/Power/Appliance' + str(CCData[1]) + '/Ch' + str(CCData[3]), '{"state":"' + str(CCData[4]) + '","unit_of_measurement":"W"}', qos=MQTT_QoS, retain=MQTT_Retain)
			
			# "Impulse meter" sensor
			elif ((CCData[2] == 2) | (CCData[2] == 3) | (CCData[2] == 4)):
				print ("Temperature: " + str(CCData[0]) + " °C - Sensor " + str(CCData[1]) + " Impulse per unit: " + str(CCData[4]) + " - Impulse count: " + str(CCData[3]))
				client.publish(MQTT_Topic + '/CurrentCost/Meter/Sensor' + str(CCData[1]), '{"state":"' + str(CCData[3]) + '","Impulse_per_unit":' + str(CCData[4]) + '}', qos=MQTT_QoS, retain=MQTT_Retain)

	except:
		pass
