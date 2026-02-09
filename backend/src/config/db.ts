import mongoose from "mongoose";
import { env } from "./env";

export const connectDB = async (): Promise<void> => {
	if (!env.mongoUri) {
		console.error(" MONGO_URI is missing in env");
		process.exit(1);
	}

	try {
		await mongoose.connect(env.mongoUri);
		console.log(" MongoDB connected Succesfully");
	} catch (error) {
		console.error(" MongoDB connection failed:", error);
		process.exit(1);
	}
};
