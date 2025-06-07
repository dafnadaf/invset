FROM bitnami/spark:3.5
RUN apt-get update && apt-get install -y openjdk-17-jdk scala
COPY target/scala-3.3.3/streamingjob_3-0.1.jar /opt/spark/jobs/
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
CMD ["spark-submit","--class","StreamingJob","/opt/spark/jobs/streamingjob_3-0.1.jar"]
