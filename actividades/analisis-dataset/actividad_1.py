import sys
from pathlib import Path
import pandas as pd

# Importar constantes y funciones de validación de dataset-medios
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dataset-medios"
sys.path.append(str(BASE_DIR))

from usar_modelo import LIMITES, es_posible

def main():
    csv_path = BASE_DIR / "envios_medios.csv"
    datos = pd.read_csv(csv_path)

    print("=== 1. CLIMA VS MEDIO RECOMENDADO (PORCENTAJES) ===")
    tabla_clima = pd.crosstab(datos["clima"], datos["medio_recomendado"], normalize="index") * 100
    print(tabla_clima.round(2))
    print()

    print("=== 2. ZONA DESTINO VS MEDIO RECOMENDADO (PORCENTAJES) ===")
    tabla_zona = pd.crosstab(datos["zona_destino"], datos["medio_recomendado"], normalize="index") * 100
    print(tabla_zona.round(2))
    print()

    print("=== 3. RESUMEN DE DISTANCIA, PESO Y VOLUMEN POR MEDIO (MIN, MEDIAN, MAX) ===")
    resumen_metricas = datos.groupby("medio_recomendado")[["distancia_km", "peso_kg", "volumen_l"]].agg(["min", "median", "max"])
    print(resumen_metricas.round(2))
    print()

    print("=== 4. LÍMITES TEÓRICOS (LIMITES) ===")
    for medio, lim in LIMITES.items():
        print(f"{medio}: {lim}")
    print()

    print("=== 5. VALIDACIÓN DE REGLAS CON es_posible ===")
    # Revisar si cada fila cumple las reglas según su etiqueta asignada
    cumple_reglas = datos.apply(lambda fila: es_posible(fila["medio_recomendado"], fila), axis=1)
    violaciones = (~cumple_reglas).sum()
    print(f"Total de envíos: {len(datos)}")
    print(f"Envíos que rompen las reglas del negocio: {violaciones} ({violaciones / len(datos) * 100:.2f}%)")
    print()

    print("=== 6. DISTANCIA POR ZONA DESTINO (BICI EN PERIFERIA) ===")
    print(datos.groupby("zona_destino")["distancia_km"].agg(["min", "median", "mean", "max"]).round(2))
    bici_periferia = len(datos[(datos["medio_recomendado"] == "bicicleta") & (datos["zona_destino"] == "periferia")])
    total_bici = len(datos[datos["medio_recomendado"] == "bicicleta"])
    print(f"\nBicicletas en periferia: {bici_periferia} de {total_bici} bicicletas ({bici_periferia/total_bici*100:.2f}%)")
    print()

    print("=== 7. CAMIONETAS EN VIAJES DE MENOS DE 2 KM ===")
    camionetas_cortas = datos[(datos["medio_recomendado"] == "camioneta") & (datos["distancia_km"] < 2.0)]
    print(f"Total de camionetas < 2 km: {len(camionetas_cortas)}")

    # Razones claras para ir en camioneta:
    # 1. Es refrigerado (solo camioneta puede)
    # 2. Peso > 25 kg (supera a moto y bici y dron)
    # 3. Volumen > 90 L (supera a moto y bici y dron)
    # 4. Peso > 8 kg o Volumen > 40 L si no pudiera moto por alguna razón
    razon_clara = camionetas_cortas[
        (camionetas_cortas["refrigerado"] == 1) | 
        (camionetas_cortas["peso_kg"] > 25.0) | 
        (camionetas_cortas["volumen_l"] > 90.0)
    ]
    sin_razon_clara = camionetas_cortas[~camionetas_cortas.index.isin(razon_clara.index)]

    print(f"Con razón técnica indiscutible (refrigerado, peso > 25kg o vol > 90L): {len(razon_clara)}")
    print(f"Sin una de esas tres razones directas: {len(sin_razon_clara)}")
    if len(sin_razon_clara) > 0:
        print("\nDetalle de las que no tienen razón técnica estricta:")
        print(sin_razon_clara[["peso_kg", "volumen_l", "fragil", "valor_declarado_mxn", "trafico", "prioridad"]].describe().round(2))

if __name__ == "__main__":
    main()
