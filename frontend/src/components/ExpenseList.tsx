import type { Expense } from "../types/expense";
import { ExpenseItem } from "./ExpenseItem";
import "./ExpenseList.css";

interface ExpenseListProps {
	expenses: Expense[];
	onCategoryChange: (id: string, updated: Expense) => void;
	onDeleted: (id: string) => void;
}

export function ExpenseList({ expenses, onCategoryChange, onDeleted }: ExpenseListProps) {
	if (expenses.length === 0) {
		return (
			<div className="expense-list-empty">
				<p>No expenses yet. Add one above to get started — we’ll suggest a category automatically.</p>
			</div>
		);
	}

	return (
		<section className="expense-list">
			<h2 className="expense-list-title">Recent expenses</h2>
			<ul className="expense-list-ul">
				{expenses.map((expense) => (
					<ExpenseItem
						key={expense._id}
						expense={expense}
						onCategoryChange={(updated) => onCategoryChange(expense._id, updated)}
						onDeleted={() => onDeleted(expense._id)}
					/>
				))}
			</ul>
		</section>
	);
}
