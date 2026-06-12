# oil-extraction-potential-moreni
***made in 4 h at 1 am out of pure curiosity of the 1st city of Romania that extracted petrol (3rd in the world) and wanted to see what it could have achieved  if better circumstances happened.  

# 🛢️ Historical Data Science: The Lost Wealth of Moreni (1948-2026)

## 📌 Overview
This project is an end-to-end Data Science and Applied Mathematics pipeline that explores a counterfactual economic scenario. It analyzes the historical oil extraction in Moreni, Romania—once a global hub for standard oil companies—and calculates the theoretical current value of a Sovereign Wealth Fund had the profits been retained locally, modeled after the Texas or Norwegian financial systems.

The architecture combines automated data ingestion, advanced Aspect-Based Sentiment Analysis (ABSA) on historical Dutch archives, physical well-decline regression, and stochastic financial modeling.

## ⚙️ Architecture & Pipeline

1. **Data Ingestion (`extragere_masiva_api.py`)**
   - Implemented an automated SRU API scraper communicating with the National Library of the Netherlands (Delpher).
   - Extracted over 3,000 historical documents regarding the Astra Română oil operations.

2. **Aspect-Based Sentiment Analysis (`absa_nlp.py`)**
   - Deployed a dual-model NLP architecture running on a local CUDA environment.
   - **Zero-Shot Classification:** Used `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` to categorize 100-year-old Dutch text into aspects (Finance, Accidents, Strikes, Technology).
   - **Sentiment Extraction:** Applied `nlptown/bert-base-multilingual-uncased-sentiment` to gauge the polarity of the reporting.

3. **Physical Modeling (`arps_decline_moreni.py`)**
   - Modeled the physical depletion of the Tuicani plateau reservoir using the Arps Exponential Decline curve equation via non-linear least squares optimization (`scipy.optimize`).

4. **Financial Integration & Monte Carlo (`master_finance_v2.py` & `vizualizare_si_monte_carlo.py`)**
   - Mapped the NLP sentiment scores as dynamic weights adjusting the historical production volumes (e.g., negative sentiment linked to 'Accidents' implies a drop in production).
   - Ran a Monte Carlo simulation (1000 parallel iterations) factoring in historical market volatility and systemic shocks (e.g., 1973 Oil Crisis, 2008 Financial Crash) to calculate the 2026 median value of the hypothetical fund.

## 📊 Key Findings

![Monte Carlo Simulation](simulare_monte_carlo_moreni.png)

* **NLP Insights:** Historical reporting was overwhelmingly skewed towards financial metrics. "Accidents" and "Strikes" generated extreme, polarized sentiment scores, highlighting the brutal nature of early 20th-century extraction.
* **Financial Projection:** The median projection places the 2026 value of the local fund at **~$9.82 Billion USD**, demonstrating the overwhelming power of compound interest over physical resource extraction across an 80-year horizon.

## 🚀 Tech Stack
* **Languages:** Python
* **Libraries:** `pandas`, `numpy`, `scipy`, `scikit-learn`
* **Deep Learning:** `transformers`, `torch` (CUDA)
* **Data Visualization:** `matplotlib`, `seaborn`
* **Network:** `requests`, `xml.etree`

## 🛠️ How to run
1. Install dependencies: `pip install -r requirements.txt` *(make sure PyTorch is compiled with CUDA for faster inference)*.
2. Run data extraction: `python extragere_masiva_api.py`
3. Execute the NLP pipeline: `python absa_nlp.py`
4. Generate the final Monte Carlo simulation: `python vizualizare_si_monte_carlo.py`
