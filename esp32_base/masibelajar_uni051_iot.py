import time
from machine import Pin
import dht
from umqtt.simple import MQTTClient
import ujson
import network
import urequests as requests

# Definisi
class DHT11:
    def __init__(self, pin, time_debounce = 5):
        self.pin = pin
        self._sensor = dht.DHT11(pin)
        self.temperature = None
        self.humidity = None
        self.last_used = time.time() + 5
        self.time_debounce = time_debounce
        
        
    def debounce(self, time_debounce = None):
        time_debounce = time_debounce if time_debounce is not None else self.time_debounce
        now = time.time()
        return now - self.last_used < time_debounce
    
            
    def update(self):
        self.temperature = self._sensor.temperature()
        self.humidity = self._sensor.humidity()
    
    
    def measure(self):
        if self.debounce():
            return False
        
        self._sensor.measure()
        self.last_used = time.time()
        return True
        
        
    def isStatusDifferent(self):
        temperature = self._sensor.temperature()
        humidity = self._sensor.humidity()
        
        return temperature != self.temperature or humidity != self.humidity
        
        
    def overview(self):
        return f"Temperature : {self.temperature}, Humidity : {self.humidity}"
    


class LED:
    def __init__(self, pin):
        self.pin = pin
        
        
    def on(self):
        self.pin.value(1)
        
        
    def off(self):
        self.pin.value(0)
        

pir_led = LED(Pin(5, Pin.OUT))
dht11 = DHT11(Pin(13, Pin.IN), 10)

DEVICE_ID = "m-security"

WIFI_SSID = "ES"
WIFI_PASSWORD = "00011000"

UBIDOTS_TOKEN = "BBUS-kiWazp9NWTu1392oaOpNPKF6YzaDJW"

# Connection
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting")
    time.sleep(0.1)
print("WiFi Connected!")
print(wifi_client.ifconfig())

# Func
def push_to_ubidots(data):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    
    try:
        response = requests.post(url, json=data, headers=headers)
    except Exception as e:
        print("Push To Ubidots Error", e)
    else:
        print("Data terkirim ke Ubidots!")
        print("[Ubidots] Response:", response.text)
        
    


# Loop utama
while True:
    # DHT11
    try:
        if dht11.measure() and dht11.isStatusDifferent():
            dht11.update()
            print(dht11.overview())
            
            data = {
                "temperature" : dht11.temperature,
                "humidity" : dht11.humidity
            }
            push_to_ubidots(data)
    except Exception as e:
        print("Error : DHT11", e, dht11.last_used, time.time())

    # Tunggu sebentar sebelum membaca lagi
    time.sleep(1)


