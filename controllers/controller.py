import json
from data import SensorOutputModel

class Controller(object):
    def __init__(self, arduinoEndpoint=None, userEndpoint=None):
        self._arduino = arduinoEndpoint
        self._usr = userEndpoint
        self._sensorData = SensorOutputModel()
        self._avgGenList = [self.averageGen() for i in range(0, 5)]   # a list of generator functions for running averages
        for g in self._avgGenList: next(g)                          # must call next() before usage

    def openArduinoConnection(self):
        self._arduino.openPort()

    def closeArduinoConnection(self):
        self._arduino.closePort()

    def readArduinoStream(self):
        ''' reads a stream of json data incoming from the arduino's attached sensors; into the sensor model.'''
        for x in self._arduino.serialOut():
            try:
                data = json.loads(x)
                self.__updateSensorData(data)
                print(self._sensorData)
            except json.decoder.JSONDecodeError:
                print('\n')

    def averageGen(self):
        '''generates a running average given a value through .send()'''
        total = avg = count = 0
        while True:
            val = yield avg
            total += val
            count += 1
            avg = total / count

    def getAvgTemp(self, scale=None):
        if scale:
            scale = scale.lower()
            if scale == 'c':
                return self._sensorData.temperature['c']
            if scale == 'f':
                return self._sensorData.temperature['f']
            if scale == 'k':
                return self._sensorData.temperature['k']

    def getAvgIllum(self):
        return self._sensorData.illuminance

    def getAvgSoilMoisture(self):
        return self._sensorData.soilMoisture

    def __updateSensorData(self, data):
        ''' updates the sensor model with generated running averages of each value. '''
        self._sensorData.temperature['c'] = round(self._avgGenList[0].send(data['temperature']['c']), 2)
        self._sensorData.temperature['f'] = round(self._avgGenList[1].send(data['temperature']['f']), 2)
        self._sensorData.temperature['k'] = round(self._avgGenList[2].send(data['temperature']['k']), 2)
        self._sensorData.illuminance = round(self._avgGenList[3].send(data['light_level']), 2)
        self._sensorData.soilMoisture = round(self._avgGenList[4].send(data['soil_moisture']), 2)
