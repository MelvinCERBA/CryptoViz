import { Table, Column, Model, DataType } from 'sequelize-typescript'

@Table({})
export class User extends Model {
  @Column({
    type: DataType.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  })
  id!: number

  @Column({
    type: DataType.STRING,
    allowNull: false,
    unique: true, 
    validate: {
      isEmail: true, 
    },
  })
  email!: string

  @Column({
    type: DataType.STRING,
    allowNull: false,
  })
  username!: string

  @Column({
    type: DataType.STRING,
    allowNull: false,
  })
  password!: string
}
