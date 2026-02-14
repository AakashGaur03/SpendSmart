import { useState } from "react";
import type { Expense } from "../types/expense";
import { api } from "../api/client";
import "./AddExpenseForm.css";

interface AddExpenseFormProps {
	onAdded: (expense: Expense) => void;
}

export function AddExpenseForm({ onAdded }: AddExpenseFormProps) {
	const [description, setDescription] = useState("");
	const [amount, setAmount] = useState("");
	const [submitting, setSubmitting] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const desc = description.trim();
		if (!desc) return;
		setError(null);
		setSubmitting(true);
		try {
			const body: { description: string; amount?: number } = { description: desc };
			const num = amount.trim() ? parseFloat(amount) : undefined;
			if (num !== undefined && !Number.isNaN(num) && num >= 0) {
				body.amount = num;
			}
			const data = await api.createExpense(body);
			onAdded(data);
			setDescription("");
			setAmount("");
		} catch (e) {
			setError(e instanceof Error ? e.message : "Failed to add expense");
		} finally {
			setSubmitting(false);
		}
	};

	return (
		<form className="add-expense-form" onSubmit={handleSubmit}>
			<div className="form-row">
				<input
					type="text"
					placeholder="What did you spend on? e.g. Metro ticket"
					value={description}
					onChange={(e) => setDescription(e.target.value)}
					disabled={submitting}
					className="input-description"
				/>
				<input
					type="number"
					placeholder="Amount"
					min="0"
					step="0.01"
					value={amount}
					onChange={(e) => setAmount(e.target.value)}
					disabled={submitting}
					className="input-amount"
				/>
			</div>
			{error && <p className="form-error">{error}</p>}
			<button type="submit" disabled={submitting || !description.trim()} className="btn-submit">
				{submitting ? "Adding…" : "Add expense"}
			</button>
		</form>
	);
}
