import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

# 1. Definim strict ecuația matematică pentru declinul exponențial Arps
def arps_exponential(t, qi, D):
    return qi * np.exp(-D * t)

def ruleaza_regresie_arps():
    print("--- INIȚIALIZARE MODEL MATEMATIC: DECLIN MORENI ---")
    
    # 2. Generăm date istorice simulate (ex: din 1950 până în 2000)
    # Timpul t = 0 reprezintă anul 1950
    ani = np.arange(0, 51, 2) 
    ani_reali = ani + 1950
    
    # Presupunem un vârf de 5 milioane barili și o rată de declin reală ascunsă de 0.08
    qi_adevarat = 5_000_000
    D_adevarat = 0.08
    
    # Generăm producția teoretică și adăugăm "zgomot" (fluctuații economice, greve, etc.)
    zgomot = np.random.normal(0, 300_000, size=len(ani))
    productie_reala = arps_exponential(ani, qi_adevarat, D_adevarat) + zgomot
    
    # Ne asigurăm că producția nu scade sub zero din cauza zgomotului statistic
    productie_reala = np.maximum(productie_reala, 0)
    
    # 3. Executăm Curve Fitting (Minimizarea non-liniară a celor mai mici pătrate)
    print("Rulăm algoritmul de optimizare (Levenberg-Marquardt)...")
    
    # P0 reprezintă estimările inițiale [qi_estimat, D_estimat] pentru a ajuta convergența matricei
    estimari_initiale = [4_000_000, 0.05]
    
    parametri_optimi, matrice_covarianta = curve_fit(
        arps_exponential, 
        ani, 
        productie_reala, 
        p0=estimari_initiale
    )
    
    qi_calculat, D_calculat = parametri_optimi
    
    print("\n--- REZULTATELE REGRESIEI ---")
    print(f"Producția inițială calculată (qi): {qi_calculat:,.0f} barili (Adevărat: {qi_adevarat:,})")
    print(f"Rata de declin calculată (D):      {D_calculat:.4f} (Adevărat: {D_adevarat})")
    
    # 4. Evaluăm calitatea modelului matematic
    productie_prezisa = arps_exponential(ani, qi_calculat, D_calculat)
    mse = mean_squared_error(productie_reala, productie_prezisa)
    rmse = np.sqrt(mse)
    print(f"Eroarea Pătratică Medie (RMSE):    {rmse:,.0f} barili")
    
    # 5. Vizualizarea datelor
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background') # Un fundal negru pentru contrast maxim
    
    # Plotăm datele zgomotoase
    plt.scatter(ani_reali, productie_reala, color='cyan', label='Date Istorice Extrase (cu zgomot)', zorder=5)
    
    # Plotăm curba perfectă calculată de matrice
    plt.plot(ani_reali, productie_prezisa, color='magenta', linewidth=2, 
             label=f'Curba Arps (Regresie)\n$q_i$={qi_calculat:,.0f}, $D$={D_calculat:.3f}')
    
    plt.title('Regresia Declinului Extracției de Petrol - Modelul Arps', fontsize=14)
    plt.xlabel('Anul', fontsize=12)
    plt.ylabel('Producție (Barili)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    nume_grafic = 'regresie_arps_moreni.png'
    plt.savefig(nume_grafic, dpi=300)
    print(f"\nGraficul a fost salvat cu succes ca '{nume_grafic}'.")

if __name__ == "__main__":
    ruleaza_regresie_arps()