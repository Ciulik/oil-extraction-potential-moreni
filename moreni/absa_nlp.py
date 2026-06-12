import pandas as pd
import torch
from transformers import pipeline

def ruleaza_absa_istoric():
    print("1. Citim dataset-ul masiv...")
    df = pd.read_csv("master_dataset_moreni.csv")
    # Pentru un test rapid poți lăsa .head(200), apoi scoți limitarea
    df = df.head(3384) 
    
    device_id = 0 if torch.cuda.is_available() else -1
    
    print("2. Încărcăm modelele NLP pe GPU...")
    # Modelul Zero-Shot pentru detectarea Aspectului (Subiectului)
    aspect_classifier = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
        device=device_id
    )
    
    # Modelul pentru Sentiment
    sentiment_classifier = pipeline(
        "sentiment-analysis", 
        model="nlptown/bert-base-multilingual-uncased-sentiment", 
        device=device_id, 
        truncation=True
    )
    
    etichete_aspect = ['financiële winst', 'werkongeluk', 'werknemersstaking', 'technologie']
    
    rezultate_aspecte = []
    rezultate_sentimente = []
    
    print("3. Rulăm inferența ABSA...")
    for idx, row in df.iterrows():
        text = row['Titlu']
        
        # 1. Detectăm despre CE vorbește (Aspect)
        pred_aspect = aspect_classifier(text, candidate_labels=etichete_aspect)
        aspect_câștigător = pred_aspect['labels'][0] # Luăm eticheta cu cea mai mare probabilitate
        
        # 2. Detectăm CUM vorbește (Sentiment: 1 = Negativ, 5 = Pozitiv)
        pred_sentiment = sentiment_classifier(text)[0]
        stele = int(pred_sentiment['label'].split()[0])
        
        rezultate_aspecte.append(aspect_câștigător)
        rezultate_sentimente.append(stele)
        
        if idx % 50 == 0 and idx > 0:
            print(f"   Procesat {idx}/{len(df)} documente...")

    df['Aspect_Detectat'] = rezultate_aspecte
    df['Sentiment_Stele'] = rezultate_sentimente
    
    # Traducem în coduri pentru a le integra matematic
    mapare_aspecte = {
        'financiële winst': 'FINANCIAR',
        'werkongeluk': 'ACCIDENT',
        'werknemersstaking': 'GREVA',
        'technologie': 'TEHNOLOGIE'
    }
    df['Aspect_Detectat'] = df['Aspect_Detectat'].map(mapare_aspecte)
    
    df.to_csv("rezultate_absa_moreni.csv", index=False)
    print("\nFișierul 'rezultate_absa_moreni.csv' a fost generat cu succes!")

if __name__ == "__main__":
    ruleaza_absa_istoric()