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

# CategoryID 2 : Career and Business
# CategoryID 34 : Tech
categories = ["2","34"]
api_key = "779381934495d33c6f40555a8087754a#"
group_url = "http://api.meetup.com/2/groups"
page = 200
offset = 0
city_table = "meetup_cities"
group_table = "meetup_groups"
localhost = 'xxx.xxx.xxx.xx'
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




def get_groups():
    per_page = page
    group_offset = offset
    city_flag = "1"
    group_flag = "0"
    connection = happybase.Connection(localhost)
    city_con = connection.table(city_table)
    group_con = connection.table(group_table)
    # put a starting row_key from meetup_cities table
    row_key = b'11105'
    for i in range(10):
        for key, data in city_con.scan(row_start=row_key, limit=3000):
            country = data['city_details:country']
            state = data['city_details:state']
            temp = key
            processed = data['city_details:processed']
            if processed == '0':
                for (categoty) in categories:
                    results_we_got = per_page
                    while (results_we_got == per_page):
                        if country == 'us':
                            # For Country: US
                            response = get_results(group_url,
                                                   {"sign": "true", "country": country,
                                                    "city": data['city_details:city_name'],
                                                    "state": data['city_details:state'],
                                                    "key": api_key,
                                                    "page": per_page, "offset": group_offset,
                                                    "category_id": categoty})

                        else:
                            # For Country: India
                            response = get_results(group_url,
                                                   {"sign": "true", "country": country,
                                                    "city": data['city_details:city_name'],
                                                    "key": api_key,
                                                    "page": per_page, "offset": group_offset, "category_id": categoty})

                        group_offset += 1
                        results_we_got = response['meta']['count']
                        exception_count = 0
                        print results_we_got, key
                        for group in response['results']:
                            try:
                                desc = group['description'].encode('ascii', 'ignore').encode('utf8').replace('\n', ' ')
                            except Exception as e:
                                desc = 'Not Available'
                                exception_count += 1
                                pass

                            group_con.put(str(group['id']), {'group_details:grp_name': group['name'],
                                                             'group_details:rating': str(group['rating']),
                                                             'group_details:category': str(group['category']['id']),
                                                             'group_details:city': group['city'],
                                                             'group_details:create_date': str(group['created']),
                                                             'group_details:desc': desc,
                                                             'group_details:lat': str(group['lat']),
                                                             'group_details:lon': str(group['lon']),
                                                             'group_details:state': str(state),
                                                             'group_details:country': str(country),
                                                             'group_details:processed': str(group_flag)})


                            city_con.put(str(key), {'city_details:processed': str(city_flag)})
        row_key = temp.encode()





def main():
    get_groups()



if __name__ == "__main__":
    main()