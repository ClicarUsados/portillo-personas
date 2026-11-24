"""Promotores Portillo Usados de sucursales de zona oriente (base de Javiera y Tomás Pascual).
Cómo reproducirlo: python3 analisis/v3_oriente_promotores.py
Fuente: inputs_clean/CR_2025-Venta-Usados_*.parquet, campaña "2025 - Venta Usados Portillo".
Zona oriente = sucursales con LA DEHESA, BILBAO, LAS CONDES, LUIS CARRERA, PADRE HURTADO, VITACURA o DELANO [HIPÓTESIS de mapeo].
Solo conteos; no imprime PII ni nombres de vendedores."""
import glob, pandas as pd
f = glob.glob('inputs_clean/CR_2025-Venta-Usados_*.parquet')[0]
d = pd.read_parquet(f); d = d[d['campaña o sensor'] == '2025 - Venta Usados Portillo']
nps = [c for c in d.columns if c.startswith('En base a tu')][0]
d['nps'] = pd.to_numeric(d[nps], errors='coerce')
ori = d['nombre_concesionario'].fillna('').str.contains(r'LA DEHESA|BILBAO|LAS CONDES|LUIS CARRERA|PADRE HURTADO|VITACURA|DELANO', regex=True)
d['zona'] = ori.map({True: 'oriente', False: 'resto'})
print(d.groupby('zona').agg(n=('nps', 'size'), promotores=('nps', lambda s: (s >= 9).sum())))
p = d[d.nps >= 9]
print(pd.crosstab(p['¿Cómo llegaste a #empresa# para comprar tu auto?'], p['zona']))
print(pd.crosstab(p['Vehículo en parte de pago'].astype(str), p['zona']))
po = p[p.zona == 'oriente']
print(po['nombre_concesionario'].value_counts())
print(po['des_marca'].value_counts().head(10))
print(po['des_modelo'].astype(str).str.contains(r'RAV ?4', regex=True).sum(), 'RAV4 de', len(po))
mc = [c for c in d.columns if c.startswith('Macrocategoría') and '.' not in c]
print(pd.concat([po[c] for c in mc]).dropna().value_counts())
print(po[[c for c in d.columns if c.startswith('Dada tu')][0]].value_counts())
