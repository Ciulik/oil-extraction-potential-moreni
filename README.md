# 🛢️ Historical Data Science: The Lost Wealth of Moreni (1948-2026)

## 📌 Overview
This project is an end-to-end Data Science and Applied Mathematics pipeline exploring a counterfactual economic scenario. It analyzes the historical oil extraction in Moreni, Romania—once a global hub for standard oil companies—and calculates the theoretical current value of a Sovereign Wealth Fund had the profits been retained locally. 

The architecture combines automated data ingestion, advanced Aspect-Based Sentiment Analysis (ABSA) on historical Dutch archives, physical well-decline regression, and stochastic financial modeling.

<img width="613" height="515" alt="image" src="https://github.com/user-attachments/assets/cabfe532-65ab-4d84-8467-3acc18749a39" />

link for demo (auto-download html) (https://media.base44.com/files/public/6a56ce2da4ebc6d6e69009b0/1ee18bb70_Digital_Twin_HeatMap_Moreni.html)


## ⚙️ Architecture & Pipeline
1. **Data Ingestion (`extragere_masiva_api.py`)**: Automated SRU API scraper communicating with the National Library of the Netherlands (Delpher), extracting 3,000+ historical documents regarding Astra Română operations.
2. **Aspect-Based Sentiment Analysis (`absa_nlp.py`)**: Dual-model NLP architecture running on a local CUDA environment. Utilizes `mDeBERTa-v3-base-mnli-xnli` for zero-shot aspect classification and `bert-base-multilingual-uncased-sentiment` for polarity extraction.
3. **Physical Modeling (`arps_decline_moreni.py`)**: Models reservoir depletion using the Arps Exponential Decline curve via non-linear least squares optimization (`scipy.optimize`).
4. **Financial Integration & Monte Carlo (`vizualizare_si_monte_carlo.py`)**: Maps NLP sentiment scores as dynamic weights adjusting historical production volumes, executing a 1,000-iteration Monte Carlo simulation accounting for historical market volatility.

## 📊 Key Findings
- **NLP Insights:** Historical reporting was heavily skewed towards financial metrics, with "Accidents" generating extreme negative polarity, highlighting early 20th-century extraction conditions.
- **Financial Projection:** The median projection places the 2026 value of the local fund at ~$9.82 Billion USD, demonstrating the mathematical power of compound interest over physical resource extraction.

## 🚀 Tech Stack
- **Languages:** Python
- **Libraries:** pandas, numpy, scipy, scikit-learn
- **Deep Learning:** transformers, torch (CUDA)
- **Data Visualization:** matplotlib, seaborn, folium

## 🛠️ How to Run Locally
To replicate the environment and execute the pipeline:
1. **Clone and Navigate:** `git clone https://github.com/Ciulik/oil-extraction-potential-moreni.git && cd oil-extraction-potential-moreni`
2. **Install Dependencies:** `pip install -r requirements.txt` (Ensure PyTorch is compiled with CUDA for faster NLP inference).
3. **Environment Setup (Optional):** Create a `.env` file in the root directory if future API integrations require specific credentials.
4. **Execute Pipeline:**
   - Data Extraction: `python extragere_masiva_api.py`
   - Sentiment Analysis: `python absa_nlp.py`
   - Financial Simulation: `python vizualizare_si_monte_carlo.py`
