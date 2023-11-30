# CryptoViz Spark Application

This repository contains the Spark application for processing real-time analytics. Written in Python.

## Introduction

### The data

Must's:

- **Prices :** Real-time and historical price data for various cryptocurrencies
- **Volumes :** Transaction volumes over a specific period can offer insight into market trends

Nice to have's:

- **News and Events**: Important news articles, updates, and events that could affect cryptocurrency prices.
- **Regulatory Updates**: Government actions, legal changes, or policy shifts regarding cryptocurrencies.

### The challenges

- Finding the data
- Rate limits : be carefull not to get banned from scraped sites
- Evaluating the data's reliability : fake news ? errors ? ...

## Getting Started

### Run the service locally

1. Install Docker
2. Clone this repository
3. Build and run the local Kafka cluster (confluent platform) : `docker compose up -d` in ./kafka_cluster
4. Build and run the spark cluster, submit the spark app to the cluster: `docker compose build --no-cache && docker compose up -d` at root
5. Simply modify you script, and down/up the spark containers to see the result.

You can see the output of the app in the logs of the spar-submitter container in Docker Desktop.

### Tutorials

- [Getting started with Confluent/Kafka locally](https://docs.confluent.io/platform/current/platform-quickstart.html#ce-docker-quickstart)
   Hierarchical Topics: Kafka also supports topic hierarchies, so you could have something like cryptocurrency.bitcoin.price and cryptocurrency bitcoin.news as separate but logically connected topics.

## Dependencies

- Apache Spark
- PySpark

## Features

- Real-time data analytics
- Consumer for Confluent/Kafka queue

## Deployment

The Spark application runs in a cloud-based Spark cluster managed by Google Cloud's DataProc service.

