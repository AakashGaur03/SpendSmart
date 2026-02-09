import type { Response } from "express";

type ApiResponseOptions<T> = {
	res: Response;
	statusCode?: number;
	message: string;
	data?: T;
};

export const sendSuccess = <T>({ res, statusCode = 200, message, data }: ApiResponseOptions<T>) => {
	return res.status(statusCode).json({
		success: true,
		message,
		data: data ?? null,
	});
};

type ApiErrorResponseOptions = {
	res: Response;
	statusCode?: number;
	message: string;
	errors?: any;
};

export const sendError = ({ res, statusCode = 500, message, errors = null }: ApiErrorResponseOptions) => {
	return res.status(statusCode).json({
		success: false,
		message,
		errors,
	});
};
