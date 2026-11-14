import sys
from pathlib import Path
import pandas as pd

# Buscar ruta de dataset-medios
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dataset-medios"
if not (BASE_DIR / "envios_medios.csv").exists():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent / "proyectos" / "dataset-medios"

sys.path.append(str(BASE_DIR))

def main():
    csv_path = BASE_DIR / "envios_medios.csv"
    if not csv_path.exists():
        print(f"Error: No se encontró {csv_path}")
        return

    datos = pd.read_csv(csv_path)

    print("=== 1. TABLA HORA DE SALIDA VS MEDIO RECOMENDADO ===")
    tabla_hora = pd.crosstab(datos["hora_salida"], datos["medio_recomendado"])
    print(tabla_hora)
    print()

    print("=== 2. HORAS SIN DRONES ===")
    if "dron" in tabla_hora.columns:
        horas_sin_dron = tabla_hora[tabla_hora["dron"] == 0].index.tolist()
        print(f"Horas con 0 drones: {horas_sin_dron}")
    print()

    print("=== 3. ENVÍOS DE NOCHE VS DÍA ===")
    # Noche: antes de las 6 o desde las 21 (es decir, horas < 6 o >= 21)
    es_noche = (datos["hora_salida"] < 6) | (datos["hora_salida"] >= 21)
    total_noche = es_noche.sum()
    total_dia = (~es_noche).sum()
    total = len(datos)
    print(f"Total envíos noche (<6 o >=21): {total_noche} ({total_noche/total*100:.2f}%)")
    print(f"Total envíos día (6 a 20): {total_dia} ({total_dia/total*100:.2f}%)")
    print()

    print("=== 4. CAMBIO ENTRE 20:00 Y 21:00 ===")
    filtro_20_21 = tabla_hora.loc[[20, 21]] if 20 in tabla_hora.index and 21 in tabla_hora.index else "No disponible"
    print(filtro_20_21)

if __name__ == "__main__":
    main()
