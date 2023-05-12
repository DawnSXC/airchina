from django.test import TestCase

# Create your tests here.
import unittest
from requestTest import ReqTest



class TestMethod(unittest.TestCase):


    def setUp(self):
        self.run = ReqTest()
# test /findflight/
    #run normally
    def test_findflght(self):
        url = "http://127.0.0.1:8000/airchina/findflight"
        data={
            "arrival_airport":"Beijing Airport",
             "departure_airport":"HK Aiport",
              "date":"2023/05/01"
        }
        res = self.run.run_req(url, 'GET', data)
        print(res)
# missing arrival airport information
    def test_fingflight_missing_arrairport(self):
        url = "http://127.0.0.1:8000/airchina/findflight"
        data={

             "departure_airport":"HK Aiport",
              "date":"2023/05/01"
        }
        res = self.run.run_req(url, 'POST',data)
        print(res)

# missing depature airport information
    def test_fingflight_missing_depairport(self):
        url = "http://127.0.0.1:8000/airchina/findflight"
        data = {
            "arrival_airport": "Beijing Airport",
            "date": "2023/05/01"
        }
        res = self.run.run_req(url, 'POST', data)
        print(res)

# missing start date information
    def test_fingflight_missing_date(self):

        url = "http://127.0.0.1:8000/airchina/findflight"
        data = {
            "arrival_airport": "Beijing Airport",
            "departure_airport": "HK Aiport",
        }
        #res = self.run.run_req(url, 'POST', data)
        res = self.client.get('airlines/findflight/')
        print(res.status_code)

# Airport does not exist
    def test_findflght_wrongairport(self):
        url = "http://127.0.0.1:8000/airchina/findflight"
        data={
            "arrival_airport":"Airport not exit",
             "departure_airport":"HK Aiport",
            "date":"2023/05/01"
        }
        res = self.run.run_req(url, 'GET', data)
        print(res)
    def test_findflght_post(self):
        url = "http://127.0.0.1:8000/airchina/findflight"
        data={
            "arrival_airport":"Beijing Airport",
             "departure_airport":"HK Aiport",
              "date":"2023/05/01"
        }
        res = self.run.run_req(url, 'POST', data)
        print(res)


if __name__ == '__main__':
    unittest.main()