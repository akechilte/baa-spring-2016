#!/bin/bash

####################################################################################################
#Creates required HBase and MySQL tables
####################################################################################################

#Create HBase meetup_cities table
create table 'meetup_cities', {NAME => 'city_details'} | hbase shell

#Create HBase meetup_groups table
create table 'meetup_groups', {NAME => 'group_details'} | hbase shell

#Create HBase meetup_events table
create table 'meetup_events', {NAME => 'event_details'} | hbase shell

#Create MYSQL table
$1=$uid
$2=$pwd
$3=$dbname

mysql -u $1 -p$2 << EOF

use projects;

CREATE TABLE meetup_insights (
	grp_id INT NOT NULL, 
	event_month INT NOT NULL, 
	event_year INT NOT NULL, 
	event_count INT, 
	total_yes_count DECIMAL(10,2), 
	total_attend_count DECIMAL(10,2), 
	avg_yes_count DECIMAL(10,2), 
	avg_attend_count DECIMAL(10,2), 
	last_event_dt CHAR(10), 
	name VARCHAR(100), 
	STATE VARCHAR(40), 
	Country VARCHAR(40), 
	PRIMARY KEY (grp_id,event_month,event_year,name)
);

CREATE table meetup_interest( 
	interest_id INT NOT NULL, 
	Interest_name CHAR(40), 
	interest_desc CHAR(100), 
	PRIMARY KEY (interest_id)
);

CREATE table group_interest_mapping( 
	grp_id INT NOT NULL, 
	grp_Interest_id CHAR(40),  
	PRIMARY KEY (grp_id)
);

EOF


###End of Script###

