import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

// TODO: enrich streaming pipeline with more sources

object StreamingJob:
  def main(args: Array[String]): Unit =
    val spark = SparkSession.builder
      .appName("InvestStream")
      .master(sys.env.getOrElse("SPARK_MASTER", "local[*]"))
      .getOrCreate()

    import spark.implicits._
    spark.sparkContext.setLogLevel("WARN")

    val finSchema = new StructType()
      .add("company", "string")
      .add("period", "string")
      .add("pe", "double")
      .add("roe", "double")

    val finDF = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", "kafka:9092")
      .option("subscribe", "financial_data")
      .load()
      .selectExpr("CAST(value AS STRING)")
      .select(from_json($"value", finSchema).as("data"))
      .select("data.*")

    val textSchema = new StructType()
      .add("source","string").add("text","string")
      .add("sentiment", new StructType()
          .add("neg","double").add("neu","double").add("pos","double"))
      .add("topic","integer").add("ts","string")

    val textDF = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", "kafka:9092")
      .option("subscribe", "text_features")
      .load()
      .selectExpr("CAST(value AS STRING)")
      .select(from_json($"value", textSchema).as("t"))
      .selectExpr("t.sentiment.pos as pos",
                  "t.sentiment.neg as neg",
                  "t.topic as topic",
                  "t.ts as ts")

    val textAgg = textDF
      .withWatermark("ts", "2 hours")
      .groupBy(window($"ts", "1 hour").as("w"))
      .agg(avg("pos").as("avg_pos"),
           avg("neg").as("avg_neg"),
           count("*").as("msg_cnt"))

    val features = finDF
      .join(textAgg)
      .withColumn("feature_vector",
        array($"pe",$"roe",$"avg_pos",$"avg_neg",$"msg_cnt"))

    val query = features.writeStream
      .foreachBatch { (batchDF, _) =>
        batchDF.write
          .format("jdbc")
          .option("url","jdbc:postgresql://postgres:5432/invest")
          .option("dbtable","features")
          .option("user","invest").option("password","invest")
          .mode("append").save()
      }
      .start()

    query.awaitTermination()
