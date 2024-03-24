# Use the Bitnami Spark image as the base image
FROM bitnami/spark:3.5.1

# Install the Cassandra Python driver
RUN pip install cassandra-driver

