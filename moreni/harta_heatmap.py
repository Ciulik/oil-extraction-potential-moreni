import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import numpy as np

print("1. Încărcăm datele istorice...")
df = pd.read_csv(r'D:\Desktop\moreni\cache\main\rezultate_absa_moreni.csv')

# Dicționarul pentru dispersie (Jittering)
coordonate_hardcodate = {
    "astra romana": [44.9877, 25.6434],
    "romano-american": [44.9755, 25.6480],
    "koninklijke": [44.9617, 25.6571], 
    "steaua romana": [44.9800, 25.6500],
    "tuicani": [44.9920, 25.6350],
    "160": [44.9900, 25.6380]
}

def extrage_si_disperseaza(titlu):
    if pd.isna(titlu): return None
    titlu_lower = str(titlu).lower()
    for cheie, coords in coordonate_hardcodate.items():
        if cheie in titlu_lower:
            return [coords[0] + np.random.normal(0, 0.0005), coords[1] + np.random.normal(0, 0.0005)]
    return [44.9827 + np.random.normal(0, 0.005), 25.6404 + np.random.normal(0, 0.008)]

df['Coords'] = df['Titlu'].apply(extrage_si_disperseaza)
df_clean = df.dropna(subset=['Coords', 'Anul']).copy()

df_clean['Latitudine'] = df_clean['Coords'].apply(lambda x: x[0])
df_clean['Longitudine'] = df_clean['Coords'].apply(lambda x: x[1])

# ==========================================
# REZOLVAREA BUG-ULUI "UNIX EPOCH 1970"
# ==========================================
# Ne asigurăm că anii sunt strict numere întregi
df_clean['Anul'] = df_clean['Anul'].astype(int)
# Generăm lista unică și sortată a anilor
ani_sortati = sorted(list(df_clean['Anul'].unique()))

print(f"Pregătim animația pentru {len(ani_sortati)} ani (inclusiv perioada de dinainte de 1970)...")

# Construim datele pentru HeatMap
heat_data = []
for an in ani_sortati:
    date_an = df_clean[df_clean['Anul'] == an][['Latitudine', 'Longitudine']].values.tolist()
    heat_data.append(date_an)

m_heat = folium.Map(location=[44.985, 25.645], zoom_start=14, tiles='CartoDB dark_matter')

# ==========================================
# 1. HEATMAP-UL CARE PULSEAZĂ
# ==========================================
HeatMapWithTime(
    heat_data,
    # Aici este cheia: trecem anii ca STRING-uri (text simplu), ocolind astfel limitările de timp din JavaScript
    index=[str(an) for an in ani_sortati], 
    auto_play=True,
    radius=35, 
    gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1.0: 'red'},
    min_opacity=0.4,
    max_opacity=0.9,
    use_local_extrema=True
).add_to(m_heat)

# ==========================================
# 2. ANCORELE STATICE (CLICKABILE)
# ==========================================
print("Adăugăm ancorele pe care poți da click pentru a citi articolele...")
evenimente_extreme = df_clean[(df_clean['Sentiment_Stele'] == 1) | (df_clean['Sentiment_Stele'] == 5)]
# Selectăm un eșantion pentru a nu încărca abuziv memoria browserului
evenimente_extreme = evenimente_extreme.sample(n=min(100, len(evenimente_extreme)), random_state=42)

for index, row in evenimente_extreme.iterrows():
    culoare_ancora = 'red' if row['Sentiment_Stele'] == 1 else 'lime'
    
    html_popup = f"""
    <div style='min-width: 250px; font-family: Arial, sans-serif;'>
        <h4 style='margin-bottom: 5px; color: {culoare_ancora};'>Eveniment Major ({row['Anul']})</h4>
        <p style='font-size: 13px; color: #333;'><b>Articol:</b> <i>{row['Titlu']}</i></p>
        <hr style='margin: 5px 0;'>
        <p style='font-size: 12px; margin: 0;'><b>Aspect:</b> {row['Aspect_Detectat']}</p>
    </div>
    """
    
    # Punem puncte foarte mici pe hartă, care rămân permanent acolo
    # Când HeatMap-ul ajunge la anul respectiv, va părea că "aprinde" acest punct
    folium.CircleMarker(
        location=[row['Latitudine'], row['Longitudine']],
        radius=3, # Foarte fin, ca să nu distrugă estetica HeatMap-ului
        color='white',
        weight=1,
        fill=True,
        fill_color=culoare_ancora,
        fill_opacity=0.9,
        popup=folium.Popup(html_popup, max_width=300)
    ).add_to(m_heat)

m_heat.save('Digital_Twin_Moreni_HeatMap_Perfect.html')
print("Gata! Ecranul alb a dispărut, anii vechi s-au întors, iar articolele pot fi citite.")