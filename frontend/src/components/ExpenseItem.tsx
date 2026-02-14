import { useState } from "react";
import type { Expense, ExpenseCategory } from "../types/expense";
import { CATEGORIES } from "../types/expense";
import { api } from "../api/client";
import "./ExpenseItem.css";

interface ExpenseItemProps {
	expense: Expense;
	onCategoryChange: (updated: Expense) => void;
	onDeleted: () => void;
}

function formatDate(iso: string) {
	const d = new Date(iso);
	return d.toLocaleDateString(undefined, {
		month: "short",
		day: "numeric",
		year: d.getFullYear() !== new Date().getFullYear() ? "numeric" : undefined,
	});
}

function confidenceLabel(conf?: number) {
	if (conf == null) return null;
	if (conf >= 0.85) return { text: "High", class: "confidence-high" };
	if (conf >= 0.5) return { text: "Medium", class: "confidence-medium" };
	return { text: "Low", class: "confidence-low" };
}

export function ExpenseItem({ expense, onCategoryChange, onDeleted }: ExpenseItemProps) {
	const [editing, setEditing] = useState(false);
	const [selectedCategory, setSelectedCategory] = useState<ExpenseCategory>(expense.category);
	const [saving, setSaving] = useState(false);
	const [deleting, setDeleting] = useState(false);

	const confidence = confidenceLabel(expense.confidence);
	const isUserCorrected = expense.category !== expense.predictedCategory;

	const handleSaveCategory = async () => {
		if (selectedCategory === expense.category) {
			setEditing(false);
			return;
		}
		setSaving(true);
		try {
			const updated = await api.updateExpenseCategory(expense._id, selectedCategory);
			onCategoryChange(updated);
			setEditing(false);
		} finally {
			setSaving(false);
		}
	};

	const handleDelete = async () => {
		if (!window.confirm("Delete this expense?")) return;
		setDeleting(true);
		try {
			await api.deleteExpense(expense._id);
			onDeleted();
		} finally {
			setDeleting(false);
		}
	};

	return (
		<li className="expense-item">
			<div className="expense-item-main">
				<div className="expense-item-head">
					<span className="expense-item-desc">{expense.description}</span>
					{expense.amount != null && (
						<span className="expense-item-amount">
							{typeof expense.amount === "number" && expense.amount % 1 !== 0
								? expense.amount.toFixed(2)
								: expense.amount}
						</span>
					)}
				</div>
				<div className="expense-item-meta">
					<span className="expense-item-date">{formatDate(expense.date)}</span>
					{confidence && expense.confidence != null && (
						<span className={`expense-item-confidence ${confidence.class}`}>
							{Math.round(expense.confidence * 100)}% · {confidence.text}
						</span>
					)}
					{isUserCorrected && <span className="expense-item-corrected">You corrected this</span>}
				</div>
			</div>

			<div className="expense-item-category">
				{editing ? (
					<div className="category-edit">
						<select
							value={selectedCategory}
							onChange={(e) => setSelectedCategory(e.target.value as ExpenseCategory)}
							className="category-select"
						>
							{CATEGORIES.map((c) => (
								<option key={c} value={c}>
									{c}
								</option>
							))}
						</select>
						<button type="button" onClick={handleSaveCategory} disabled={saving} className="btn-save">
							{saving ? "Saving…" : "Save"}
						</button>
						<button
							type="button"
							onClick={() => {
								setSelectedCategory(expense.category);
								setEditing(false);
							}}
							disabled={saving}
							className="btn-cancel"
						>
							Cancel
						</button>
					</div>
				) : (
					<>
						<span className="category-badge">{expense.category}</span>
						<button type="button" onClick={() => setEditing(true)} className="btn-edit" title="Change category">
							Edit
						</button>
					</>
				)}
			</div>

			<button type="button" onClick={handleDelete} disabled={deleting} className="btn-delete" title="Delete expense">
				{deleting ? "…" : "×"}
			</button>
		</li>
	);
}
