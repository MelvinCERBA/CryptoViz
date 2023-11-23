import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import { Request, Response, NextFunction } from 'express';
import { AuthenticatedRequest } from '../types/express/custom-express';

const checkAuthMiddleware = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const token = req.headers["authorization"];
    if (!token) {
        return res.status(401).json({ message: "Access denied. No token provided." });
    }
    try {
        const decoded = verifyToken(token);
        req.user! = decoded; 
        next();
    } catch (error) {
        res.status(400).json({ message: "Invalid token." });
    }
}


async function hashPassword(password: string): Promise<string> {
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    return hashedPassword;
}

async function comparePasswords(inputPassword: string, storedHashedPassword: string): Promise<boolean> {
    return await bcrypt.compare(inputPassword, storedHashedPassword);
}

function generateToken(userID: string): string {
    const secretKey = process.env.JWT_SECRET!;  
    const token = jwt.sign({ id: userID }, secretKey, { expiresIn: "1h" }); // Token expires in 1 hour
    return token;
}

function verifyToken(token: string): any {
    const secretKey = process.env.JWT_SECRET!;
    try {
        return jwt.verify(token, secretKey);
    } catch (error) {
        throw new Error("Token is not valid");
    }
}

export default checkAuthMiddleware;
