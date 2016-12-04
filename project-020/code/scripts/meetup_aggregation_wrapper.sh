#!/bin/sh

if [ $# -ne 3 ]
then
echo "This script requires 3 parameters"
echo "1) HBase conf folder, example: /usr/hdp/current/hbase-client/conf/"
echo "2) Master URL to submit Spark job: yarn or ip"
echo "3) Deployment mode, example: local or cluster"
exit 1
fi

spark-submit --driver-class-path ${1}  --class "SparkHBaseMeetupApp" --master ${2} --deploy-mode ${3} ./spark-hbase-meetup-project-assembly-1.0.jar ../conf/meetup_analytics.conf

exit 0
