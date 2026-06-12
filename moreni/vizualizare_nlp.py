import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def vizualizeaza_rezultate():
    print("1. Încărcăm rezultatele NLP...")
    try:
        df = pd.read_csv("rezultate_finale_nlp.csv")
    except FileNotFoundError:
        print("Eroare: Nu găsesc rezultate_finale_nlp.csv!")
        return
    
    # Modelul multilingv returnează formatul "X stars". Extragem strict cifra.
    df['Stele'] = df['Sentiment_Stele'].str.extract('(\d)').astype(int)

    # --- PARTEA 1: VIZUALIZAREA DATELOR ---
    # Setăm un design curat și profesional pentru grafice
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 5))

    # Graficul A: Distribuția generală a sentimentelor (1 - 5 stele)
    plt.subplot(1, 2, 1)
    sns.countplot(data=df, x='Stele', palette='RdYlGn')
    plt.title('Cum privea presa olandeză Moreniul?')
    plt.xlabel('Sentiment (1 = Panică/Negativ, 5 = Entuziasm/Pozitiv)')
    plt.ylabel('Număr de Articole')

    # Graficul B: Cât de sigur a fost modelul pe predicțiile lui?
    plt.subplot(1, 2, 2)
    sns.histplot(data=df, x='Scor_Incredere', bins=15, kde=True, color='indigo')
    plt.title('Distribuția Încrederii (Confidence Score)')
    plt.xlabel('Siguranța modelului (0.0 - 1.0)')
    plt.ylabel('Frecvență')

    plt.tight_layout()
    # Salvăm imaginea direct pe disk pentru a o putea include într-un raport
    nume_grafic = "grafic_sentiment_moreni.png"
    plt.savefig(nume_grafic, dpi=300)
    print(f"2. Succes! Graficele au fost salvate în '{nume_grafic}'.")

    # --- PARTEA 2: SANITY CHECK (Testarea riguroasă) ---
    print("\n=== SANITY CHECK: Analiza Extremelor ===")
    print("Verificăm dacă modelul face sens logic izolând predicțiile cu cea mai mare încredere matematică.\n")
    
    pozitive = df[df['Stele'] >= 4].nlargest(3, 'Scor_Incredere')
    negative = df[df['Stele'] <= 2].nlargest(3, 'Scor_Incredere')
    
    print("🟢 Top 3 cele mai POZITIVE articole:")
    for _, row in pozitive.iterrows():
        print(f"   [Încredere: {row['Scor_Incredere']:.2f}] {row['Titlu']}")
        
    print("\n🔴 Top 3 cele mai NEGATIVE/PESIMISTE articole:")
    for _, row in negative.iterrows():
        print(f"   [Încredere: {row['Scor_Incredere']:.2f}] {row['Titlu']}")

if __name__ == "__main__":
    vizualizeaza_rezultate()