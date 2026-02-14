import mongoose, { Schema, Document, Model } from "mongoose";

const VALID_CATEGORIES = ["Food", "Shopping", "Bills", "Transport", "Entertainment", "Personal", "Other"] as const;

export type ExpenseCategory = (typeof VALID_CATEGORIES)[number];

export interface ITopPrediction {
	category: string;
	confidence: number;
}

export interface IExpense extends Document {
	description: string;
	amount?: number;
	date: Date;
	category: ExpenseCategory;
	/** Category predicted by ML at creation */
	predictedCategory?: ExpenseCategory;
	/** Confidence of the prediction (0–1) */
	confidence?: number;
	/** Top 3 predictions from ML (for feedback if user changes category) */
	topPredictions?: ITopPrediction[];
	/** Whether we already sent feedback to ML for a user correction */
	feedbackSent?: boolean;
	createdAt: Date;
	updatedAt: Date;
}

const TopPredictionSchema = new Schema(
	{
		category: { type: String, required: true },
		confidence: { type: Number, required: true, min: 0, max: 1 },
	},
	{ _id: false }
);

const expenseSchema = new Schema<IExpense>(
	{
		description: { type: String, required: true, trim: true },
		amount: { type: Number, min: 0 },
		date: { type: Date, default: () => new Date() },
		category: {
			type: String,
			required: true,
			enum: VALID_CATEGORIES,
		},
		predictedCategory: { type: String, enum: VALID_CATEGORIES },
		confidence: { type: Number, min: 0, max: 1 },
		topPredictions: [TopPredictionSchema],
		feedbackSent: { type: Boolean, default: false },
	},
	{
		timestamps: true,
		toJSON: {
			transform(_, ret: Record<string, unknown>) {
				if (ret._id) ret._id = (ret._id as mongoose.Types.ObjectId).toString();
				if (ret.date) ret.date = new Date(ret.date as Date).toISOString();
				if (ret.createdAt) ret.createdAt = new Date(ret.createdAt as Date).toISOString();
				if (ret.updatedAt) ret.updatedAt = new Date(ret.updatedAt as Date).toISOString();
			},
		},
	}
);

export const Expense: Model<IExpense> = mongoose.models.Expense ?? mongoose.model<IExpense>("Expense", expenseSchema);
