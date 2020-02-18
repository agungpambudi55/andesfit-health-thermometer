import pygatt

import logging
logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

def handleData(handle, value):
    if len(value) == 6:
        temperatureHigh, temperatureLow = value[2] << 8, value[1] & 0xFF
        temperature = (temperatureHigh | temperatureLow) / 100
        temperature = str(round(temperature, 1))
        
        print('Temperature {} C'.format(temperature))

try:
    adapter = pygatt.GATTToolBackend(hci_device='hci0')
    adapter.start()

    for discover in adapter.scan(run_as_root=True, timeout=5):
        if discover['name'] == 'TEMP':
            print('Device found, try to connect with device')
            device = adapter.connect(discover['address'])
            print('Connected with device')
                            
            while True:
                device.subscribe('00002a1c-0000-1000-8000-00805f9b34fb', callback=handleData, indication=True)
                
except KeyboardInterrupt:
    print('Terminate')
except:
    print('Something went wrong with adapter')
finally:
    adapter.stop()