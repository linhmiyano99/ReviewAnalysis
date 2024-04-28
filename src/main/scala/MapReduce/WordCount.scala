package MapReduce
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.rdd.RDD
import services.API.{sendToAPI, processResponse}
case class Review (reviewId: String, asin: String, reviewName: String, helpful: Array[Int], reviewText: String, overall: Float, summary: String, unixReviewTime: Int, reviewTime: String)

// Function to send review text to API and process the response

object WordCount {
  def main(args: Array[String]): Unit = {

//    val spark = SparkSession.getActiveSession.get
  val spark = SparkSession.builder()
    .appName("MapReduceApplication")
    .config("spark.master", "local") // Remove this if you're running on a cluster
    .getOrCreate()

    // Read input text file
    var csv= spark.read.format("csv")
          .option("header", "true")
          .option("inferSchema", "true")
          .load("data/input/88201679_20493037179.csv")

      csv = csv.withColumn("reviewText", col("reviewText").cast(StringType))
              .withColumn("orderId", col("orderId").cast(StringType))
              .withColumn("rate", col("rate").cast(StringType))
    println(csv.show())
    println(csv.printSchema())

    val textDF = csv.select("reviewText")


    val textRDD = textDF.rdd
      .filter(row => !row.isNullAt(0)) // Filter out null values
      .map(row => row.getString(0))

      val responsesRDD: RDD[String] = textRDD.map(sendToAPI)
      responsesRDD.foreach(processResponse)

  }
}
