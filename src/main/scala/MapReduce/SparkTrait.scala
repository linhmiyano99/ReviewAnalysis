package MapReduce
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{SQLContext, SparkSession}

trait SparkTrait {
  private val tasksPerCore = 2
  private val conf = new SparkConf()
    .setAppName("FirstScalaAppName")
    .setMaster("local[*]")
    .set("spark.driver.memory", "10G")
    .set("spark.executor.memory", "10G")
    .set("spark.local.dir", "/tmp")
  protected implicit val spark: SparkSession = SparkSession.builder().config(conf).getOrCreate()
  protected val sc: SparkContext = spark.sparkContext
  protected val sqlContext: SQLContext = spark.sqlContext

  spark.conf.set("spark.sql.shuffle.partitions", ((java.lang.Runtime.getRuntime.availableProcessors * sc.statusTracker.getExecutorInfos.length) * tasksPerCore).toString())
  spark.conf.set("spark.default.parallelism", ((java.lang.Runtime.getRuntime.availableProcessors * sc.statusTracker.getExecutorInfos.length) * tasksPerCore).toString())

}
