import { Router } from "express";
import { z } from "zod";
import { sendSuccess } from "../utils/apiResponse";
import { asyncHandler } from "../utils/asyncHandler";
import { AppError } from "../utils/AppError";
import { Expense, type ExpenseCategory, type ITopPrediction } from "../models/Expense";
import { predictCategory, submitFeedback } from "../services/mlService";

const router = Router();

const VALID_CATEGORIES = ["Food", "Shopping", "Bills", "Transport", "Entertainment", "Personal", "Other"] as const;

const createExpenseSchema = z.object({
	description: z.string().min(1, "Description is required").trim(),
	amount: z.number().min(0).optional(),
	date: z.union([z.string().datetime(), z.string().regex(/^\d{4}-\d{2}-\d{2}$/)]).optional(),
});

const categoryEnum = z.enum(["Food", "Shopping", "Bills", "Transport", "Entertainment", "Personal", "Other"]);
const updateExpenseSchema = z.object({
	category: categoryEnum,
});

/** GET /api/expenses – list all expenses, newest first */
router.get(
	"/expenses",
	asyncHandler(async (req, res) => {
		const expenses = await Expense.find().sort({ createdAt: -1 }).lean();
		return sendSuccess({
			res,
			message: "Expenses fetched",
			data: expenses,
		});
	})
);

/** POST /api/expenses – create expense, get ML prediction, save */
router.post(
	"/expenses",
	asyncHandler(async (req, res) => {
		const parsed = createExpenseSchema.safeParse(req.body);
		if (!parsed.success) {
			const first = parsed.error.issues[0];
			throw new AppError(first?.message ?? "Validation failed", 400);
		}
		const { description, amount, date } = parsed.data;

		let predictedCategory: ExpenseCategory = "Other";
		let confidence = 0;
		let topPredictions: ITopPrediction[] = [];

		try {
			const prediction = await predictCategory(description);
			predictedCategory = prediction.predicted_category as ExpenseCategory;
			confidence = prediction.confidence;
			topPredictions = prediction.top_predictions.map((p) => ({
				category: p.category,
				confidence: p.confidence,
			}));
		} catch (err) {
			console.error("ML predict failed, using default category:", err);
		}

		const expense = await Expense.create({
			description,
			amount,
			date: date ? new Date(date) : new Date(),
			category: predictedCategory,
			predictedCategory,
			confidence,
			topPredictions,
			feedbackSent: false,
		});

		return sendSuccess({
			res,
			statusCode: 201,
			message: "Expense created",
			data: expense,
		});
	})
);

/** PATCH /api/expenses/:id – update expense (e.g. category); send feedback to ML if category changed */
router.patch(
	"/expenses/:id",
	asyncHandler(async (req, res) => {
		const { id } = req.params;
		const parsed = updateExpenseSchema.safeParse(req.body);
		if (!parsed.success) {
			const first = parsed.error.issues[0];
			throw new AppError(first?.message ?? "Validation failed", 400);
		}
		const { category: userSelectedCategory } = parsed.data;

		const expense = await Expense.findById(id);
		if (!expense) {
			throw new AppError("Expense not found", 404);
		}

		const previousCategory = expense.category;
		expense.category = userSelectedCategory as ExpenseCategory;

		if (
			previousCategory !== userSelectedCategory &&
			!expense.feedbackSent &&
			expense.predictedCategory &&
			expense.topPredictions?.length
		) {
			try {
				await submitFeedback({
					item: expense.description,
					predicted_category: expense.predictedCategory,
					confidence: expense.confidence ?? 0,
					top_predictions: expense.topPredictions,
					user_selected_category: userSelectedCategory,
				});
				expense.feedbackSent = true;
			} catch (err) {
				console.error("ML feedback failed:", err);
			}
		}

		await expense.save();

		return sendSuccess({
			res,
			message: "Expense updated",
			data: expense,
		});
	})
);

/** DELETE /api/expenses/:id */
router.delete(
	"/expenses/:id",
	asyncHandler(async (req, res) => {
		const deleted = await Expense.findByIdAndDelete(req.params.id);
		if (!deleted) {
			throw new AppError("Expense not found", 404);
		}
		return sendSuccess({
			res,
			message: "Expense deleted",
			data: { id: deleted._id },
		});
	})
);

export default router;
