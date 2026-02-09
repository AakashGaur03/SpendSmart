import { Router } from "express";
import { sendSuccess } from "./utils/apiResponse";
import { AppError } from "./utils/AppError";

const router = Router();

router.get("/health", (req, res) => {
	return sendSuccess({
		res,
		statusCode: 200,
		message: "Backend is healthy",
		data: {
			timestamp: new Date().toISOString(),
		},
	});
});

router.get("/test-error", (req, res) => {
	throw new AppError("This is a test error", 400);
});

export default router;
