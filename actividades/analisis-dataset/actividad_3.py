import sys
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dataset-medios"
if not (BASE_DIR / "envios_medios.csv").exists():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent / "proyectos" / "dataset-medios"

sys.path.append(str(BASE_DIR))

try:
    from usar_modelo import es_posible
except ImportError:
    es_posible = None

def main():
    csv_path = BASE_DIR / "envios_medios.csv"
    modelo_path = BASE_DIR / "modelo_medios.joblib"

    if not csv_path.exists() or not modelo_path.exists():
        print(f"Error: Verifique que existan {csv_path} y {modelo_path}")
        return

    datos = pd.read_csv(csv_path)
    modelo = joblib.load(modelo_path)

    # Separar datos igual que en paso 4
    x = datos.drop(columns=["medio_recomendado", "id_envio"], errors="ignore")
    y = datos["medio_recomendado"]

    x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=42
    )

    predicciones = modelo.predict(x_prueba)
    df_eval = x_prueba.copy()
    df_eval["real"] = y_prueba
    df_eval["predicho"] = predicciones
    df_eval["error"] = df_eval["real"] != df_eval["predicho"]

    total_errores = df_eval["error"].sum()
    total_prueba = len(df_eval)
    print(f"=== TOTAL DE ERRORES: {total_errores} de {total_prueba} ({total_errores/total_prueba*100:.2f}%) ===")
    print(f"Exactitud en prueba: {(1 - total_errores/total_prueba)*100:.2f}%\n")

    print("=== MATRIZ / CONFUSIONES MÁS FRECUENTES ===")
    confusiones = df_eval[df_eval["error"]].groupby(["real", "predicho"]).size().sort_values(ascending=False)
    print(confusiones.head(10))
    print()

    print("=== ERRORES: ERA MOTO Y EL MODELO PREDICHO DRON ===")
    moto_a_dron = df_eval[(df_eval["real"] == "moto") & (df_eval["predicho"] == "dron")]
    print(f"Total moto -> dron: {len(moto_a_dron)}")
    if len(moto_a_dron) > 0:
        de_noche = ((moto_a_dron["hora_salida"] < 6) | (moto_a_dron["hora_salida"] >= 21)).sum()
        print(f"De noche (<6 o >=21): {de_noche} de {len(moto_a_dron)}")

        if es_posible:
            corrige_reglas = moto_a_dron.apply(lambda r: not es_posible("dron", r), axis=1)
            print(f"Casos donde las reglas descartan el dron (imposible): {corrige_reglas.sum()}")
            print(f"Casos donde el dron sí era posible físicamente pero el operador eligió moto: {(~corrige_reglas).sum()}")
    print()

    print("=== ERRORES: ERA MOTO Y EL MODELO PREDICHO BICICLETA ===")
    moto_a_bici = df_eval[(df_eval["real"] == "moto") & (df_eval["predicho"] == "bicicleta")]
    print(f"Total moto -> bicicleta: {len(moto_a_bici)}")
    if len(moto_a_bici) > 0:
        print("Resumen de distancia en estos errores:")
        print(moto_a_bici["distancia_km"].describe().round(2))
        print("Comparado con bicicletas acertadas:")
        bici_acertadas = df_eval[(df_eval["real"] == "bicicleta") & (df_eval["predicho"] == "bicicleta")]
        print(bici_acertadas["distancia_km"].describe().round(2))

if __name__ == "__main__":
    main()
