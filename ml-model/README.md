# ML Module

## Scope

This module is responsible for:

- Preparing and cleaning expense text data
- Training an NLP-based classification model
- Evaluating model performance
- Exporting trained artifacts (model and vectorizer)

No API or UI logic lives here.

## Datasets

### Primary Dataset (Training & Evaluation)

- Filename: `primary_spending_patterns_detailed.csv`
- Source: Kaggle – [Spending Patterns Dataset](https://www.kaggle.com/datasets/ahmedmohamed2003/spending-habits)
- Size: ~10,000 rows
- Used for:
  - Model training
  - Validation and evaluation
- Contains structured item descriptions mapped to spending categories.
- Categories will be normalized into a smaller, consistent set for classification.

### Secondary Dataset (External Testing – Future Use)

- Filename: `testing_later_upi_transactions_sample.csv`
- Source: Kaggle – [UPI Transactions 2024 Dataset](https://www.kaggle.com/datasets/skullagos5246/upi-transactions-2024-dataset)
- Size: ~25,000 rows
- Used for:
  - Testing model generalization on unseen, real-world-like data
- Not used in initial training due to different schema and category definitions.

### Backup / Reference Dataset

- Source: Kaggle – [Personal Expense Classification Dataset](https://www.kaggle.com/datasets/sahideseker/personal-expense-classification-dataset)
- Size: ~100 rows
- Status: Not stored in repository
- Purpose:
  - Reference only
  - Used to validate early assumptions about text-based expense categorization
