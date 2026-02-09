import dotenv from "dotenv";

dotenv.config();

export const env = {
	port: process.env.PORT ? Number(process.env.PORT) : 4000,
	mongoUri: process.env.MONGO_URI || "",
	mlServiceUrl: process.env.ML_SERVICE_URL || "http://localhost:8000",
	nodeEnv: process.env.NODE_ENV || "development",
};
