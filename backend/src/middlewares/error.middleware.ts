import type { NextFunction, Request, Response } from "express";
import { ZodError } from "zod";
import { sendError } from "../utils/apiResponse";
import { AppError } from "../utils/AppError";

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
	if (err instanceof ZodError) {
		const formattedErrors = err.issues.map((issue) => ({
			path: issue.path.join("."),
			message: issue.message,
		}));

		return sendError({
			res,
			statusCode: 400,
			message: "Validation failed",
			errors: formattedErrors,
		});
	}

	if (err instanceof AppError) {
		return sendError({
			res,
			statusCode: err.statusCode,
			message: err.message,
			errors: err.errors,
		});
	}

	console.error("Unhandled Error:", err);

	return sendError({
		res,
		statusCode: 500,
		message: "Internal Server Error",
		errors: null,
	});
};
