import dotenv from "dotenv";
import express from "express";
import userRoutes from "./routes/userRoutes";
import { sequelize } from "./models/index";
import cors from 'cors';

dotenv.config();
if (!process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is not defined in .env");
}
const app = express();

app.use(cors({
    origin: 'http://localhost:5173' 
  }));
app.use(express.json()); 
app.use("/users", userRoutes);

app.get("/", (req, res) => {
    res.send("Hello, TypeScript with Express!");
});

sequelize.sync({ alter: true })
.then(() => {
    console.log('Database synced');
})
.catch((error) => {
    console.error('Error syncing database:', error);
});

const port = 8080;
const ip = "0.0.0.0";
app.listen(port, ip, () => {
    console.log(`API listening at http://${ip}:${port}`);
});