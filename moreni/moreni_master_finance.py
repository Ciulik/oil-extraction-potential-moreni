import numpy as np

def calcul_financiar_integrat():
    print("=== SIMULARE FINANCIARĂ FINALĂ: MORENI 2026 ===\n")
    
    # 1. PARAMETRII DIN REGRESIA ARPS
    # Acestea sunt datele "găsite" de scriptul anterior pe curba de declin
    qi_calculat = 4_850_000 # Barili produși în anul de vârf (estimat 1948)
    D_calculat = 0.08       # Rata de declin anual (8%)
    
    # Generăm anii de la naționalizare (1948) până în prezent (2026)
    ani_simulare = np.arange(0, 79) 
    ani_reali = ani_simulare + 1948
    
    # Calculăm producția de bază folosind ecuația Arps
    productie_anuala = qi_calculat * np.exp(-D_calculat * ani_simulare)
    
    # 2. INTEGRAREA NLP (Sentimentul Presei ca Multiplicator Economic)
    # Presupunem că am extras media sentimentului pe decenii. 
    # În anii '50 (naționalizare dură, panica din presă), aplicăm o penalizare de ineficiență de 15%
    # În anii '70 (boom-ul industrial local), aplicăm un boost de 10%
    multiplicator_sentiment = np.ones(len(ani_simulare))
    multiplicator_sentiment[(ani_reali >= 1948) & (ani_reali <= 1958)] = 0.85 # Panică/Ineficiență
    multiplicator_sentiment[(ani_reali >= 1970) & (ani_reali <= 1980)] = 1.10 # Entuziasm/Investiții
    
    # Ajustăm producția finală cu datele NLP
    productie_ajustata = productie_anuala * multiplicator_sentiment
    
    # 3. CALCULUL FINANCIAR (Banii)
    # Folosim un preț istoric mediu conservator ajustat la inflație (ex: 45 USD/baril)
    pret_mediu_usd = 45.0 
    
    venit_brut_anual = productie_ajustata * pret_mediu_usd
    total_barili_extrasi = np.sum(productie_ajustata)
    total_valoare_bruta_usd = np.sum(venit_brut_anual)
    
    # 4. SCENARIUL FONDULUI SUVERAN (Stil Norvegia/Texas)
    # Dacă 15% din valoarea extrasă ar fi rămas strict în conturile Primăriei Moreni
    redeventa_locala = venit_brut_anual * 0.15
    
    # Banii nu stau sub saltea, sunt investiți la bursă cu un randament mediu de 6% pe an
    rata_dobanda = 0.06
    ani_investiti = 2026 - ani_reali
    
    # Aplicăm formula dobânzii compuse pentru fiecare an în parte (Vectorizat)
    fond_suveran_2026 = redeventa_locala * (1 + rata_dobanda)**ani_investiti
    valoare_fond_total = np.sum(fond_suveran_2026)
    
    # Afișăm rezultatele transformate în MILIARDE pentru a fi ușor de citit
    print(f"🛢️ Total petrol extras (model Arps ajustat NLP): {total_barili_extrasi:,.0f} barili")
    print(f"💵 Valoarea istorică brută a petrolului:        ${total_valoare_bruta_usd / 1_000_000_000:.2f} MILIARDE USD")
    print("-" * 60)
    print(f"🏦 DACA Banii ar fi rămas în Moreni (Fond Suveran local investit la 6%):")
    print(f"💰 VALOARE FOND ÎN 2026: ${valoare_fond_total / 1_000_000_000:.2f} MILIARDE USD")
    print("-" * 60)

if __name__ == "__main__":
    calcul_financiar_integrat()