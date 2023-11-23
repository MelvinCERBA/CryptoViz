import express from 'express'
import * as userController from '../controllers/userController'
import checkAuthMiddleware from '../middlewares/authenticationMiddleware'
import profileAuthorizationMiddleware from '../middlewares/profileAuthorizationMiddleware'
import { AuthenticatedRequest } from '../types/express/custom-express'

const router = express.Router()

router.post('/register', userController.register)
router.post('/login', userController.login)
router.get('/profile/:id', checkAuthMiddleware, profileAuthorizationMiddleware, userController.getProfile)
router.put('/profile/:id', checkAuthMiddleware, profileAuthorizationMiddleware, userController.updateProfile)
router.delete('/profile/:id', checkAuthMiddleware, profileAuthorizationMiddleware, userController.deleteProfile)

export default router
