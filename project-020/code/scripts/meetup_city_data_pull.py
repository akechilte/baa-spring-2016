from __future__ import unicode_literals
from datetime import datetime, timedelta

import requests
import json
import time
import codecs
import sys
import happybase

'''
Author : mbiswas
Reference: https://www.meetup.com/meetup_api/, https://happybase.readthedocs.io/en/latest/

'''

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
api_key = "779381934495d33c6f40555a8087754a"
city_url = "https://api.meetup.com//2/cities"
page = 200
offset = 0
city_table = "meetup_cities"
localhost = 'xxx.xxx.xxx.xxx'
REQUEST_LATENCY=0.2


def get_results(url,params):
    request = requests.get(url, params=params)
    limit = request.headers['x-ratelimit-reset']
    if limit == '2':
        time.sleep(10)
    data = request.json()
    _update_rate_limit(request.headers)
    return data

def _wait_for_rate_limit(next_req_time):
    now = datetime.now()
    if next_req_time > now:
        t = next_req_time - now
        time.sleep(t.total_seconds())


def _update_rate_limit(hdr):
    remaining = float(hdr['x-ratelimit-remaining'])
    reset = float(hdr['x-ratelimit-reset'])
    spacing = reset / (1.0 + remaining)
    delay = spacing - REQUEST_LATENCY
    next_req_time = datetime.now() + timedelta(seconds=delay)
    _wait_for_rate_limit(next_req_time)



def get_cities(country, state):
    per_page = page
    city_offset = offset
    connection = happybase.Connection(localhost)
    table = connection.table(city_table)
    flag = "0"
    results_we_got = per_page
    while (results_we_got == per_page):
        response = get_results(city_url,
                               {"sign": "true", "country": country, "key": api_key,
                                "page": per_page, "offset": city_offset})
        city_offset += 1
        results_we_got = response['meta']['count']
        for city in response['results']:
            if country == 'US':
                table.put(str(city['id']), {'city_details:city_name': city['city'],
                                            'city_details:country': city['country'],
                                            'city_details:lat': str(city['lat']),
                                            'city_details:lon': str(city['lon']),
                                            'city_details:member_count': str(city['member_count']),
                                            'city_details:rank': str(city['ranking']),
                                            'city_details:state': city['state'],
                                            'city_details:zip': city['zip'],
                                            'city_details:processed': flag})
            else:
                # For India, there is no "state" from response
                table.put(str(city['id']), {'city_details:city_name': city['city'],
                                            'city_details:country': city['country'],
                                            'city_details:lat': str(city['lat']),
                                            'city_details:lon': str(city['lon']),
                                            'city_details:member_count': str(city['member_count']),
                                            'city_details:rank': str(city['ranking']),
                                            'city_details:zip': city['zip'],
                                            'city_details:processed': flag})




def main():
    country = sys.argv[1]
    get_cities(country)



if __name__ == "__main__":
    main()