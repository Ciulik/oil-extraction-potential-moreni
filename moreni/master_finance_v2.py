import numpy as np
import pandas as pd

def ruleaza_model_hibrid():
    print("=== MODEL FINANCIAR HIBRID: ARPS + ABSA ===")
    
    # 1. PARAMETRII FIZICI AI ZĂCĂMÂNTULUI
    qi_calculat = 4_850_000
    D_calculat = 0.08       
    
    # 2. ÎNCĂRCAREA DATELOR NLP
    try:
        df_nlp = pd.read_csv("rezultate_absa_moreni.csv")
    except FileNotFoundError:
        print("Eroare: Rulează mai întâi absa_nlp.py!")
        return

    # Construim o logică de penalizare/boost pe baza aspectului
    # Regula: Dacă e ACCIDENT și sentiment negativ (1-2), e un dezastru pe schelă (-20% producție anuala)
    # Dacă e FINANCIAR și sentiment pozitiv (4-5), e un an cu profit și extracție uriașă (+15%)
    def calculeaza_impact_anual(row):
        aspect = row['Aspect_Detectat']
        sentiment = row['Sentiment_Stele']
        
        if aspect == 'ACCIDENT' and sentiment <= 2:
            return -0.20
        elif aspect == 'FINANCIAR' and sentiment >= 4:
            return 0.15
        elif aspect == 'GREVA' and sentiment <= 2:
            return -0.10
        elif aspect == 'TEHNOLOGIE' and sentiment >= 4:
            return 0.05
        return 0.0 # Neutru

    df_nlp['Impact_Economic'] = df_nlp.apply(calculeaza_impact_anual, axis=1)
    
    # Agregăm impactul mediu pe fiecare AN
    impact_pe_an = df_nlp.groupby('Anul')['Impact_Economic'].mean().reset_index()
    dict_impact = dict(zip(impact_pe_an['Anul'], impact_pe_an['Impact_Economic']))

    # 3. SIMULAREA FINANCIARĂ
    ani_simulare = np.arange(0, 79) 
    ani_reali = ani_simulare + 1948
    
    productie_baza = qi_calculat * np.exp(-D_calculat * ani_simulare)
    productie_ajustata = np.zeros(len(ani_simulare))
    
    for i, an in enumerate(ani_reali):
        # Dacă avem date NLP pentru anul respectiv, aplicăm multiplicatorul
        # 1.0 = Producție normală (baseline). Dacă impactul e -0.20, multiplicatorul e 0.80.
        multiplicator = 1.0 + dict_impact.get(an, 0.0) 
        productie_ajustata[i] = productie_baza[i] * multiplicator

    pret_mediu_usd = 45.0 
    venit_brut_anual = productie_ajustata * pret_mediu_usd
    
    redeventa_locala = venit_brut_anual * 0.15
    rata_dobanda = 0.06
    ani_investiti = 2026 - ani_reali
    
    fond_suveran_2026 = redeventa_locala * (1 + rata_dobanda)**ani_investiti
    
    valoare_fond_total = np.sum(fond_suveran_2026)
    total_barili_extrasi = np.sum(productie_ajustata)
    
    print(f"\n🛢️ Total petrol extras (Arps + Integrare ABSA completă): {total_barili_extrasi:,.0f} barili")
    print(f"💰 VALOAREA FINALĂ FOND SUVERAN (2026): ${valoare_fond_total / 1_000_000_000:.2f} MILIARDE USD\n")

if __name__ == "__main__":
    ruleaza_model_hibrid()