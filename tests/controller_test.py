import unittest
from data import dao
from controllers import Controller

class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.arduinoEndpoint = dao.ArduinoEndpoint('Arduino Uno Endpoint')
        self.controller = Controller(arduinoEndpoint=self.arduinoEndpoint)

    def testAverageGenerator(self):
        averager = self.controller.averageGen()
        next(averager)
        testVals = [23, 23434, 45,2 ,424,245,6 ,646,346,25,77,34246,73,6]
        for i in testVals:
            avg = averager.send(i)
            print(avg)

    def testOutStream(self):
        self.controller.readArduinoStream()


if __name__ == '__main__':
    ctrlTest = ControllerTest()
    ctrlTest.setUp()
    ctrlTest.testAverageGenerator()
    ctrlTest.testOutStream()

