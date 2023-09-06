# CryptoViz Infrastructure

This repository contains all the infrastructure-as-code (IaC) files for the CryptoViz project.

## Tools

- Docker
- Kubernetes
- Terraform

## Getting Started

### Deployment

1. Install Docker, Kubernetes, and Terraform
2. Clone this repository
3. Deploy the stack with `terraform apply`

### Development 

#### Run Confluent Platform locally

Confluent platform is used to mimic confluent cloud locally. It is used byt the web scrapper and by the spark application.

1. Install Docker
2. Clone this repository
3. Create the docker network "confluent-network" with `docker network create --driver bridge confluent-network`
4. Build and run the Confluent Platform cluster with `docker compose up -d`

#### Run local Postgresql DB

We use postgres to mimic CLoudSQL in the development environnement.

1. Install Docker
2. Clone this repository
3. Create the docker network "db-network" with `docker network create --driver bridge db-network`
4. Build and run the Confluent Platform cluster with `docker compose up -d`
5. A pgAdmin is available at http://localhost:8082/ 
    - Acces it using  user `admin@example.com` and password `admin`
    - connect to the postgres server at `db:5432` with user `myuser` and password `mypassword`

## Deployment

All microservices are containerized and orchestrated using Kubernetes. Terraform is used for automating the infrastructure.

