import dotenv from "dotenv"
import express from "express"
import userRoutes from "./src/routes/userRoutes"
import { sequelize } from "./src/models/index"


dotenv.config()
if (!process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is not defined in .env")
}

const app = express()
const router = express.Router();

sequelize.sync({ alter: true }).then(() => {
    console.log('Database synced');

    const port = 8080
    const ip = "0.0.0.0"    
    app.listen(port, ip, () => {
        console.log(`API listening at http://${ip}:${port}`)
    })
    
    
    router.use("/users", userRoutes)
    
    app.get("/", (req, res) => {
        res.send("Hello, TypeScript with Express!")
    })
})
.catch((error) => {
    throw new Error('Error syncing database:', error);
});


export default router
