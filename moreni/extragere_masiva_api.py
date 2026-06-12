import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

def extrage_delpher_api_masiv(query="Moreni", max_rezultate=5000):
    print(f"Începem extracția masivă pentru '{query}' (Țintă: {max_rezultate} articole)...")
    url = "http://jsru.kb.nl/sru/sru"
    articole_totale = []
    
    # Paginare din 500 în 500 pentru a nu copleși serverul
    pas = 500 
    
    for start_record in range(1, max_rezultate + 1, pas):
        print(f" Extragem setul {start_record} - {min(start_record + pas - 1, max_rezultate)}...")
        
        params = {
            'version': '1.2',
            'operation': 'searchRetrieve',
            'x-collection': 'DDD_artikel', 
            'query': query,
            'maximumRecords': pas,
            'startRecord': start_record
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespaces = {'srw': 'http://www.loc.gov/zing/srw/', 'dc': 'http://purl.org/dc/elements/1.1/'}
            records = root.findall('.//srw:record', namespaces)
            
            if not records:
                print(" Nu mai sunt rezultate disponibile pe server.")
                break
                
            for record in records:
                titlu = record.find('.//dc:title', namespaces)
                data_pub = record.find('.//dc:date', namespaces)
                
                # Extragem doar anul pentru a ne fi mai ușor la regresia financiară
                an_publicare = None
                if data_pub is not None:
                    # Unele date sunt "1929-05-28", luăm doar primii 4 indici
                    an_publicare = data_pub.text[:4] if len(data_pub.text) >= 4 else None
                
                articole_totale.append({
                    'Anul': an_publicare,
                    'Titlu': titlu.text if titlu is not None else 'Fără titlu'
                })
                
            # Pauză de politețe pentru a evita Timeout/Ban
            time.sleep(2.5)
            
        except Exception as e:
            print(f" Eroare la pachetul curent: {e}")
            break
            
    df_rezultate = pd.DataFrame(articole_totale)
    # Curățăm datele unde anul nu este valid
    df_rezultate = df_rezultate.dropna(subset=['Anul', 'Titlu'])
    # Convertim anul la număr întreg pentru calculele viitoare
    df_rezultate['Anul'] = pd.to_numeric(df_rezultate['Anul'], errors='coerce')
    df_rezultate = df_rezultate.dropna(subset=['Anul'])
    
    df_rezultate.to_csv("master_dataset_moreni.csv", index=False)
    print(f"\nSucces! Am extras {len(df_rezultate)} articole și le-am salvat în 'master_dataset_moreni.csv'.")

if __name__ == "__main__":
    extrage_delpher_api_masiv("Moreni", max_rezultate=13530) # Poți crește numărul