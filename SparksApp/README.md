# CryptoViz Spark Application

This repository contains the Spark application for processing real-time analytics. Written in Python.

## Getting Started

### Run the service locally
1. Install Docker
2. Clone this repository
3. Build and run the local Kafka cluster (confluent platform) : `docker compose up -d` in ./kafka_cluster
4. Build and run the spark cluster, submit the spark app to the cluster: `docker compose up -d` at root
5. Simply modify you script, and down/up the spark containers to see the result.

You can see the output of the app in the logs of the spar-submitter container in Docker Desktop.

## Tutorials

- [Getting started with Confluent/Kafka locally](https://docs.confluent.io/platform/current/platform-quickstart.html#ce-docker-quickstart)

## Dependencies

- Apache Spark
- PySpark

## Features

- Real-time data analytics
- Consumer for Confluent/Kafka queue

## Deployment

The Spark application runs in a cloud-based Spark cluster managed by Google Cloud's DataProc service.

