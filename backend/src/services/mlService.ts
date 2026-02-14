import axios, { AxiosInstance } from "axios";
import { env } from "../config/env";

export interface PredictionResponse {
	predicted_category: string;
	confidence: number;
	confidence_level: string;
	probabilities: Record<string, number>;
	top_predictions: { category: string; confidence: number }[];
}

export interface FeedbackPayload {
	item: string;
	predicted_category: string;
	confidence: number;
	top_predictions: { category: string; confidence: number }[];
	user_selected_category: string;
}

const client: AxiosInstance = axios.create({
	baseURL: env.mlServiceUrl,
	timeout: 10000,
	headers: { "Content-Type": "application/json" },
});

export async function predictCategory(item: string): Promise<PredictionResponse> {
	const { data } = await client.post<PredictionResponse>("/predict", { item });
	return data;
}

export async function submitFeedback(payload: FeedbackPayload): Promise<void> {
	await client.post("/feedback", payload);
}

export async function checkMlHealth(): Promise<boolean> {
	try {
		const { data } = await client.get<{ status: string }>("/health");
		return data?.status === "ok";
	} catch {
		return false;
	}
}
