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

## Sequelize

### How to create a migration
1. Update the Model Definition in `app/models`
2. Create the migration (from within the container)
> npx sequelize-cli migration:create --name <migration-name>  

3. Implement the `up()` and `down()` functions in `/migrations/<migration-name>.js`

### How to run migrations
1. Ensure the dn container is running
2. Run the migrations (from within the container):
> npx sequelize-cli db:migrate --config ./app/config/config.json

## Deployment

The API is containerized using Docker. For Kubernetes deployment, refer to the `_Infra` repository.

