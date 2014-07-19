import requests
import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute("CREATE TABLE tides(time,prediction,measurment,f,s,q)")

def set_querry(product='',date='',begin_date='',end_date='',range='',
               station='8545240',datum='mlw',units='english',tz='gmt',
               app='phillyrd.org',format='json'):
    '''
    returns a dictionary of parameters formated for calling noaa api.
    takes product 'water_level' or 'predictions'
    takes either date of 'latest' or 'today' or begin and end dates
    inputs are not sanitized
    '''
    params = {
        'station':station,
        'product':product,
        'datum':datum,
        'units':units,
        'time_zone':tz,
        'application':app,
        'format':format}

    if date != '' and (begin_date != '' or end_date != ''):
        # something is wrong
        return False

    elif date == 'latest' or date == 'today':
        params['date'] = date
        return params

    elif begin_date != '' and end_date != '' and range == '':
        params['begin_date'] = begin_date
        params['end_date'] = end_date
        return params

    elif range != '' and (begin_date != '' or end_date != '') and (begin_date == '' or end_date == ""):
        # implement date + range selection
        return True 

    else:
        return False


api_url = 'http://tidesandcurrents.noaa.gov/api/datagetter'  

def querry_api(params):
    return requests.get(api_url,params=params).json()

def enroll_data(formatted_data,cursor,connection):
    '''
    takes a list of pre-formated tuples of data and inserts each tuple in sequence into our db
    returns nothing
    '''
    for i in range(len(formatted_data)):
        cursor.execute("INSERT INTO tides VALUES (?,?,?,?,?,?)",formatted_data[i])
    connection.commit()

def format_data(api_dict):
    '''
    take raw api return and format for storage in our db
    input is dictionary with keys 'data' and 'metadata'
    value for key 'data' is a list containing one or more dictionaries
    each of these 'data' dictionaries represent one data point
    we convert each data point into a tuple and return a list of tuples.
    '''
    formatted_data = []
    for i in range(len(api_dict[u'data'])):
        formatted_data.append(tuple([api_dict[u'data'][i][u't'],
                                                           u'',
                                    api_dict[u'data'][i][u'v'],
                                    api_dict[u'data'][i][u'f'],
                                    api_dict[u'data'][i][u's'],
                                    api_dict[u'data'][i][u'q']
                                                             ]))
    return formatted_data

def extract_data(cur):
    '''this dumps all rows.  may not be practicle for production use but useful for testing.'''
    cur.execute("SELECT * FROM tides")
    return cur.fetchall()

def get_and_store():
    '''get measurements for today and insert into db.  mostly for convinience of manual testing'''
    enroll_data(format_data(querry_api(set_querry('water_level','today'))),cur,conn)
