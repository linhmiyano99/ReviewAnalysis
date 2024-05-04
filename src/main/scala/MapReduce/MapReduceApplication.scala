package MapReduce
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkContext
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import services.API.sendToAPI


case class Review (reviewId: String, asin: String, reviewName: String, helpful: Array[Int], reviewText: String, overall: Float, summary: String, unixReviewTime: Int, reviewTime: String)

// Function to send review text to API and process the response

object MapReduceApplication {
  def main(args: Array[String]): Unit = {

//    val spark = SparkSession.getActiveSession.get
  val tasksPerCore = 2
  val conf = new SparkConf()
      .setAppName("MapReduceApplication")
      .setMaster("local[*]")
      .set("spark.driver.memory", "10GB")
      .set("spark.executor.memory", "10GB")
  val spark: SparkSession = SparkSession.builder().config(conf).getOrCreate()
  val sc: SparkContext = spark.sparkContext
  spark.conf.set("spark.sql.shuffle.partitions", ((java.lang.Runtime.getRuntime.availableProcessors * sc.statusTracker.getExecutorInfos.length) * tasksPerCore).toString())
  spark.conf.set("spark.default.parallelism", ((java.lang.Runtime.getRuntime.availableProcessors * sc.statusTracker.getExecutorInfos.length) * tasksPerCore).toString())

  val numWorkers = sc.getConf.getInt("spark.executor.instances", 0)

  println("Number of Spark workers: " + numWorkers)


    // Read input text file
    var csv= spark.read.format("csv")
          .option("header", "true")
          .option("inferSchema", "true")
          .load("data/input/")

      csv = csv.withColumn("reviewText", col("reviewText").cast(StringType))
              .withColumn("orderId", col("orderId").cast(StringType))
              .withColumn("rate", col("rate").cast(StringType))
    println(csv.show())
    println(csv.printSchema())

    val textDF = csv.select("reviewText")


    val textRDD = textDF.rdd
      .filter(row => !row.isNullAt(0)) // Filter out null values
      .map(row => row.getString(0))

      val responsesRDD: RDD[(String, String)] = textRDD.map(sendToAPI)
//      responsesRDD.foreach(processResponse)
      val data = responsesRDD.collect()

      val df = spark.createDataFrame(data).toDF("reviewText", "result")
      df.write
        .format("csv")
        .option("header", "true")
        .mode("overwrite")
        .save("data/output/result.csv")
  }
}
