ThisBuild / scalaVersion := "3.3.3"
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-sql-kafka-0-10" % "3.5.1",
  "org.apache.spark" %% "spark-streaming" % "3.5.1",
  "org.postgresql" % "postgresql" % "42.7.3"
)
