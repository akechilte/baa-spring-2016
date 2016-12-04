lazy val root = (project in file(".")).settings(
    name := "sample-hbase-project",
    version := "1.0",
    scalaVersion := "2.10.5"
  )

resolvers += "Spark-Hbase repo" at "http://repo.hortonworks.com/content/groups/public/"
 
libraryDependencies += "org.apache.spark" %% "spark-core" % "1.6.2" % "provided"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "1.6.2"
libraryDependencies += "com.hortonworks" % "shc" % "1.0.0-1.6-s_2.10"

// META-INF discarding
mergeStrategy in assembly <<= (mergeStrategy in assembly) { (old) =>
   {
    case PathList("META-INF", xs @ _*) => MergeStrategy.discard
    case x => MergeStrategy.first
   }
}
