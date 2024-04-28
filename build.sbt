import sbt.Keys.libraryDependencies

import scala.collection.Seq

ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.19"
val sparkVersion = "3.3.3"

lazy val root = (project in file("."))
  .settings(
    name := "MapReduceApplication",
      libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.2.0",
      "org.apache.spark" %% "spark-sql" % "3.2.0",
      "org.apache.spark" %% "spark-core" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",// https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-common
      "org.apache.spark" %% "spark-mllib" % sparkVersion % "provided"

    )
  )
mainClass in Compile := Some("MapReduce.WordCount")
