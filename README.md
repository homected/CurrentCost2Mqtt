![currentcost logo](logo.png)
# CurrentCost2Mqtt
A gateway to publish [Current Cost](http://www.currentcost.com) energy monitor values to a MQTT broker.

## Credits
First of all I have to say Thanks to [lolouk44](https://github.com/lolouk44) and [Robin Wilson](http://blog.rtwilson.com/how-to-log-electricity-usage-from-a-currentcost-envir-part-1/) for the code my program is based on.

## Introduction
At first time I used the [lolouk44 home assistant custom component](https://github.com/lolouk44/CurrentCost_HA_CC) to integrate my [Current Cost Envi](http://www.currentcost.com/product-envi.html) energy monitor in [home assistant](https://www.home-assistant.io/) but I had some issues when I restart Home Assistant and I had to restart it several times until the energy values are correctly showed. Appart of it I have interest to move the Envi far from the server where Home Assistant runs so I started to look for other possibilities. In any case thanks to lolouk44 for the great support he given me.

My home automation system is mainly based on [ZWave](https://z-wavealliance.org/) technology and recently I moved from the ZWave integration of Home Assistant to a [Zwave to MQTT](https://github.com/OpenZWave/Zwave2Mqtt) gateway running on a [Raspberry Pi](https://www.raspberrypi.org/). It allows me to improve the performance of the ZWave network because I moved my Zwave stick to a better location, so I started thinking to move the Current Cost monitor to the Raspberry Pi and send its values through the MQTT broker.

## Installation

### Raspberry Pi

1. First, update your distribution.

   ```sh
   sudo apt update
   sudo apt upgrade
   ```
   
2. Install Python pip and some dependencies.

   ```sh
   sudo apt install python3-pip
   pip3 install pyserial
   pip3 install untangle
   pip3 install paho-mqtt
   ```
 
3. Install git and clone the repository.

   ```sh
   sudo apt install git
   cd~
   git clone https://github.com/homected/CurrentCost2Mqtt.git currentcost2mqtt
   ```

## Configuration

1. Set your own configuration parameters editing the program file.

   ```sh
   cd currentcost2mqtt
   sudo nano currentcost2mqtt.py
   ```

  You have to replace the text between quotes with the correct values for your configuration:
  
  - **COM_PORT**: Something like /dev/ttyUSB0 or COM1 or /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0;
  - **MQTT_Host**: The IP Address of the MQTT broker;
  - **MQTT_Port**: Port of the MQTT broker, for example 1883;
  - **MQTT_User**: Username to authenticate into the MQTT broker;
  - **MQTT_Password**: Password to authenticate into the MQTT broker;
  - **MQTT_Topic**: The topic of the MQTT broker where publish the data;
  - **MQTT_QoS**: Quality of Service level (0, 1 or 2);
  - **MQTT_Retain**: True for retain MQTT messages of False for not retain;

  Save and close the file with: Control+O, Enter, Control+X
  
  
2. Optionally, you can set this program runs automatically when the raspberry boots with these commands:

   ```sh
   sudo cp currentcost2mqtt.service /lib/systemd/system/currentcost2mqtt.service
   sudo chmod 644 /lib/systemd/system/currentcost2mqtt.service
   sudo systemctl daemon-reload
   sudo systemctl enable currentcost2mqtt.service
   ```

## Run

1. For start manually the program you can use this command:

   ```sh
   python3 currentcost2mqtt.py
   ```

If you set the program to run after boots, reboot the raspberry with this command:

   ```sh
   sudo reboot
   ```
   
After boot, you can control the process with these commands:

   ```sh
   sudo systemctl start currentcost2mqtt
	 sudo systemctl status currentcost2mqtt
	 sudo systemctl stop currentcost2mqtt
   ```
