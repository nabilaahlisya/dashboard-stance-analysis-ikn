# IKN Public Opinion Analysis

**Machine Learning and BERTopic for Stance Classification and Topic Identification of Public Opinions Regarding the Relocation of Indonesia's Capital City (IKN)**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![BERTopic](https://img.shields.io/badge/BERTopic-Topic%20Modeling-orange)
![Status](https://img.shields.io/badge/Status-Undergraduate%20Thesis-success)

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Machine Learning Results](#machine-learning-results)
- [BERTopic Analysis](#bertopic-analysis)
- [Flask Application](#flask-application)
- [Tools & Technologies](#tools--technologies)
- [Project Structure](#project-structure)
- [Model Files](#model-files)
- [How to Run](#how-to-run)
- [Research Context](#research-context)
- [Author](#author)

## Project Overview

This project analyzes public opinions regarding the **relocation of Indonesia's capital city (Ibu Kota Nusantara/IKN)** using Machine Learning and topic modeling.

The analysis focuses on identifying public stance toward the relocation of IKN into three categories:
* **Pro**
* **Contra**
* **Neutral**

In addition, **BERTopic** is applied to identify and explore the main topics discussed within public opinion data.

This project was developed as part of an undergraduate thesis in Information Systems.

## Objectives

* Classify public opinions regarding the relocation of IKN into Pro, Contra, and Neutral stances.
* Compare the performance of several Machine Learning algorithms using different n-gram representations and train-test split scenarios.
* Identify discussion topics within public opinion using BERTopic.
* Develop a Flask-based prototype for stance prediction and data visualization.

## Dataset

The dataset consists of Indonesian-language public opinion data collected from **X (formerly Twitter)** related to the relocation of Indonesia's capital city.

**Data collection period:**
January 1, 2024 – August 31, 2025

**Final labeled dataset:**
4,400 data points

The dataset underwent several preprocessing and data cleaning steps, including:

* Removing duplicate data
* Filtering texts containing fewer than three words
* Filtering non-Indonesian content
* Data cleaning and normalization
* Manual stance labeling

### Stance Categories

| Category | Description                                                   |
| -------- | ------------------------------------------------------------- |
| Pro      | Opinions supporting the relocation of IKN                     |
| Contra   | Opinions opposing the relocation of IKN                       |
| Neutral  | Opinions that do not clearly support or oppose the relocation |

## Methodology

The project consists of two main analytical approaches:

### 1. Stance Classification
Five Machine Learning algorithms were evaluated:
* Random Forest
* Decision Tree
* Logistic Regression
* Support Vector Machine (SVM)
* K-Nearest Neighbors (KNN)

Text features were represented using:
* Unigram
* Bigram
* Trigram

Three train-test split scenarios were evaluated:
* 90:10
* 80:20
* 70:30

In total, **45 experimental configurations** were evaluated.

### 2. Topic Modeling

**BERTopic** was used to identify topics within public opinion data.

The topic modeling process used:

* Sentence Transformer: `all-MiniLM-L6-v2`
* Minimum topic size: 30
* Outlier topic filtering

The identified topics were analyzed based on representative words and the public opinions associated with each topic.

## Machine Learning Results

The experimental results showed differences in classification performance across algorithms, n-gram representations, and train-test split scenarios.

One of the strongest experimental configurations was:
**Random Forest + Bigram + 90:10 train-test split**

The configuration achieved approximately:
* **Accuracy:** 0.80
* **Weighted F1-score:** 0.80

The complete experimental results and model comparisons are available in the project notebooks.

## BERTopic Analysis

BERTopic was applied to discover recurring themes within public discussions surrounding the relocation of IKN.

The topic modeling workflow includes:
1. Text preprocessing
2. Sentence embedding generation
3. Dimensionality reduction
4. Clustering
5. Topic representation
6. Topic interpretation

The resulting topics were visualized to support exploration of major themes discussed in public opinion.

## Flask Application

A Flask-based prototype was developed to demonstrate the implementation of the research results.

The application provides features including:
* Stance prediction from text input
* CSV data upload
* Date-based filtering
* Stance distribution visualization
* Topic visualization

The Flask application currently runs locally and serves as a prototype for demonstrating the analytical workflow.

## Tools & Technologies

### Programming & Data Analysis
* Python
* Pandas
* NumPy
* Scikit-learn

### Natural Language Processing
* NLP
* N-gram
* Sentence Transformers
* BERTopic

### Visualization & Web Application
* Matplotlib
* WordCloud
* Flask
* HTML
* CSS

### Development Environment
* Jupyter Notebook
* Google Colab

## Project Structure

```text
dashboar-stance-analyst-ikn/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── install_venv.bat                # Script to set up virtual environment
├── run_app.bat                     # Script to run the Flask app
├── README.md
│
├── utils/                          # Helper modules (preprocessing, prediction, etc.)
├── templates/                      # HTML templates for the Flask app
├── static/                         # CSS, JS, and static assets
│
├── model_terbaik.pkl               # Best stance classification model (download separately, see below)
├── model_terbaik_pipeline.pkl      # Full preprocessing + model pipeline (download separately)
├── vectorizer_terbaik.pkl          # Text vectorizer used by the model (download separately)
├── model_bertopic                  # Trained BERTopic model (download separately)
├── embedding_model_bertopic.pkl    # Sentence embedding model for BERTopic (download separately)
│
└── venv/                           # Local virtual environment (not pushed to GitHub)
```

> Note: `venv/`, `python-3.13.0-amd64.exe`, and any local upload folders are excluded from the repository via `.gitignore`. Trained model files are not stored in this repository due to their size — see [Model Files](#model-files) below.

## Model Files

The trained model files used by this application are not included in this repository because of their file size. Download them from Google Drive and place them in the root of the project folder before running the app:

**Download link:** [Model files (Google Drive)](https://drive.google.com/drive/folders/1xSjQY361FQf4UwPF7Oey6sJhzc_ktNU9?usp=sharing)

Files to place in the project root:
* `model_terbaik.pkl`
* `model_terbaik_pipeline.pkl`
* `vectorizer_terbaik.pkl`
* `model_bertopic`
* `embedding_model_bertopic.pkl`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/nabilaahlisya/dashboard-stance-analysis-ikn.git
cd dashboard-stance-analysis-ikn
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Alternatively, on Windows you can run the provided setup script:

```bash
install_venv.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the trained model files

Download the model files from the [Google Drive link](#model-files) above and place them in the project root folder (same level as `app.py`).

### 5. Run the Flask application

```bash
python app.py
```

Or, on Windows:

```bash
run_app.bat
```

Then open the local address displayed in the terminal, usually:

```text
http://127.0.0.1:5000/
```

## Research Context

This project was developed as part of an undergraduate thesis:
**"Komparasi Kinerja Algoritma Machine Learning dengan Pendekatan BERTopic untuk Analisis Stance dan Identifikasi Topik pada Opini Publik Terkait IKN"**

The research compares Machine Learning algorithms for stance classification and applies BERTopic to identify topics within public opinions regarding the relocation of Indonesia's capital city.

## Author

**Nabila Ahlisya Fatir**

Information Systems Graduate
UPN "Veteran" Jawa Timur

Interested in **Data Analytics, Business Analytics, and Machine Learning**.
