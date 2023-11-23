import express from "express"
import { Request, Response, NextFunction } from "express"
import { AuthenticatedRequest } from "../types/express/custom-express"

const profileAuthorizationMiddleware = (
    req: AuthenticatedRequest,
    res: Response,
    next: NextFunction
) => {
    const requested_user_id = req.params.id
    if (requested_user_id != req.user!.id) {
        return res
            .status(403)
            .json({ message: "Forbidden access to other users profile." })
    }
    next()
}

export default profileAuthorizationMiddleware