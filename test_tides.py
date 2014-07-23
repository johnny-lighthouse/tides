import unittest
import tides
import inspect
import sqlite3
import datetime

valid_api_data = {u'data': [{u'q': u'p', u's': u'0.013', u'f': u'1,0,0,0', u't': u'2014-07-17 22:12', u'v': u'6.575'}
                           ,{u'q': u'p', u's': u'0.020', u'f': u'1,0,0,0', u't': u'2014-07-17 23:18', u'v': u'6.611'}],
               u'metadata': {u'lat': u'39.9333', u'lon': u'-75.1417', u'id': u'8545240', u'name': u'Philadelphia'}}

bad_s_data = {u'data': [{u'q': u'p', u's': u'0.013', u'f': u'1,0,0,0', u't': u'2014-07-17 22:12', u'v': u'6.575'}
                       ,{u'q': u'p', u's': u'', u'f': u'1,0,0,0', u't': u'2014-07-17 23:18', u'v': u'6.611'}],
           u'metadata': {u'lat': u'39.9333', u'lon': u'-75.1417', u'id': u'8545240', u'name': u'Philadelphia'}}


valid_formated_data = [(datetime.datetime(2014, 7, 17, 22, 12), None, 6.575, u'1,0,0,0', 0.013, u'p'),
                       (datetime.datetime(2014, 7, 17, 23, 18), None, 6.611, u'1,0,0,0', 0.02, u'p')]


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
        self.assertIs(type(tides.format_data(bad_s_data)[1][4]),type(None))

class Test_storage(unittest.TestCase):

    def setUp(self):
        sql_create = "CREATE TABLE tides(time timestamp PRIMARY KEY,prediction number ,measurement number,f,s number,q)"
        self.conn = sqlite3.connect(':memory:',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()
        self.cur.execute(sql_create)
        pass

    def test_initiate_db(self):
        a,b = tides.initiate_db()
        self.assertIs(type(a),tides.sqlite3.Connection)
        self.assertIs(type(b),tides.sqlite3.Cursor)

    def test_enroll(self):
        self.assertTrue(inspect.isfunction(tides.enroll_data))
        tides.enroll_data(valid_formated_data,self.conn,self.cur)
        self.assertEqual(tides.extract_all_data(self.cur),valid_formated_data)

if __name__ == '__main__':
    unittest.main()
