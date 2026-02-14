const API_BASE = "/api";

interface ApiSuccess<T> {
	success: true;
	message: string;
	data: T;
}

interface ApiError {
	success: false;
	message: string;
	errors: unknown;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

async function request<T>(path: string, options: RequestInit = {}): Promise<ApiSuccess<T>["data"]> {
	const res = await fetch(`${API_BASE}${path}`, {
		...options,
		headers: {
			"Content-Type": "application/json",
			...options.headers,
		},
	});
	const json: ApiResponse<T> = await res.json();

	if (!res.ok) {
		const err = json as ApiError;
		throw new Error(err.message || "Request failed");
	}

	const success = json as ApiSuccess<T>;
	return success.data;
}

export interface CreateExpenseInput {
	description: string;
	amount?: number;
	date?: string;
}

export const api = {
	getExpenses: () => request<import("../types/expense").Expense[]>("/expenses"),

	createExpense: (body: CreateExpenseInput) =>
		request<import("../types/expense").Expense>("/expenses", {
			method: "POST",
			body: JSON.stringify(body),
		}),

	updateExpenseCategory: (id: string, category: import("../types/expense").ExpenseCategory) =>
		request<import("../types/expense").Expense>(`/expenses/${id}`, {
			method: "PATCH",
			body: JSON.stringify({ category }),
		}),

	deleteExpense: (id: string) => request<{ id: string }>(`/expenses/${id}`, { method: "DELETE" }),
};
