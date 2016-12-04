import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import org.apache.spark.SparkConf
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.functions._
import com.typesafe.config._
import java.io._

object SparkHBaseMeetupApp {

  def main(args: Array[String]) {

    val sparkConf = new SparkConf().setAppName("SparkHBaseMeetupAggregation")
    val sc = new SparkContext(sparkConf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
  
    //below code is referenced from https://github.com/typesafehub/config/blob/master/examples/scala/complex-app/src/main/scala/ComplexApp.scala
    val configFile = new File(args(0))
    val configValue = ConfigFactory.parseFile(configFile)
    val groupsTableName = configValue.getString("meetupApp.groupsTableName")
    val eventsTableName = configValue.getString("meetupApp.eventsTableName")
 
   // below piece of code is referenced from http://hortonworks.com/blog/spark-hbase-dataframe-based-hbase-connector/
    def group_catalog = s"""{
       |"table":{"namespace":"default", "name":"$groupsTableName"},
       |"rowkey":"key",
       |"columns":{
         |"grpId":{"cf":"rowkey", "col":"key", "type":"string"},
         |"grpName":{"cf":"group_details", "col":"grp_name", "type":"string"},
         |"grpDesc":{"cf":"group_details", "col":"desc", "type":"string"},
         |"city":{"cf":"group_details", "col":"city", "type":"string"},
         |"state":{"cf":"group_details", "col":"state", "type":"string"},
	 |"country":{"cf":"group_details", "col":"country", "type":"string"}
       |}
     |}""".stripMargin

    val groupDF = sqlContext.read.options(Map("catalog"->group_catalog)).format("org.apache.spark.sql.execution.datasources.hbase").load()

    //user defined function to convert the input record to map 
    def createInterestMap(record:String): Map[String, String] = {
     val array = record.split(",")
     val interestMap = Map[String, String](
     (array(1) -> array(0))
    )
    return interestMap
    }

    val file = sc.textFile(configValue.getString("meetupApp.interestLookupFile"))

    val interestMap = sc.broadcast(file.flatMap(x => createInterestMap(x)).collectAsMap())

    /** user defined function to identify whether the input string contains
    * the interest topics and assigns the key in a comma separated list */
    def mapGroupAndInterest=udf((name:String,desc:String) => {
        	var output = ""
            for ((key,value) <- interestMap.value) {
            if (name.toLowerCase.contains(key) || desc.toLowerCase.contains(key)){
                    output += value + ","
            }
        }
        output
    })

    //spark functions are referenced from spark documentation
    import sqlContext.implicits._

    val grpInterestFilteredDF = groupDF.withColumn("interestArray", mapGroupAndInterest($"grpName",$"grpDesc")).where(length($"interestArray") > 0).select("grpId","interestArray")

    val grpInterestExplodedDF = grpInterestFilteredDF.withColumn("interestId", explode(split($"interestArray", ","))).where(length($"interestId") > 0 )

    //below line of code is referenced from https://github.com/databricks/spark-csv
    grpInterestExplodedDF.select("grpId","interestId").write.format("com.databricks.spark.csv").option("header", "false").save(configValue.getString("meetupApp.groupInterestMapOutput"))

    def event_catalog = s"""{
       |"table":{"namespace":"default", "name":"$eventsTableName"},
       |"rowkey":"key",
       |"columns":{
         |"eventId":{"cf":"rowkey", "col":"key", "type":"string"},
         |"eventDt":{"cf":"event_details", "col":"event_dt", "type":"string"},
         |"attendCount":{"cf":"event_details", "col":"attendance_count", "type":"string"},
         |"yesRSVPCount":{"cf":"event_details", "col":"yes_rsvp_count", "type":"string"},
         |"grpId":{"cf":"event_details", "col":"grp_id", "type":"string"},
         |"name":{"cf":"event_details", "col":"event_name", "type":"string"},
         |"desc":{"cf":"event_details", "col":"desc", "type":"string"}
       |}
     |}""".stripMargin

     val eventDataFrame = sqlContext.read.options(Map("catalog"->event_catalog)).format("org.apache.spark.sql.execution.datasources.hbase").load()

     //below code is referenced from http://www.joda.org/joda-time/
     import org.joda.time._

     val epochToGreg=udf((input:String) => {
         	new DateTime(input.toLong).toDateTime.toString("yyyy-MM-dd")
     })

     val getMonth=udf((input:String) => {
         	new DateTime(input.toLong).toDateTime.getMonthOfYear()
     })

     val getYear=udf((input:String) => {
         	new DateTime(input.toLong).toDateTime.getYear()
     })

     //user defined function identify interest in events
     def mapEventAndInterest=udf((name:String,desc:String) => {
             var output = ""
             val nameDesc = name.toLowerCase().replaceAll("[^0-9a-zA-Z ]+"," ").replaceAll(" +"," ") + " " + desc.toLowerCase().replaceAll("[^0-9a-zA-Z ]+"," ").replaceAll(" +"," ")
             for ((key,value) <- interestMap.value) {
             if (nameDesc.contains(key)){
                     output += value + ","
             }
         }
         output
     })
     
     val eventDFWithDate = eventDataFrame.withColumn("eventDate",epochToGreg($"eventDt")).withColumn("eventMonth",getMonth($"eventDt")).withColumn("eventYear",getYear($"eventDt"))

     val eventInterestFilteredDF = eventDFWithDate.select($"eventYear",$"eventMonth",$"name",$"desc",$"grpId").withColumn("interestArray", mapEventAndInterest($"name",$"desc")).where(length($"interestArray") > 0).select($"eventYear",$"eventMonth",$"grpId",$"interestArray")

     val eventInterestExplodedDF = eventInterestFilteredDF.withColumn("interestId", explode(split($"interestArray", ","))).where(length($"interestId") > 0 )

     eventInterestExplodedDF.registerTempTable("group_event_interest")

     val groupEventInterestDF = sqlContext.sql(s"SELECT grpId,eventMonth,eventYear,interestId,count(interestId) as interestCount FROM group_event_interest GROUP BY grpId,eventMonth,eventYear,interestId")

     groupEventInterestDF.select("grpId","eventYear","eventMonth","interestId","interestCount").write.format("com.databricks.spark.csv").option("header", "false").save(configValue.getString("meetupApp.groupEventInterestOutput"))

     eventDFWithDate.registerTempTable("meetup_events")

     val eventAgg = sqlContext.sql(s"SELECT grpId,eventMonth,eventYear,count(eventId) as event_count,sum(yesRSVPCount) as total_yes_count,sum(attendCount) as total_attend_count,avg(yesRSVPCount) as avg_yes_count,avg(attendCount) as avg_attend_count,max(eventDate) as last_event_dt FROM meetup_events GROUP BY grpId,eventMonth,eventYear")

     groupDF.registerTempTable("groups")
     eventAgg.registerTempTable("eventAgg")

     val finalAggDF = sqlContext.sql(s"SELECT a.grpId,a.eventMonth,a.eventYear,a.event_count,a.total_yes_count,a.total_attend_count,a.avg_yes_count,a.avg_attend_count,a.last_event_dt,b.city,b.state,b.country from eventAgg as a LEFT JOIN groups as b on a.grpId = b.grpId")

     finalAggDF.write.format("com.databricks.spark.csv").option("header", "false").save(configValue.getString("meetupApp.aggregationOutput"))

     groupDF.select("grpId","city","state","country").write.format("com.databricks.spark.csv").option("header", "false").save(configValue.getString("meetupApp.groupDataOutput"))

    sc.stop()

  }

}
