# CryptoViz API

Express.js-based RESTful API for the CryptoViz project. Written in typescript.

## Getting Started

### Running the service locally
1. Install Docker & Docker Compose
2. Clone this repository
3. Build and run the container: `docker compose up -d`
4. Either:
    - code normally without intellisense
    - install the dependencies on your os 
    - develop inside the container, using VsCode's "Remote Explorer" extension

## Dependencies

- Express.js
- Sequelize for ORM & Migrations

## Endpoints

- `/`: default "hello world" endpoint

## Deployment

The API is containerized using Docker. For Kubernetes deployment, refer to the `_Infra` repository.

