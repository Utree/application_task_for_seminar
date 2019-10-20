import requests
import urllib.error
import urllib.request
import json


def search_local(lat, lon):
    baseurl = 'https://map.yahooapis.jp/search/local/V1/localSearch'
    params = {
        'appid': 'dj00aiZpPUxkZnlIN0YwM3dZNSZzPWNvbnN1bWVyc2VjcmV0Jng9MmU-',
        'output': 'json',
        'sort': 'score',
        'start': 1,
        'results': '20',
        'lat': str(lat),
        'lon': str(lon),
        'dist': 1,
    }
    url = '{}?{}'.format(baseurl, urllib.parse.urlencode(params))
    res = requests.get(url)
    result = []
    ydf = json.loads(res.text)
    search_result = []

    features = ydf['Feature']
    if ydf['ResultInfo']['Count']:
        total = ydf['ResultInfo']['Total']

        for f in features:
            if f['Geometry']['Type'] == 'point':
                ll = f['Geometry']['Coordinates'].split(',')
                poi = {
                    'uid': f['Property']['Uid'],
                    'name': f['Name'],
                    'station': f['Property']['Station'],
                    'lat': ll[1],
                    'lon': ll[0]
                }
                result.append(poi)

        for i, poi in enumerate(result, 1):
            search_result.append(
                '{uid},{name},{lon},{lat}'.format(
                    name=poi['name'],
                    uid=poi['uid'],
                    lon=poi['lon'],
                    lat=poi['lat']
                )
            )
    return search_result