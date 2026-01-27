# ML Module

---

## Scope

- Preparing and cleaning expense text data
- **Training an NLP-based classification model** (`train.py`)
- Evaluating model performance
- Exporting trained artifacts (model and vectorizer)

---

## Virtual Environment Setup

We use a Python virtual environment to isolate dependencies.

```bash
# Create venv in the project root
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
# OR
venv\Scripts\activate     # Windows


pip install -r requirements.txt

```

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

## Model Artifacts

After training, the following artifacts are generated:

- `model.pkl`: Trained text classification model
- `vectorizer.pkl`: TF-IDF vectorizer used during training

These artifacts are reused by the ML API service
to generate predictions without retraining.

## Model Selection

Two models were trained and evaluated:

- Multinomial Naive Bayes
- Logistic Regression (primary model)

Both models achieved high accuracy on validation and test sets.
Logistic Regression was selected as the primary model because:

- It provides well-calibrated class probabilities via `predict_proba`
- Feature weights are interpretable (word-level influence per category)
- It is robust for sparse TF-IDF features
- It generalizes well to unseen text variations

Multinomial Naive Bayes is retained only for experimentation and comparison.

## Prediction Confidence

The model outputs both:

- Predicted category (`predict`)
- Per-category probabilities (`predict_proba`)

The highest probability is used as a confidence score.
Predictions are **not treated as 100% certain**.

Low-confidence predictions can be flagged in the application
to allow users to manually correct the category.

## Known Limitations

- Training data contains short, structured item descriptions
- Real-world transaction text may be noisier or incomplete
- Some categories (e.g., Entertainment vs Personal) may overlap semantically
- The model relies purely on text and does not use metadata
  such as merchant name, amount, or transaction time

Future improvements may include:

- Additional metadata features
- Larger and more diverse datasets
- Incremental retraining using user feedback

## Out of Scope

This module does NOT handle:

- API endpoints
- Real-time inference
- Database storage
- User feedback persistence
- Model retraining automation

These responsibilities belong to downstream services.

```

```

## Project Structure

```text
ml-model/
├── artifacts/
│   ├── tfidf_vectorizer.pkl   # Trained TF-IDF vectorizer
│   └── expense_classifier_lr.pkl # Trained ML model
│   └── expense_classifier_nb.pkl # Trained ML model
│
├── data/
│   ├── raw/
│       └── backup_primary_spending_patterns_detailed.csv
│       └── CategoryMapping
│       └── primary_spending_patterns_detailed.csv
│       └── testing_later_upi_transactions_sample.csv
│   ├── processed/
│       └── training_dataset.csv
├── feedback/
│   └── feedback.jsonl
├── notebooks/
│   └── expense_category_model.ipynb
├── training/
│   ├── data/
│       └── retrain.py
│   └── dataset_builder.py
│   └── text_utils.py
│
├── requirements.txt
├── README.md
└── venv/
```

Command to build feedback_dataset.csv from feedback.jsonl
python training/dataset_builder.py

Command to build build_base_dataset from primary_spending_patterns_detailed.csv
python training/build_base_dataset.py

```text
Base Dataset + Feedback Dataset
        ↓
     Merge & Clean
        ↓
   Vectorizer Training
        ↓
     Model Training
        ↓
      Evaluation
        ↓
 Versioned Artifact Saving
```

Output Artifacts

Each retraining run generates:

```text
artifacts/
├── latest/
│     ├── expense_classifier_lr.pkl
│     └── tfidf_vectorizer.pkl
│
└── versions/
      └── <timestamp>/
            ├── expense_classifier_lr.pkl
            └── tfidf_vectorizer.pkl


latest/ → model currently used in production

versions/ → full training history for rollback & auditing
```

Command to Run Retraining
python training/retrain.py
