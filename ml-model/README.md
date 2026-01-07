# ML Module

## Scope

This module is responsible for:

- Preparing and cleaning expense text data
- **Training an NLP-based classification model**
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

### Available Categories (Raw)

The primary dataset contains the following original spending categories:

- Groceries
- Shopping
- Subscriptions
- Housing and Utilities
- Transportation
- Food
- Medical/Dental
- Personal Hygiene
- Fitness
- Travel
- Hobbies
- Friend Activities
- Gifts

Note:
The model is designed to generalize to unseen expense descriptions.
Items not explicitly listed in the dataset (e.g., "Metro Ticket", "Bus Pass")
are expected to be inferred based on semantic similarity in text features.
Users can manually override predictions when needed.

## Category Normalization

The raw dataset contains fine-grained spending categories.
For modeling and usability, categories are normalized into the following
seven high-level classes:

### Food

- Groceries
- Food

### Shopping

- Shopping

### Bills

- Subscriptions
- Housing and Utilities

### Transport

- Transportation

### Entertainment

- Hobbies
- Friend Activities
- Travel

### Personal

- Personal Hygiene
- Fitness

### Other

- Medical/Dental
- Gifts

### Text Preprocessing

Text preprocessing is intentionally kept minimal due to the short and structured
nature of expense descriptions. The following steps are applied:

- Convert text to lowercase
- Remove punctuation
- Normalize whitespace

No stemming/Lemmatization ("running" → "run"), stop-word removal, or rule-based keyword matching is used.

## Data Splitting Strategy

The primary dataset is split into three subsets:

- **Training Set (60%)**

  - Used to train the classification model
  - The model learns patterns between expense text and normalized categories

- **Validation Set (20%)**

  - Used for hyperparameter tuning and model selection
  - Helps detect overfitting during training

- **Test Set (20%)**
  - Held out and used only once for final evaluation
  - Provides an unbiased estimate of real-world performance

The split is performed randomly while preserving class distribution
(stratified split).

## Evaluation Metrics

The model is evaluated using standard multi-class classification metrics:

- **Accuracy**

  - Measures overall correctness of predictions

- **Precision**

  - Measures how many predicted category labels are correct

- **Recall**

  - Measures how well the model identifies all instances of a category

- **F1-score**

  - Harmonic mean of precision and recall
  - Used to balance false positives and false negatives

- **Confusion Matrix**
  - Visualizes misclassifications across categories
  - Helps identify overlapping or ambiguous expense classes

## Feature Extraction

Expense items are converted into numerical features using TF-IDF
(Term Frequency–Inverse Document Frequency).

- Input feature: `Item` text
- Output label: normalized spending category
- Unigrams and bigrams are used to capture short phrases
  (e.g., "metro ticket", "electricity bill")

TF-IDF is chosen over raw word counts to reduce the impact of
frequent generic terms and improve semantic discrimination.

## Artifact = Output of training

When your model finishes training, you don’t want to:
retrain every time
lose learned weights
So you save the result.
Typical ML artifacts:
model.pkl → trained classifier
vectorizer.pkl → TF-IDF text transformer
