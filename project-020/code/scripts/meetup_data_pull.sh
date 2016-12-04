#!/bin/bash
echo "Starting meetup_city_data_pull Script"
nohup python project-020/code/scripts/meetup_city_data_pull.py "US" &
nohup python project-020/code/scripts/meetup_city_data_pull.py "IN" &
# Pause for 2 mins to allow city data to be pulled, because Group pull script refers to the meetup_cities HBase table
sleep 120
echo "Starting meetup_city_data_pull Script"
nohup python project-020/code/scripts/meetup_group_data_pull.py &

#Sleep induced to allow some group data to be pulled before starting to fetch events data
sleep 120
nohup python project-020/code/scripts/meetup_event_data_pull.py &