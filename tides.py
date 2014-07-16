import requests

api_querry = {
    'date':'latest',
    'station':'8545240',
    'product':'water_level',
    'datum':'mlw',
    'units':'english',
    'time_zone':'gmt',
    'application':'phillyrd.org',
    'format':'json'
    }

api_url = 'http://tidesandcurrents.noaa.gov/api/datagetter'  

def querry_api():
    data = requests.get(api_url,params=api_querry)
    return data.json()

def unpack_latest(api_data):
    # latest data from noaa should be a dictionary with keys 'data' and 'metadata'.
    # data value is a list with one item which is another dictionary with unicode values.
    # for now we're only interested in t and v keys which are the timestamp and the tide height.
    return tuple([str( api_data[u'data'][0][u't']),float( api_data[u'data'][0][u'v'])])
