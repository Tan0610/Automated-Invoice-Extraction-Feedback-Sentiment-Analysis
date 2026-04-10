# Automated Invoice Extraction & Feedback Sentiment Analysis

An NLP-powered after-sales customer support portal that extracts structured data from purchase invoices (PDF or text) and performs sentiment analysis on customer feedback to automate support ticket prioritization.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture & Pipeline](#architecture--pipeline)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Notebook](#running-the-notebook)
  - [Generating Sample Invoices](#generating-sample-invoices)
- [Dataset](#dataset)
- [Models & Performance](#models--performance)
- [NLP Techniques Used](#nlp-techniques-used)
- [Sample Output](#sample-output)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Overview

This project addresses the challenge of manual after-sales support processing by combining **invoice data extraction** with **customer feedback sentiment analysis**. When a customer submits an invoice along with their review or complaint, the system:

1. Extracts key fields (invoice number, dates, amounts, companies, items) from the invoice using regex patterns and Named Entity Recognition (NER).
2. Preprocesses the feedback text through tokenization, stopword removal, stemming, and lemmatization.
3. Classifies the feedback sentiment as **Positive**, **Negative**, or **Neutral** using two independently trained ML models.
4. Assigns a support priority level (HIGH / NORMAL / LOW) based on the predicted sentiment.

---

## Features

- **Dual Invoice Extraction** -- Combines regex pattern matching with spaCy Named Entity Recognition for robust data extraction from both structured and unstructured invoice text.
- **PDF Invoice Support** -- Accepts PDF files directly using pdfplumber for text extraction, or raw text input.
- **Comprehensive Text Preprocessing** -- Tokenization (word and sentence level), stopword removal, Porter stemming, WordNet lemmatization, and POS tagging.
- **Two Independent ML Models** -- Multinomial Naive Bayes and Logistic Regression classifiers, both using TF-IDF vectorization, providing confidence scores across all sentiment classes.
- **Visual Analytics** -- Word frequency charts, bigram/trigram analysis, word clouds, and side-by-side model confidence comparison plots.
- **Automated Priority Routing** -- Negative feedback flagged as HIGH priority for immediate support escalation; neutral as NORMAL; positive as LOW.
- **Sample Invoice Generator** -- Standalone script to generate professional A4 PDF invoices with Indian billing format (GST, INR currency).
- **Fallback Handling** -- Gracefully uses sample data when no user input is provided, enabling quick demonstration.

---

## Project Structure

```
NLP_PROJECT/
|-- NLP_Project.ipynb              # Main Jupyter notebook (interactive portal)
|-- generate_invoices.py           # Script to generate sample PDF invoices
|-- requirements.txt               # Python dependencies
|-- README.md                      # Project documentation
|-- dataset/
|   +-- customer_invoice_feedback.csv   # Training dataset (200 labeled records)
+-- sample_invoices/
    |-- invoice_1.pdf              # Sample invoice - TechNova Solutions
    |-- invoice_2.pdf              # Sample invoice - CloudMinds India
    |-- invoice_3.pdf              # Sample invoice - Bharat Electronics
    |-- invoice_4.pdf              # Sample invoice - Wipro Peripherals
    |-- invoice_5.pdf              # Sample invoice - Reliance Digital
    +-- test_reviews.txt           # 5 test reviews with expected sentiments
```

---

## Architecture & Pipeline

```
USER INPUT
    |
    v
[PDF File or Pasted Text] --> pdfplumber extraction / direct text
    |
    v
INVOICE DATA EXTRACTION
    |-- Regex Patterns: Invoice No, Dates, Amounts, Companies, Items
    +-- spaCy NER: ORG, PERSON, DATE, MONEY, GPE entities
    |
    v
TEXT PREPROCESSING
    |-- Word & Sentence Tokenization (NLTK)
    |-- Stopword Removal (English corpus)
    |-- Porter Stemming
    +-- WordNet Lemmatization
    |
    v
FEEDBACK ANALYSIS
    |-- Word Frequency (Top 15 with bar chart)
    |-- N-gram Analysis (Bigrams & Trigrams)
    +-- Word Cloud Visualization
    |
    v
SENTIMENT CLASSIFICATION
    |-- Model 1: TF-IDF --> Multinomial Naive Bayes
    |-- Model 2: TF-IDF --> Logistic Regression
    +-- Confidence Scores for Positive / Negative / Neutral
    |
    v
OUTPUT
    |-- Extracted Invoice Details
    |-- Feedback Statistics (token counts, top words)
    |-- Dual Model Predictions with Confidence %
    +-- Priority: HIGH (negative) / NORMAL (neutral) / LOW (positive)
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Jupyter Notebook or JupyterLab

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Tan0610/Automated-Invoice-Extraction-Feedback-Sentiment-Analysis.git
   cd Automated-Invoice-Extraction-Feedback-Sentiment-Analysis
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy English model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Download NLTK data (auto-downloaded on first run, or manually)**

   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```

---

## Usage

### Running the Notebook

1. Start Jupyter:

   ```bash
   jupyter notebook NLP_Project.ipynb
   ```

2. Run the cells sequentially:
   - **Cell 1** -- Loads libraries, downloads NLP resources, trains both ML models on the dataset, and reports accuracy scores.
   - **Cell 2** -- Prompts for invoice input (PDF path or pasted text) and customer feedback. Uses sample data if left empty.
   - **Cell 5** -- Extracts invoice data using regex + spaCy NER. Displays extracted fields and entity tables.
   - **Cell 6** -- Preprocesses feedback text. Shows tokenization, stemming vs. lemmatization comparison table, and POS tags.
   - **Cell 7** -- Generates word frequency chart (top 15), bigram/trigram analysis, and word cloud.
   - **Cell 8** -- Predicts sentiment using both models. Displays side-by-side confidence bar charts.
   - **Cell 9** -- Prints a consolidated summary with extracted details, statistics, predictions, and priority routing.

### Generating Sample Invoices

To regenerate the 5 sample PDF invoices:

```bash
python generate_invoices.py
```

This creates professional A4 invoices in `sample_invoices/` with:
- Company headers with branding
- Itemized tables with alternating row colors
- GST (18%) calculations
- Payment terms and bank details

### Testing with Sample Reviews

The file `sample_invoices/test_reviews.txt` contains 5 pre-written reviews mapped to each sample invoice, along with expected sentiment labels. Use these to validate the model predictions.

---

## Dataset

The training dataset (`dataset/customer_invoice_feedback.csv`) contains **200 labeled records** with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| invoice_id | string | Unique identifier (INV-001 to INV-200) |
| invoice_text | string | Structured invoice text (company, items, amounts) |
| customer_feedback | string | Customer review or complaint text |
| sentiment | string | Label: positive, negative, or neutral |

### Sentiment Distribution

| Sentiment | Count | Percentage |
|-----------|-------|------------|
| Positive | 81 | 40.5% |
| Negative | 69 | 34.5% |
| Neutral | 50 | 25.0% |

The dataset covers Indian electronics and IT vendors, with invoices in INR (Indian Rupees) and 18% GST applied uniformly.

---

## Models & Performance

Two classifiers are trained on an 80/20 train-test split (160 training, 40 test samples):

| Model | Vectorization | Key Parameters |
|-------|---------------|----------------|
| Multinomial Naive Bayes | TF-IDF (English stopwords removed) | Default alpha |
| Logistic Regression | TF-IDF (English stopwords removed) | max_iter=1000, random_state=42 |

Both models output:
- Predicted sentiment class
- Confidence probability for each class (positive, negative, neutral)
- Classification report (precision, recall, F1-score)

---

## NLP Techniques Used

| Technique | Library | Purpose |
|-----------|---------|---------|
| Tokenization | NLTK (word_tokenize, sent_tokenize) | Split text into words and sentences |
| Stopword Removal | NLTK (English corpus) | Remove common non-informative words |
| Stemming | NLTK (PorterStemmer) | Reduce words to root form |
| Lemmatization | NLTK (WordNetLemmatizer) | Context-aware root form reduction |
| POS Tagging | NLTK (pos_tag) | Part-of-speech classification |
| Named Entity Recognition | spaCy (en_core_web_sm) | Extract ORG, PERSON, DATE, MONEY entities |
| TF-IDF Vectorization | scikit-learn | Convert text to numerical feature vectors |
| Regex Pattern Matching | Python re | Extract structured fields from invoice text |

---

## Sample Output

**Extracted Invoice Details:**
```
Invoice Number : INV-301
Company        : TechNova Solutions
Customer       : Sharma Electronics
Total Amount   : Rs.16,402
Date           : 2025-07-01
```

**Sentiment Prediction:**
```
Naive Bayes     : POSITIVE (Confidence: 89.2%)
Logistic Reg.   : POSITIVE (Confidence: 91.5%)
Priority        : LOW - Positive feedback logged
```

---

## Technologies Used

| Category | Libraries |
|----------|-----------|
| Data Processing | pandas, numpy |
| Visualization | matplotlib, seaborn, wordcloud |
| NLP | nltk, spacy (en_core_web_sm) |
| Machine Learning | scikit-learn (TF-IDF, Naive Bayes, Logistic Regression) |
| PDF Processing | pdfplumber |
| PDF Generation | fpdf2 |
| Language | Python 3.8+ |

---

## License

This project is open source and available for educational and research purposes.
