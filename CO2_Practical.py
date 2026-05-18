import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
# ==================================

filename = "CO2_Practical.csv"
df = pd.read_csv(filename)
n = len(df)

print(f"✅ Set de date încărcat cu succes. Observații (n) = {n}\n")

# ==================================
# REGRESSION & ANOVA
# ==================================
# Variabila Independentă (X) = Emisii Totale
# Variabila Dependentă (Y) = Consum de Gaz
X = df['Emisii_Totale_tone_CO2']
Y = df['Emisii_de_CO2_Estimat'] + df['Emisii_de_CO2_Reziduu']

# Adăugăm constanta (Intercept / b0) pentru statsmodels
X_stat = sm.add_constant(X)
model = sm.OLS(Y, X_stat).fit()

#  REGRESSION
print("="*40)
print(" 1. REZULTATE REGRESIE (COEFICIENȚI)")
print("="*40)
print(f"Intercept (b0): {model.params['const']:.4f}")
print(f"Panta (b1): {model.params['Emisii_Totale_tone_CO2']:.4f}")
print(f"R-squared: {model.rsquared:.4f}")

# ANOVA
print("\n" + "="*40)
print(" 2. TABEL ANOVA (Analiza Varianței)")
print("="*40)
# Tabel ANOVA generat nativ din statsmodels (NU SUPORTA ANOVA_LM() CE NECESITA FORMULE TIP R)
# anova_table = sm.stats.anova_lm(model, typ=1)

# anova_data = {
#     'df': [model.df_model, model.df_resid, model.df_],
#     'sum_sq': [model.ess, model.ssr, model.sst],
#     'mean_sq': [model.mse_model, model.mse_resid],
#     'F': [model.fvalue, float('nan')],
#     'PR(>F)': [model.f_pvalue, float('nan')]
# }
# anova_table = pd.DataFrame(anova_data, index=['Model (Regresie)', 'Residual (Eroare)'])
# pd.options.display.float_format = '{:,.4f}'.format
# print(anova_table)

anova_data = [
    [int(model.df_model), model.ess, model.mse_model, model.fvalue, model.f_pvalue],
    [int(model.df_resid), model.ssr, model.mse_resid, "", ""],
    [int(model.df_model + model.df_resid), model.centered_tss, "", "", ""]
]

# Definim coloanele și rândurile exact ca în Excel
anova_table = pd.DataFrame(
    anova_data, 
    columns=['df', 'SS', 'MS', 'F', 'Significance F'], 
    index=['Regression', 'Residual', 'Total']
)

# Formatăm numerele ca să fie identice cu output-ul din Excel
pd.options.display.float_format = '{:.5f}'.format 
print(anova_table)

# ==================================
# HYPOTHESIS TESTING & Z-CALCULATIONS
# ==================================
reziduuri = model.resid

# Parametrii eșantionului:  Media, deviația standard, eroarea standard
mu_esantion = np.mean(reziduuri)
sigma_esantion = np.std(reziduuri, ddof=1) 
eroare_standard = sigma_esantion / np.sqrt(n)

# Formularea ipotezelor (H0 și H1)
# H0: mu = 0 (Modelul este bun)
# H1: mu != 0 (Modelul are o eroare sistematică)
mu_ipoteza = 0   # Aceasta este valoarea pe care o presupune H0

# Calculul Z-Statistic (Z Test)
z_stat = (mu_esantion - mu_ipoteza) / eroare_standard

# Calculul Z-Critic pentru Nivel de Încredere 95% și 98% (Two-tailed / Bilateral)
z_crit_95 = stats.norm.ppf(1 - 0.05/2)   # z ~ 1.96)
z_crit_98 = stats.norm.ppf(1 - 0.02/2)   # z ~ 2.33)

print("\n" + "="*40)
print(" 3. TESTAREA IPOTEZEI Z (GAUSS-LAPLACE)")
print("="*40)
print(f"Media reziduurilor din eșantion (μ): {mu_esantion:.4f}")   # Suma tuturor reziduurilor dă întotdeauna zero
print(f"Deviația Standard (σ): {sigma_esantion:.4f}")
print(f"Eroarea Standard (SE): {eroare_standard:.4f}\n")

print(f"Z calculat (Z-Statistic): {z_stat:.4f}")
print(f"Z critic (95% Confidence): ±{z_crit_95:.4f}")
print(f"Z critic (98% Confidence): ±{z_crit_98:.4f}")

# Concluzia testului (95%)
if abs(z_stat) > z_crit_95:
    print("\nCONCLUZIE (95%): Respingem H0.")
    print("Explicație: Z-calculat a depășit granița Z-critic.")
    print("Modelul are un bias semnificativ statistic (media reziduurilor nu este 0).")
else:
    print("\nCONCLUZIE (95%): Acceptăm (Nu putem respinge) H0.")
    print(f"Explicație: Z-calculat a căzut în regiunea de acceptare (între -{z_crit_95:.2f} și +{z_crit_95:.2f}).")
    print("Media reziduurilor = 0")
    # print("Diferența dintre media reziduurilor și 0 este doar o coincidență statistică. Modelul este ne-distorsionat.")

# Concluzia testului (98%)
if abs(z_stat) > z_crit_98:
    print("\nCONCLUZIE (98%): Respingem H0.")
    print("Explicație: Z-calculat a depășit granița Z-critic.")
    print("Modelul are un bias semnificativ statistic (media reziduurilor nu este 0).")
else:
    print("\nCONCLUZIE (98%): Acceptăm (Nu putem respinge) H0.")
    print(f"Explicație: Z-calculat a căzut în regiunea de acceptare (între -{z_crit_98:.2f} și +{z_crit_98:.2f}).")

# ==================================
# PLOTTING: DISTRIBUȚIA NORMALĂ (Gauss-Laplace)
# ==================================
plt.style.use('seaborn-v0_8-darkgrid')

# Creăm o figură cu 2 sub-grafice (1 rând, 2 coloane)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# --- GRAFICUL 1: REGRESIA LINIARĂ ---
ax1.scatter(X, Y, color='royalblue', s=60, alpha=0.7, edgecolor='black', label='Date Reale')

# Creăm punctele pentru a desena linia perfectă de regresie
x_line = np.linspace(X.min(), X.max(), 100)
x_line_stat = sm.add_constant(x_line)
y_line = model.predict(x_line_stat)

ax1.plot(x_line, y_line, color='crimson', linewidth=2.5, label='Linie de Regresie (OLS)')

ax1.set_title('Regresia Liniară: Emisii CO2 vs Consum Gaz', fontsize=14, fontweight='bold')
ax1.set_xlabel('Emisii Totale de CO2 (tone)', fontsize=12)
ax1.set_ylabel('Consum Gaz (Estimat + Reziduu)', fontsize=12)
ax1.legend(loc='upper left', fontsize=11)

# --- GRAFICUL 2: DISTRIBUȚIA NORMALĂ (Gauss-Laplace) ---
ax2.hist(reziduuri, bins=20, density=True, alpha=0.6, color='royalblue', 
         edgecolor='black', label='Frecvența Reziduurilor')

xmin, xmax = ax2.get_xlim()
x_gauss = np.linspace(xmin, xmax, 100)
y_gauss = stats.norm.pdf(x_gauss, mu_esantion, sigma_esantion)

ax2.plot(x_gauss, y_gauss, 'k-', linewidth=2.5, color='crimson', 
         label=f'Curba Gauss-Laplace\n(μ={mu_esantion:.2f}, σ={sigma_esantion:.2f})')

# Liniile pentru Z-Critic 95%
x_crit_low = mu_esantion - (z_crit_95 * sigma_esantion)
x_crit_high = mu_esantion + (z_crit_95 * sigma_esantion)

ax2.axvline(x_crit_low, color='green', linestyle='--', linewidth=2, label=f'Z-Critic 95% Inf. ({x_crit_low:.2f})')
ax2.axvline(x_crit_high, color='green', linestyle='--', linewidth=2, label=f'Z-Critic 95% Sup. ({x_crit_high:.2f})')
ax2.axvline(mu_esantion, color='black', linestyle=':', linewidth=2, label='Media (μ)')

ax2.set_title(f'Distribuția Normală a Reziduurilor (n={n})', fontsize=14, fontweight='bold')
ax2.set_xlabel('Eroare Reziduală', fontsize=12)
ax2.set_ylabel('Densitate de Probabilitate', fontsize=12)
ax2.legend(loc='upper right', fontsize=10)

# Afișează ferestrele de grafice (Matplotlib)
plt.tight_layout()
plt.show()

# ==================================
# PLOTTING: DISTRIBUȚIA NORMALĂ (Gauss-Laplace)
# ==================================
# Folosim aceiași parametri calculați anterior (mu_esantion, sigma_esantion, z_crit_98)
plt.style.use('seaborn-v0_8-darkgrid')
fig3, ax3 = plt.subplots(figsize=(10, 6))

# Histograma reziduurilor
ax3.hist(reziduuri, bins=20, density=True, alpha=0.6, color='royalblue', 
         edgecolor='black', label='Frecvența Reziduurilor')

# Creăm axa X pentru curba teoretică (lărgim puțin limitele pentru a vizualiza bine liniile depărtate de 98%)
xmin, xmax = ax3.get_xlim()
x_gauss_98 = np.linspace(xmin - 5, xmax + 5, 100)
y_gauss_98 = stats.norm.pdf(x_gauss_98, mu_esantion, sigma_esantion)

# Trasăm curba Gauss
ax3.plot(x_gauss_98, y_gauss_98, 'k-', linewidth=2.5, color='crimson', 
         label=f'Curba Gauss-Laplace\n(μ={mu_esantion:.2f}, σ={sigma_esantion:.2f})')

# Calculăm și adăugăm liniile Z-Critic pentru 98%
x_crit_low_98 = mu_esantion - (z_crit_98 * sigma_esantion)
x_crit_high_98 = mu_esantion + (z_crit_98 * sigma_esantion)

ax3.axvline(x_crit_low_98, color='purple', linestyle='--', linewidth=2.5, 
            label=f'Z-Critic 98% Inf. ({x_crit_low_98:.2f})')
ax3.axvline(x_crit_high_98, color='purple', linestyle='--', linewidth=2.5, 
            label=f'Z-Critic 98% Sup. ({x_crit_high_98:.2f})')

# Adăugăm valoarea Mediei (care este 0)
ax3.axvline(mu_esantion, color='black', linestyle=':', linewidth=2, label='Media Eșantionului (μ)')

# Formatare și detalii vizuale
ax3.set_title(f'Distribuția Normală a Reziduurilor (n={n})\nTestul Z cu Nivel de Încredere 98%', 
              fontsize=14, fontweight='bold', pad=15)
ax3.set_xlabel('Eroare Reziduală (Real - Predicție)', fontsize=12)
ax3.set_ylabel('Densitate de Probabilitate', fontsize=12)
ax3.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()