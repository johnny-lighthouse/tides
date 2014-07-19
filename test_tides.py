import unittest
import tides
import inspect
import sqlite3

valid_api_data = {u'data': [{u'q': u'p', u's': u'0.013', u'f': u'1,0,0,0', u't': u'2014-07-17 22:12', u'v': u'6.575'}
                           ,{u'q': u'p', u's': u'0.020', u'f': u'1,0,0,0', u't': u'2014-07-17 23:18', u'v': u'6.611'}],
               u'metadata': {u'lat': u'39.9333', u'lon': u'-75.1417', u'id': u'8545240', u'name': u'Philadelphia'}}

valid_formated_data = [(u'2014-07-17 22:12', None, u'6.575', u'1,0,0,0', u'0.013', u'p'),
                       (u'2014-07-17 23:18', None, u'6.611', u'1,0,0,0', u'0.020', u'p')]

class Test_fetch(unittest.TestCase):

    def setUp(self):
        self.params = {'units': 'english', 'product': 'water_level', 'station': '8545240', 
                       'application': 'phillyrd.org', 'date': 'latest', 'format': 'json', 
                       'datum': 'mlw', 'time_zone': 'gmt'}
        self.valid_products = ['water_level','predictions']
        self.valid_dates = ['today','latest']
        pass


    def test_querry_latest(self):
        '''happy path with date parameter'''
        self.assertEqual(tides.set_querry('water_level','latest'),self.params)

    def test_date_and_begin_end(self):
        '''Cannot use date with begin_date or end_date'''
        self.assertFalse(tides.set_querry('water_level','latest','string'))
        self.assertFalse(tides.set_querry('water_level','today',end_date='string'))

    def test_begin_and_range(self):
        '''should return True for now as a stub'''
        self.assertTrue(tides.set_querry('water_level',begin_date='string',range='string'))

    def test_end_and_range(self):
        self.assertTrue(tides.set_querry('water_level',end_date='string',range='string'))

    def test_begin_end(self):
        self.param = tides.set_querry('water_level',begin_date='string',end_date='string')
        self.assertEqual(self.param['begin_date'],'string')
        self.assertNotIn('date',self.param.keys())
        self.assertNotIn('range',self.param.keys())

    def test_url(self):
        self.assertEqual(tides.api_url,'http://tidesandcurrents.noaa.gov/api/datagetter')

    def test_format_data(self):
        self.assertEqual(tides.format_data(valid_api_data),valid_formated_data)

class Test_storage(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE tides(time,prediction,measurment,f,s,q)")
        pass

    def test_conn(self):
        self.assertIs(type(tides.conn),tides.sqlite3.Connection)

    def test_cur(self):
        self.assertIs(type(tides.cur),tides.sqlite3.Cursor)

    def test_enroll(self):
        self.assertTrue(inspect.isfunction(tides.enroll_data))
        tides.enroll_data(valid_formated_data,self.cur,self.conn)
        self.assertEqual(tides.extract_all_data(self.cur),valid_formated_data)

if __name__ == '__main__':
    unittest.main()
