import { useState, useEffect } from "react";
import type { Expense } from "./types/expense";
import { api } from "./api/client";
import { AddExpenseForm } from "./components/AddExpenseForm";
import { ExpenseList } from "./components/ExpenseList";
import "./App.css";

function App() {
	const [expenses, setExpenses] = useState<Expense[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	const fetchExpenses = async () => {
		try {
			setError(null);
			const data = await api.getExpenses();
			setExpenses(data ?? []);
		} catch (e) {
			setError(e instanceof Error ? e.message : "Failed to load expenses");
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		fetchExpenses();
	}, []);

	const handleAdded = (expense: Expense) => {
		setExpenses((prev) => [expense, ...prev]);
	};

	const handleCategoryChange = (id: string, updated: Expense) => {
		setExpenses((prev) => prev.map((e) => (e._id === id ? updated : e)));
	};

	const handleDeleted = (id: string) => {
		setExpenses((prev) => prev.filter((e) => e._id !== id));
	};

	return (
		<div className="app">
			<header className="header">
				<h1>SpendSmart</h1>
				<p className="tagline">Track expenses with smart categorization</p>
			</header>

			<main className="main">
				<AddExpenseForm onAdded={handleAdded} />
				{error && <div className="error-banner">{error}</div>}
				{loading ? (
					<p className="loading">Loading expenses…</p>
				) : (
					<ExpenseList expenses={expenses} onCategoryChange={handleCategoryChange} onDeleted={handleDeleted} />
				)}
			</main>
		</div>
	);
}

export default App;
