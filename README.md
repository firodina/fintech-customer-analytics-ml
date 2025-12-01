# Fintech CX Analytics

A project for analyzing user behavior, experience, and customer journey metrics in fintech applications.

## 🚀 Features

* User behavior analytics
* Churn prediction (later)
* Funnel analysis
* Customer segmentation
* Interactive dashboards

## 📁 Project Structure

fintech-customer-analytics-ml/
│
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── preprocessing/
│   ├── analytics/
│   └── models/
├── reports/
│   └── figures/
├── .github/workflows/
├── .vscode/
├── .gitignore
├── requirements.txt
└── README.md

## 🛠 Setup

```bash
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

# ✅ Task Deliverables

## **Task 1: Data Collection and Preprocessing**

Scrape reviews from the Google Play Store, preprocess them for analysis, and manage code via GitHub.

### **Tasks**

#### **Git Setup**

* Create a GitHub repository.
* Include `.gitignore`, `requirements.txt`.
* Use **“task-1” branch**.
* Commit frequently with meaningful messages after completing logical chunks.

#### **Web Scraping**

* Use **google-play-scraper** to collect reviews, ratings, dates, and app names for **three banks**.
* Target **400+ reviews per bank (1,200 total)**.

#### **Preprocessing**

* Remove duplicates, handle missing data.
* Normalize dates (e.g., `YYYY-MM-DD`).
* Save final CSV with columns: `review`, `rating`, `date`, `bank`, `source`.

### **KPIs**

* **1,200+ reviews** collected with **<5% missing data**.
* Clean CSV dataset produced.
* Organized Git repo with clear commits.

### **Minimum Essential**

* Scrape **at least 400 reviews per bank**.
* Commit a preprocessing script.
* Update README.md with methodology.

---

## **Task 2: Sentiment and Thematic Analysis**

Quantify review sentiment and identify themes to uncover satisfaction drivers and pain points.

### **Tasks**

#### **Sentiment Analysis**

* Use **distilbert-base-uncased-finetuned-sst-2-english** for sentiment scoring.
* Optionally compare with VADER or TextBlob.
* Aggregate results by bank and rating.

#### **Thematic Analysis**

A *theme* is a recurring concept or topic in user reviews.

##### Keyword Extraction & Clustering

* Extract keywords and n-grams using TF-IDF or spaCy.
* Optionally use topic modeling for clustering.
* Group related keywords into **3–5 core themes per bank** (e.g., *UI/UX*, *Login Issues*, *Performance*, *Support*, *Feature Requests*).
* Document grouping logic.

#### **Pipeline**

* Preprocessing using tokenization, stop-word removal, lemmatization if helpful.
* Save results as CSV (`review_id`, `review_text`, `sentiment_label`, `sentiment_score`, `identified_theme`).
* Implement keyword extraction.
* Cluster into themes.

#### **Git Workflow**

* Use **“task-2” branch**.
* Commit scripts and merge using pull requests.

### **KPIs**

* Sentiment scores for **90%+** of reviews.
* **3+ themes per bank** with supporting examples.
* Modular pipeline code.

### **Minimum Essential**

* Sentiment for **400+ reviews**.
* At least **2 themes per bank**.
* Commit full analysis script.
