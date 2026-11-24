"""Fase 1: universo de candidatos. Salida: research/v6_contacto/universo_candidatos.csv
Fuentes: IAB Content Taxonomy 3.1 (descargada de GitHub, ver fuentes/), Google Ads (support.google.com), URLs [WEB] consultadas 2026-11-24.
Lo que no tiene URL verificada queda con verificado=NO y NO entra al ranking."""
import csv, pathlib
ROOT = pathlib.Path("/Users/betosanchez/portillo-personas/research/v6_contacto")
IAB_URL = "https://github.com/InteractiveAdvertisingBureau/Taxonomies/blob/main/Content%20Taxonomies/Content%20Taxonomy%203.1.tsv"
FECHA = "2026-11-24"

# id IAB -> tipo
IAB_PICK = {
 "665":"actividad","666":"interes","670":"actividad","673":"lugar","677":"actividad","679":"actividad","667":"interes","662":"lugar",
 "159":"actividad","160":"lugar",
 "492":"actividad","531":"actividad","504":"actividad","539":"actividad","512":"actividad","500":"actividad","505":"actividad",
 "499":"actividad","227":"actividad","226":"actividad","225":"interes","549":"actividad","520":"actividad",
 "255":"interes","216":"interes","218":"interes","215":"interes","279":"interes","280":"interes","284":"interes",
 "283":"interes","277":"interes","275":"interes","247":"interes",
 "192":"interes",
 "18":"interes","23":"interes","6":"interes","30":"interes","35":"interes","36":"interes","25":"interes","22":"interes",
 "404":"interes","407":"interes",
 "370":"medio","371":"medio","376":"medio",
 "425":"interes",
}

def load_iab():
    rows = {}
    with open(ROOT/"fuentes"/"iab_content_3.1.tsv", encoding="utf-8") as f:
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) >= 4 and cols[0].strip().isdigit():
                rows[cols[0].strip()] = [cols[2].strip(), cols[3].strip(), cols[4].strip()]  # Name, Tier1, Tier2 (col 9+ es extension)
    return rows

# Candidatos locales y de calendario con URL consultada (ver fuentes en PLAN_PUNTOS / METODO)
WEB = [
 ("L01","Cajón del Maipo (destino)","deportes y naturaleza","cordillera","lugar","Sernatur / chile.travel","https://chile.travel/en/where-to-go/destination/cajon-del-maipo"),
 ("L02","Trekking El Morado","deportes y naturaleza","trekking cordillera","actividad","chile.travel","https://chile.travel/itinerarios/el-morado-trekking-a-glaciares-cerca-de-santiago/"),
 ("L03","Excursiones naturales de un día cerca de Santiago","escapadas","día de naturaleza","actividad","chile.travel","https://chile.travel/blog/7-excursiones-naturales-cerca-de-santiago-que-puedes-realizar-en-un-dia/"),
 ("L04","Esquí Valle Nevado","invierno","esquí","actividad","The Clinic (30-oct-2026)","https://www.theclinic.cl/2026/10/30/valle-nevado-extendera-la-temporada-de-esqui-hasta-el-1-de-diciembre-y-proyecta-superar-las-310-mil-visitas/"),
 ("L05","Centros de ski cerca de Santiago, temporada 2026","invierno","esquí","actividad","chile.travel","https://chile.travel/blog/centros-de-ski-cerca-de-santiago-que-debes-visitar-esta-temporada-2026/"),
 ("L06","Running en Parque Bicentenario","deportes urbanos","running","actividad","ESPN Run","https://espndeportes.espn.com/espn-run/nota/_/id/7797035/lugares-para-correr-parque-bicentenario-santiago-de-chile-tips-espn-run"),
 ("L07","Rutas en bicicleta en Santiago y alrededores","deportes urbanos","ciclismo urbano","actividad","chile.travel","https://chile.travel/blog/rutas-en-bicicleta-para-recorrer-en-santiago-y-sus-alrededores/"),
 ("L08","Pádel en Chile","deportes urbanos","pádel","actividad","FIP (padelfip.com, 2025-03)","https://www.padelfip.com/2025/03/focus-on-chile-a-nation-on-the-podium-of-american-padel/"),
 ("L09","Dónde jugar pádel en la Región Metropolitana","deportes urbanos","pádel","lugar","Al Aire Libre","https://www.alairelibre.cl/polideportivo/donde-jugar-padel-en-la-region-metropolitana/"),
 ("L10","Escapada a playas cercanas a Santiago (itinerario de tres días)","escapadas","costa central","lugar","chile.travel","https://chile.travel/?p=55456"),
 ("L11","Playas del litoral central para ir en el día","escapadas","costa central","lugar","Encancha (06-mar-2026)","https://www.encancha.cl/enlahora/panoramas/2026/03/06/tres-maravillosas-playas-escondidas-del-litoral-central-que-puedes-visitar-en-el-dia-para-una-desconexion-total/"),
 ("L12","Escapada de Semana Santa cerca de Santiago","escapadas","fin de semana largo","momento","Meteored","https://www.meteored.cl/noticias/actualidad/5-lugares-perfectos-para-una-escapada-cerca-de-santiago-en-semana-santa.html"),
 ("L13","Fiestas Patrias (18-19 sep)","calendario","Fiestas Patrias","momento","El Mostrador (05-sep-2026); día de semana inconsistente en otra fuente","https://www.elmostrador.cl/datos-utiles/2026/09/05/feriados-de-fiestas-patrias-revisa-cuantos-dias-libres-seran-este-2026/"),
 ("L14","Vacaciones de invierno escolares RM (22-jun a 3-jul 2026)","calendario","vacaciones de invierno","momento","CNN Chile (según calendario Mineduc, prensa)","https://www.cnnchile.com/servicios/vacaciones-invierno-escolares-2026/"),
 ("L15","Inicio de clases y vuelta a clases (marzo)","calendario","vuelta a clases","momento","La Tercera (calendario Mineduc 2026)","https://www.latercera.com/nacional/noticia/clases-desde-el-4-de-marzo-y-vacaciones-de-invierno-diferenciadas-por-region-mineduc-da-a-conocer-el-calendario-escolar-2026/"),
 ("L16","Escapadas de verano a playa desde Santiago (menos de dos horas)","escapadas","verano playa","momento","El Mostrador Jengibre (27-ene-2026)","https://www.elmostrador.cl/revista-jengibre/viajes/2026/01/27/escapadas-de-verano-desde-santiago-tres-destinos-de-playa-a-menos-de-dos-horas-de-la-capital/"),
 ("G01","Afinidad Google: Vegetarians & Vegans","afinidad Google Ads","alimentación","interes","Google Ads Help (support.google.com/google-ads/answer/2497941)","https://support.google.com/google-ads/answer/2497941"),
 ("G02","Afinidad Google: Green Living Enthusiasts","afinidad Google Ads","estilo de vida","interes","Google Ads Help","https://support.google.com/google-ads/answer/2497941"),
 ("G03","Afinidad Google: Weightlifters","afinidad Google Ads","fitness","interes","Google Ads Help","https://support.google.com/google-ads/answer/2497941"),
 ("G04","Afinidad Google: Yoga Lovers","afinidad Google Ads","fitness","interes","Google Ads Help","https://support.google.com/google-ads/answer/2497941"),
 ("G05","Afinidad Google: Golf Enthusiasts","afinidad Google Ads","deportes","interes","Google Ads Help","https://support.google.com/google-ads/answer/2497941"),
]

# Sin URL verificada: no entran al ranking
NO_VER = [
 ("N01","Intereses de Meta Ads (lista pública)","Meta Ads","interes","NO VERIFICADO: no se encontró lista pública de intereses consultable"),
 ("N02","Radios locales de conversación de Santiago oriente","medios","medio","NO VERIFICADO: búsqueda no realizada"),
 ("N03","Podcasts de autos y seminuevos en Chile","medios","medio","NO VERIFICADO: búsqueda no realizada"),
 ("N04","Newsletters de movilidad y autos en Chile","medios","medio","NO VERIFICADO: búsqueda no realizada"),
 ("N05","Cuentas locales de running o ciclismo urbano en Santiago","comunidades","comunidad","NO VERIFICADO: búsqueda no realizada"),
 ("N06","Escapada al sur (Pucón, Villarrica) desde Santiago","escapadas","sur","NO VERIFICADO: búsqueda no realizada"),
]

def main():
    iab = load_iab()
    out = []
    for iid, tipo in IAB_PICK.items():
        if iid not in iab:
            print("ID IAB no encontrado:", iid); continue
        path = iab[iid]
        # path: [tier1, tier2?, name...] ; usamos tier1 como categoria y ultimo como nombre
        nombre, cat, sub = path[0], path[1], path[2]
        out.append(dict(id=f"I{iid}", nombre=nombre, categoria=cat, subcategoria=sub, tipo=tipo,
                        fuente="IAB Content Taxonomy 3.1", url=IAB_URL, verificado="SI",
                        fecha_consulta=FECHA, iab_id=iid))
    for r in WEB:
        out.append(dict(id=r[0], nombre=r[1], categoria=r[2], subcategoria=r[3], tipo=r[4],
                        fuente=r[5], url=r[6], verificado="SI", fecha_consulta=FECHA, iab_id=""))
    for r in NO_VER:
        out.append(dict(id=r[0], nombre=r[1], categoria=r[2], subcategoria="", tipo=r[3],
                        fuente=r[4], url="", verificado="NO", fecha_consulta=FECHA, iab_id=""))
    cols = ["id","nombre","categoria","subcategoria","tipo","fuente","url","verificado","fecha_consulta","iab_id"]
    with open(ROOT/"universo_candidatos.csv","x",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    n_ver = sum(1 for r in out if r["verificado"]=="SI")
    print(f"total={len(out)} con_url={n_ver} no_verificado={len(out)-n_ver}")

if __name__ == "__main__":
    main()
