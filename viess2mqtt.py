import time
import datetime
import telnetlib
import re
import paho.mqtt.client as mqtt


class vclient(object):
    '''vcontrol client'''
    def __init__(self, host, port):
        self.telnet_client = telnetlib.Telnet(host, port)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOST, 1883, 60)

    def publish(self, cmd):
        '''Query & Publish'''
        if cmd == 'timestamp':
            timestamp = int(time.mktime(datetime.datetime.now().timetuple())) #unix time
            self.mqtt_client.publish('/vito/' + cmd, payload=timestamp, qos=0, retain=False)	    
        else:
            self.telnet_client.read_until("vctrld>")
            self.telnet_client.write(cmd + '\n')
            out = self.telnet_client.read_until('Degrees Celsius')
            search = re.search(r'[0-9]*\.?[0-9]+', out)
            # return search.group(0)
            self.mqtt_client.publish('/vito/' + cmd, payload=round(float(search.group(0)),2), 
qos=0, 
retain=False)


HOST = '192.168.88.3' # vcontrold telnet host
PORT = '3002' # vcontrold port

vals = ['timestamp', 'getOutsideTemp', 'getBoilerTemp', 'getWaterTemp']

vc = vclient(HOST, PORT)

for v in vals:
    vc.publish(v)
