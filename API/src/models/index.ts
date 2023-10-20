import { Sequelize } from 'sequelize-typescript';
import { User } from './User.model';

export const sequelize = new Sequelize({
    database:   'processed_data_db',
    username:   'myuser',
    password:   'mypassword',
    host:       'db',
    port:       5432, 
    dialect:    'postgres',
    models:     [User],
});
sequelize.authenticate()
    .then(() => console.log('Connection has been established successfully.'))
    .catch(err => console.error('Unable to connect to the database:', err));

export default sequelize;
