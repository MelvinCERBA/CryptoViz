import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { User } from '../models/User.model'; //  User model to be defined with Sequelize.

export const register = async (req: Request, res: Response) => {
    try {
        const { username, password } = req.body;

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await User.create({ username, password: hashedPassword });

        res.status(201).json({ message: 'User registered!', userId: user.id });
    } catch (error) {
        res.status(500).json({ message: 'Registration failed.', error: (error as Error).message });
    }
};

export const login = async (req: Request, res: Response) => {
    try {
        const { username, password } = req.body;
        const user = await User.findOne({ where: { username } });

        if (!user || !await bcrypt.compare(password, user.password)) {
            return res.status(400).json({ message: 'Invalid credentials.' });
        }

        const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET as string, { expiresIn: '1h' });
        res.json({ message: 'Logged in!', token });
    } catch (error) {
        res.status(500).json({ message: 'Login failed.', error: (error as Error).message });
    }
};

export const getProfile = async (req: Request, res: Response) => {
    try {
        const user = await User.findByPk(req.params.id);
        if (!user) {
            return res.status(404).json({ message: 'User not found.' });
        }
        res.json(user);
    } catch (error) {
        res.status(500).json({ message: 'Fetching profile failed.', error: (error as Error).message });
    }
};

export const updateProfile = async (req: Request, res: Response) => {
    try {
        const user = await User.findByPk(req.params.id);
        if (!user) {
            return res.status(404).json({ message: 'User not found.' });
        }

        // Assuming only the username can be updated for simplicity
        const { username } = req.body;
        user.username = username;

        await user.save();

        res.json({ message: 'Profile updated!', user });
    } catch (error) {
        res.status(500).json({ message: 'Updating profile failed.', error: (error as Error).message });
    }
};

export const deleteProfile = async (req: Request, res: Response) => {
    try {
        const user = await User.findByPk(req.params.id);
        if (!user) {
            return res.status(404).json({ message: 'User not found.' });
        }

        await user.destroy();

        res.json({ message: 'Profile deleted!' });
    } catch (error) {
        res.status(500).json({ message: 'Deleting profile failed.', error: (error as Error).message });
    }
};

