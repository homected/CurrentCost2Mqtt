![currentcost logo](logo.png)
# CurrentCost2Mqtt
A gateway to publish [Current Cost](http://www.currentcost.com) energy monitor values to a MQTT broker.

## Credits
First of all I have to say Thanks to [lolouk44](https://github.com/lolouk44) and [Robin Wilson](http://blog.rtwilson.com/how-to-log-electricity-usage-from-a-currentcost-envir-part-1/) for the code my program is based on.

## Introduction
At first time I used the [lolouk44 home assistant custom component](https://github.com/lolouk44/CurrentCost_HA_CC) to integrate my [Current Cost Envi](http://www.currentcost.com/product-envi.html) energy monitor in [home assistant](https://www.home-assistant.io/) but I had some issues when I restart Home Assistant and I had to restart it several times until the energy values are correctly showed. Appart of it I have interest to move the Envi far from the server where Home Assistant runs so I started to look for other possibilities. In any case thanks to lolouk44 for the great support he given me.

My home automation system is mainly based on [ZWave](https://z-wavealliance.org/) technology and recently I moved from the ZWave integration of Home Assistant to a [Zwave to MQTT](https://github.com/OpenZWave/Zwave2Mqtt) gateway running on a [Raspberry Pi](https://www.raspberrypi.org/). It allows me to improve the performance of the ZWave network because I moved my Zwave stick to a better location, so I started thinking to move the Current Cost monitor to the Raspberry Pi and send its values through the MQTT broker.

And finally, here is the code and the instructions to setup a Current Cost to MQTT gateway and how to get the values in Home Assistant.
