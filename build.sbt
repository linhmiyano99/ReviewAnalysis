import sbt.Keys.libraryDependencies

import scala.collection.Seq

ThisBuild / version := "0.1.0-SNAPSHOT"

scalaVersion := "2.12.14"
val sparkVersion = "3.3.3"
val hadoopVersion = "3.3.0"

dependencyOverrides += "org.apache.hadoop" % "hadoop-mapreduce-client-core" % hadoopVersion
dependencyOverrides += "org.apache.hadoop" % "hadoop-common" % hadoopVersion

lazy val root = (project in file("."))
  .settings(
    scalaVersion := "2.11.8",
    retrieveManaged := true,
    name := "MapReduceApplication",
      libraryDependencies ++= Seq(
      "org.apache.hadoop" % "hadoop-common" % hadoopVersion % "provided",
      "org.apache.hadoop" % "hadoop-mapreduce-client-core" % hadoopVersion % "provided",
      "org.apache.spark" %% "spark-core" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",// https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-common
      "org.apache.spark" %% "spark-mllib" % sparkVersion % "provided",
      "com.lihaoyi" %% "requests" % "0.6.5",
      "com.typesafe.play" %% "play-json" % "2.9.4"
    )
  )
mainClass in Compile := Some("MapReduce.MapReduceApplication")
