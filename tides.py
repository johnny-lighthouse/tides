import requests

url = 'http://tidesandcurrents.noaa.gov/api/datagetter?date=latest&station=8545240&product=water_level&datum=mlw&units=english&time_zone=gmt&application=phillyrd.org&format=json'

def get_data():
    data = requests.get(url)
    unpack = data.json()
    #unpack is a dictionary with keys data and metadata. data value is a list with one index which is another dictionary with unicode values.
    #we're only interested in t and v keys which are the timestamp and the tide height.
    return tuple([str(unpack[u'data'][0][u't']),float(unpack[u'data'][0][u'v'])])
