Project: Meetup Data Analysis and Reporting

Participants
    Rajaram, Balaji, F16-DG-4058, brajaram, brajaram@iu.edu
    
    Biswas, Malabika, F16-DG-4011, malabikab16, mbiswas@iu.edu

Abstract
    In this paper, we present our analysis on the data collected from meetup.com, a social networking platform.  This is an end-to-end to Big Data project that includes data consumption, pre-processing, analytics and visualization.  The focus of our analysis is on two countries, the United States and India.


Prerequisites
    An environment with following softwares:
    Hadoop, HDFS, Spark, Python, Scala, MySQL, Tableau, SBT (to build fat jar)
    
    pip install requirements.txt
    

Deployment Instructions

1. Clone the project
	git clone https://gitlab.com/cloudmesh_fall2016/project-020.git

2. Get API key
	get API key of your meetup account from below link and update in meetup_city_pull.py, meetup_group_pull.py, meetup_event_pull.py scripts.
	
	https://secure.meetup.com/meetup_api/key/

3. Execute script to create HBase and MySQL table
	bash project-020/code/scripts/create_tables.sh <mysql-user-id> <mysql-password> <database-name>

4. Start executing data pull scripts
	bash project-020/code/scripts/meetup_data_pull.sh

5. Once data pull is complete, 
	- put the interest_map.csv (from conf directory) into hdfs location and update the hdfs location in meetup_aggregation.conf
	- update the meetup_aggregation.conf in conf directory with the hdfs output locations
	- execute the sh meetup_aggregation_wrapper.sh with the below 3 parameters
		1) HBase conf folder, example: /usr/hdp/current/hbase-client/conf/
		2) Master URL to submit Spark job: yarn or ip or local[number of cores]
		3) Deployment mode, example: cluster or client

6. Execute MySQL data load script
    - use hadoop fs -cat aggregation_output_location/part-* > project-020/data/meetup_agg.csv
    - use hadoop fs -cat group-interest_output_location/part-* > project-020/data/group_interest_map.csv
    - python project-020/code/scripts/meetup_load_stat.py meetup_insights project-020/data/meetup_agg.csv
    - python project-020/code/scripts/meetup_load_stat.py group_interest_mapping project-020/data/group_interest_map.csv
    - python project-020/code/scripts/meetup_load_stat.py meetup_interest project-020/conf/interest_map.csv



References:
	https://gitlab.com/cloudmesh_fall2016/project-020/blob/master/report/bib/references.bib
