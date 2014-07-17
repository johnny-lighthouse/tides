import requests

def set_querry(product='',date='',begin_date='',end_date='',range='',
               station='8545240',datum='mlw',units='english',tz='gmt',
               app='phillyrd.org',format='json'):

    '''returns a dictionary of parameters formated for calling api.
    takes product 'water_level' or 'predictions'
    takes date of 'latest' or 'today'
    inputs are not sanitized '''

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

def unpack_latest(api_data):
    # latest data from noaa should be a dictionary with keys 'data' and 'metadata'.
    # data value is a list with one item which is another dictionary with unicode values.
    # for now we're only interested in t and v keys which are the timestamp and the tide height.
    return tuple([str( api_data[u'data'][0][u't']),float( api_data[u'data'][0][u'v'])])


