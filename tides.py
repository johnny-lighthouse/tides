import requests

def set_querry(product,date,station='8545240',datum='mlw',units='english',tz='gmt',app='phillyrd.org',format='json'):
    '''returns a dictionary suitable for calling api.
    takes product type 'water_level' or 'predictions'
    takes date of 'latest' or 'today' '''

    if date == 'latest' or date == 'today':
        return {
        'date':date,
        'station':station,
        'product':product,
        'datum':datum,
        'units':units,
        'time_zone':tz,
        'application':app,
        'format':format
            }

api_url = 'http://tidesandcurrents.noaa.gov/api/datagetter'  

def querry_api(params):
    return requests.get(api_url,params=params).json()

def unpack_latest(api_data):
    # latest data from noaa should be a dictionary with keys 'data' and 'metadata'.
    # data value is a list with one item which is another dictionary with unicode values.
    # for now we're only interested in t and v keys which are the timestamp and the tide height.
    return tuple([str( api_data[u'data'][0][u't']),float( api_data[u'data'][0][u'v'])])


