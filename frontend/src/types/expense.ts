export type ExpenseCategory = "Food" | "Shopping" | "Bills" | "Transport" | "Entertainment" | "Personal" | "Other";

export interface TopPrediction {
	category: string;
	confidence: number;
}

export interface Expense {
	_id: string;
	description: string;
	amount?: number;
	date: string;
	category: ExpenseCategory;
	predictedCategory?: ExpenseCategory;
	confidence?: number;
	topPredictions?: TopPrediction[];
	feedbackSent?: boolean;
	createdAt: string;
	updatedAt: string;
}

export const CATEGORIES: ExpenseCategory[] = [
	"Food",
	"Shopping",
	"Bills",
	"Transport",
	"Entertainment",
	"Personal",
	"Other",
];
