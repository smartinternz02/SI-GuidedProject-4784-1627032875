import wiotp.sdk.device
import time
import json
import random
import geocoder

myConfig = { 
    "identity": {
        "orgId": "x012hb",
        "typeId": "VITDevice",
        "deviceId":"500062"
    },
    "auth": {
        "token": "12345678"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']  

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()


while True:
    t=random.randint(90,110) #Body temperature in Fahrenheit
    p=random.randint(40,120) #Pulse rate in beats per minute
    #Blood pressure(systolic(s) & diastolic(d))-measured in mm Hg:
    d=random.randint(80,140)
    s1=random.randint(60,80) #systolic range for low Blood Pressure
    s2=random.randint(80,90) #systolic range for high Blood Pressure
    
    if (d<=120):
        s=s1
    if(d>=120):
        s=s2
    b = str(d) + "/" + str(s)    
    #Tracking current location (latitude & longitude) using geocoder:
    soldier=random.randint(1,10) #Just a random number for Soldier
    #g = geocoder.ip('me') #Location of the soldier when's he witihn the required area
    g = geocoder.ip('199.7.157.0') #Random location to consider Soldier is not in the required area
    name="Soldier" + str(soldier)
    la=(g.latlng[0]) #Latitude of soldier location
    lo=(g.latlng[1]) #Longitude of soldier location
    
    myData={'name':name,'temperature':t, 'pulserate':p,'bloodpressure':b ,'systolic':s,'diastolic':d, 'lat':la, 'lon':lo }
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(6)
client.disconnect()
