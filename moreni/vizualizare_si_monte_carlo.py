import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analizeaza_absa_si_simuleaza():
    # Setăm stilul vizual
    sns.set_theme(style="darkgrid")
    
    print("=== PARTEA 1: ANALIZA NLP (Ce au discutat olandezii?) ===")
    try:
        df_nlp = pd.read_csv("rezultate_absa_moreni.csv")
        
        # Creăm o figură cu 2 grafice pentru analiza textelor
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Graficul 1: Frecvența Aspectelor
# Înlocuiește vechea linie cu aceasta:
        sns.countplot(data=df_nlp, x='Aspect_Detectat', hue='Aspect_Detectat', palette='viridis', legend=False, ax=axes[0])
        axes[0].set_title('Distribuția Subiectelor în Presă')
        axes[0].set_ylabel('Număr Articole')
        
        # Graficul 2: Sentimentul per Aspect
# Înlocuiește vechea linie cu aceasta:
        sns.boxplot(data=df_nlp, x='Aspect_Detectat', y='Sentiment_Stele', hue='Aspect_Detectat', palette='magma', legend=False, ax=axes[1])
        axes[1].set_title('Sentimentul asociat fiecărui subiect')
        axes[1].set_ylabel('Stele (1 = Negativ, 5 = Pozitiv)')
        
        plt.tight_layout()
        plt.savefig("analiza_subiecte_moreni.png", dpi=300)
        print(" Graficele NLP au fost salvate ca 'analiza_subiecte_moreni.png'.")
        
    except FileNotFoundError:
        print(" Eroare: Nu am găsit fișierul 'rezultate_absa_moreni.csv'. Sărim peste ploturile NLP.")

    print("\n=== PARTEA 2: SIMULAREA MONTE CARLO & DINAMICA FONDULUI ===")
    
    # Parametrii fizici (extracția de bază)
    qi = 4_850_000
    D = 0.08
    ani = np.arange(0, 79) # 1948 -> 2026
    ani_reali = ani + 1948
    
    productie_anuala = qi * np.exp(-D * ani)
    venit_brut_anual = productie_anuala * 45.0 # Preț mediu USD
    depozit_anual_fond = venit_brut_anual * 0.15 # 15% redevență
    
    # Setări Monte Carlo
    numar_simulari = 1000
    randament_mediu = 0.07   # 7% creștere medie pe an la bursă
    volatilitate = 0.15      # 15% deviație standard (risc/fluctuație normală)
    
    # Matrice pentru a stoca toate cele 1000 de traiectorii (79 de ani x 1000 simulări)
    valoare_fond_mc = np.zeros((len(ani), numar_simulari))
    
    # Executăm simulările
    for sim in range(numar_simulari):
        valoare_curenta = 0
        for i, an in enumerate(ani_reali):
            # Generăm randamentul stocastic al anului respectiv
            r_anual = np.random.normal(randament_mediu, volatilitate)
            
            # Adăugăm șocuri economice hardcodate
            if an == 1973: r_anual -= 0.25  # Criza Petrolului (Crash bursier)
            if an == 2000: r_anual -= 0.20  # Dot-Com Bubble
            if an == 2008: r_anual -= 0.35  # Marea Criză Financiară
            
            # Aplicăm randamentul pe valoarea fondului din anul precedent + depozitul nou
            valoare_curenta = valoare_curenta * (1 + r_anual) + depozit_anual_fond[i]
            valoare_fond_mc[i, sim] = valoare_curenta

    # Extragem statistici din cele 1000 de universuri paralele
    mediana_fondului = np.median(valoare_fond_mc, axis=1)
    percentila_5 = np.percentile(valoare_fond_mc, 5, axis=1)   # Cel mai ghinionist scenariu
    percentila_95 = np.percentile(valoare_fond_mc, 95, axis=1) # Cel mai norocos scenariu

    # Generăm Graficul Dual (Producție vs Fond) cu intervalele Monte Carlo
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Axa stângă: Producția fizică de petrol (în declin)
    color1 = 'tab:red'
    ax1.set_xlabel('Anul')
    ax1.set_ylabel('Producție Petrol (Barili)', color=color1)
    ax1.plot(ani_reali, productie_anuala, color=color1, linewidth=2, label='Declin Zăcământ (Arps)')
    ax1.tick_params(axis='y', labelcolor=color1)

    # Axa dreaptă: Valoarea Fondului Suveran (în creștere)
    ax2 = ax1.twinx()  
    color2 = 'tab:blue'
    ax2.set_ylabel('Valoare Fond (Miliarde USD)', color=color2)
    
    # Plotăm traiectoria mediană și intervalul de încredere (zona umbrită) din Monte Carlo
    ax2.plot(ani_reali, mediana_fondului / 1e9, color='blue', linewidth=2, label='Valoare Mediană Fond (Monte Carlo)')
    ax2.fill_between(ani_reali, percentila_5 / 1e9, percentila_95 / 1e9, color='blue', alpha=0.2, 
                     label='Interval de Risc (90% din scenarii)')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Marcam Crizele Istorice
    ax2.axvline(x=1973, color='orange', linestyle='--', alpha=0.7, label='1973: Șocul Petrolier')
    ax2.axvline(x=2008, color='black', linestyle='--', alpha=0.7, label='2008: Criză Financiară')

    plt.title('Dinamica Moreni: Epuizarea Resurselor vs. Creșterea prin Dobândă Compusă & Risc')
    
    # Combinăm legendele de pe ambele axe
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig("simulare_monte_carlo_moreni.png", dpi=300)
    print(" Graficul Monte Carlo a fost salvat ca 'simulare_monte_carlo_moreni.png'.")
    
    print(f"\n💵 Scenariul Median în 2026: ${mediana_fondului[-1] / 1e9:.2f} MILIARDE USD")
    print(f"📉 Scenariul Pesimist (Top 5% ghinion): ${percentila_5[-1] / 1e9:.2f} MILIARDE USD")
    print(f"📈 Scenariul Optimist (Top 5% noroc): ${percentila_95[-1] / 1e9:.2f} MILIARDE USD")

if __name__ == "__main__":
    analizeaza_absa_si_simuleaza()