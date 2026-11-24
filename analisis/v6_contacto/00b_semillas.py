"""Fase 0: semillas por persona. Salida: research/v6_contacto/semillas_{antonia,tomas}.csv
Conceptos: research/v5_nube/conceptos_*.csv (peso/100, sin ruido). Rasgos: perfiles v5 (entregables/cliente_ideal).
Excluye género, nombre y comuna (la comuna entra solo como contraste en 01_afinidad.py)."""
import csv, pathlib
ROOT = pathlib.Path("/Users/betosanchez/portillo-personas")
OUT = ROOT/"research/v6_contacto"
RASGOS = {
 "antonia": [
  ("uso","auto de uso diario para ir al trabajo, al colegio de los hijos y a actividades familiares",0.6,"PERFIL_ANTONIA: uso y detonante"),
  ("detonante","auto actual con años y la familia necesita más espacio",0.6,"PERFIL_ANTONIA: detonante"),
  ("como_llega","llega por relación de confianza con la sucursal y recomendación de conocidos",0.6,"PERFIL_ANTONIA: cómo llega"),
  ("valora","recibir el auto limpio, ordenado y bien presentado, con trato cercano y atento",0.6,"PERFIL_ANTONIA: valora"),
  ("teme","tasación del auto actual que no calza y entrega sin fecha o con documentos pendientes",0.6,"PERFIL_ANTONIA: teme"),
  ("estilo_HIPOTESIS","escapadas de fin de semana con la familia",0.4,"PERFIL_ANTONIA: viajes de fin de semana (HIPÓTESIS)"),
  ("estilo_HIPOTESIS","vida familiar en barrio de oriente con acceso a parques y naturaleza",0.3,"HIPÓTESIS, contexto de entorno sin comuna"),
  ("estilo_HIPOTESIS","cocina y bienestar en casa con la familia",0.2,"HIPÓTESIS"),
 ],
 "tomas": [
  ("como_llega","compara seminuevos en varios portales y lee reseñas antes de ir a la sucursal",0.6,"PERFIL_TOMAS: cómo llega"),
  ("valora","ficha completa del vehículo, historial y precio transparente igual al publicado",0.6,"PERFIL_TOMAS: valora"),
  ("valora","respuesta rápida al aviso y prueba de manejo agendada",0.6,"PERFIL_TOMAS: valora"),
  ("teme","garantía corta y ficha o año distintos a lo publicado",0.6,"PERFIL_TOMAS: teme"),
  ("uso","auto para el trayecto diario y la compra de un vehículo con datos claros",0.5,"PERFIL_TOMAS: uso"),
 ],
}
COMUNAS = {"condes","vitacura","providencia","la dehesa","lo barnechea","las condes"}
def concepts(path, persona):
    rows=[]
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cluster"].startswith("ruido") or float(r["peso"])<30: continue
            if r["concepto"].lower() in COMUNAS: continue  # comuna no es variable del modelo (Fase 0/4)
            rows.append((f"c_{persona}_{r['concepto']}", "concepto", r["concepto"], round(float(r["peso"])/100*0.5,3), f"research/v5_nube/conceptos_{persona}.csv ({r['cluster']})"))
    return rows
def main():
    for persona, cfile in [("antonia","conceptos_antonia.csv"),("tomas","conceptos_tomas.csv")]:
        rows = concepts(ROOT/"research/v5_nube"/cfile, persona)
        for i,(k,texto,peso,fuente) in enumerate(RASGOS[persona]):
            rows.append((f"r_{persona}_{i:02d}", k, texto, peso, fuente))
        with open(OUT/f"semillas_{persona}.csv","x",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["id","tipo_semilla","texto","peso","fuente"]); w.writerows(rows)
        print(persona, len(rows), "semillas")
if __name__=="__main__": main()
