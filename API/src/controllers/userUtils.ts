import { User } from '../models/User.model'; 

export function userInfo(user : User) {
    return (({id, email, username}) => ({id,  email, username}))(user.get({ plain: true }))
}