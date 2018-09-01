import unittest
from data import dao
import json

class ArduinoEndpointTest(unittest.TestCase):
    def setUp(self):
        self.arduinoEndpoint = dao.ArduinoEndpoint('Arduino Uno Endpoint')

    def printStats(self, data):
        print("Temperature: "+str(data['temperature'])+
            "\nsoil_moisture: "+str(data['soil_moisture'])+
            "\nlight_level: "+str(data['light_level']))

    def test_serialOut(self):
        for x in self.arduinoEndpoint.serialOut():
            d = dict()
            try:
                d = json.loads(x)
                self.printStats(d)
            except json.decoder.JSONDecodeError:
                print("\n")


    def test_openPort(self):
        isOpen = self.arduinoEndpoint.openPort()
        self.assertTrue(isOpen == True)
        self.assertTrue(isOpen is not False)


    def test_closePort(self):
        isClosed = self.arduinoEndpoint.closePort()
        self.assertTrue(isClosed == True)
        self.assertTrue(isClosed is not False)


if __name__ == '__main__':
    aTest = ArduinoEndpointTest()
    aTest.setUp()
    aTest.test_openPort()
    aTest.test_closePort()
    # aTest.test_serialOut()
    # aTest.test_openPort()
