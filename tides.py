import requests
import sqlite3
import datetime

def initiate_db():
    connection = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE tides(time timestamp PRIMARY KEY,prediction number ,measurment number,f,s,q)")
    cursor.execute("CREATE INDEX index_tides ON tides (time);")
    cursor.execute("CREATE INDEX index_tides2 ON tides (q);")
    return connection, cursor

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

    elif date == 'latest' or date == 'today' or date == 'recent':
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

def enroll_data(formatted_data,connection,cursor):
    '''
    takes a list of pre-formated tuples of data and inserts each tuple in sequence into our db
    returns nothing
    '''
    # this works but is much slower than for loop? at least for recent querry with ~720 records.
    # cursor.executemany("INSERT INTO tides VALUES (?,?,?,?,?,?)",formatted_data)

    for i in range(len(formatted_data)):
        cursor.execute("INSERT INTO tides VALUES (?,?,?,?,?,?)",formatted_data[i])
    connection.commit()


def format_data(api_dict):
    '''
    take raw api return and format for storage in our db
    input is dictionary with keys 'data' and 'metadata'.  we are only interested in 'data'
    value for key 'data' is a list containing one or more dictionaries, each of these 'data' dictionaries represent one data point
    we convert each data point into a tuple and return a list of tuples. some fields undergo type manipulations.
    '''
    datetime_format = "%Y-%m-%d %H:%M"
    formatted_data = []
    for i in range(len(api_dict[u'data'])):

        list_key = api_dict[u'data'][i]

        timestamp = datetime.datetime.strptime(list_key[u't'],datetime_format)
        prediction = None
        value = float(list_key[u'v'])
        f = list_key[u'f']
        s = float(list_key[u's'])
        q = list_key[u'q']

        formatted_data.append(tuple([timestamp,prediction,value,f,s,q]))

    return formatted_data

def extract_all_data(cursor):
    '''this dumps all rows.  may not be practicle for production use but useful for testing.'''
    cursor.execute("SELECT * FROM tides")
    return cursor.fetchall()

def get_and_store(connection,cursor):
    '''
    get measurements for today and insert into db.
    '''
    parameters = set_querry('water_level','recent')
    api_data = querry_api(parameters)
    formatted_data = format_data(api_data)
    enroll_data(formatted_data,connection,cursor)

    '''
    can also be stated as:
    enroll_data(format_data(querry_api(set_querry('water_level','today'))),con,cur)
    '''
