import sys
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dataset-medios"
if not (BASE_DIR / "envios_medios.csv").exists():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent / "proyectos" / "dataset-medios"

sys.path.append(str(BASE_DIR))

try:
    from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO
except ImportError:
    NUMERICAS = ["distancia_km", "peso_kg", "volumen_l", "hora_salida", "trafico", "refrigerado", "fragil", "prioridad", "valor_declarado_mxn"]
    CATEGORICAS = ["clima", "zona_origen", "zona_destino", "dia_semana"]
    OBJETIVO = "medio_recomendado"

def main():
    csv_path = BASE_DIR / "envios_medios.csv"
    modelo_path = BASE_DIR / "modelo_medios.joblib"

    if not csv_path.exists():
        print(f"Error: No se encontró {csv_path}")
        return

    datos = pd.read_csv(csv_path)

    # 1. Importancia de características del modelo actual
    if modelo_path.exists():
        modelo = joblib.load(modelo_path)
        try:
            nombres = modelo.named_steps["preparacion"].get_feature_names_out()
            importancias = modelo.named_steps["arbol"].feature_importances_
            df_imp = pd.DataFrame({"caracteristica": nombres, "importancia": importancias})
            df_imp = df_imp.sort_values(by="importancia", ascending=False)
            print("=== IMPORTANCIA DE CARACTERÍSTICAS (ONE-HOT) ===")
            print(df_imp.head(15).to_string(index=False))
            print()
        except Exception as e:
            print(f"Nota: No se pudo extraer directamente get_feature_names_out: {e}")

    # 2. Experimento: Medir qué pasa al quitar cada columna original
    print("=== IMPACTO EN EXACTITUD AL QUITAR CADA COLUMNA ===")
    x = datos[NUMERICAS + CATEGORICAS]
    y = datos[OBJETIVO]

    x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=42
    )

    # Entrenar modelo base completo
    def entrenar_evaluar(cols_num, cols_cat):
        preparacion = ColumnTransformer(
            transformers=[
                ("num", "passthrough", cols_num),
                ("cat", OneHotEncoder(handle_unknown="ignore"), cols_cat),
            ]
        )
        pipe = Pipeline([
            ("preparacion", preparacion),
            ("arbol", DecisionTreeClassifier(max_depth=8, min_samples_leaf=5, random_state=42))
        ])
        pipe.fit(x_entreno[cols_num + cols_cat], y_entreno)
        preds = pipe.predict(x_prueba[cols_num + cols_cat])
        return accuracy_score(y_prueba, preds)

    acc_base = entrenar_evaluar(NUMERICAS, CATEGORICAS)
    print(f"Exactitud con todas las columnas ({len(NUMERICAS)+len(CATEGORICAS)}): {acc_base*100:.2f}%\n")

    resultados = []
    for col in NUMERICAS:
        nums_restantes = [c for c in NUMERICAS if c != col]
        acc = entrenar_evaluar(nums_restantes, CATEGORICAS)
        caida = (acc_base - acc) * 100
        resultados.append({"columna": col, "tipo": "numerica", "exactitud": acc*100, "diferencia_puntos": caida})

    for col in CATEGORICAS:
        cats_restantes = [c for c in CATEGORICAS if c != col]
        acc = entrenar_evaluar(NUMERICAS, cats_restantes)
        caida = (acc_base - acc) * 100
        resultados.append({"columna": col, "tipo": "categorica", "exactitud": acc*100, "diferencia_puntos": caida})

    df_res = pd.DataFrame(resultados).sort_values(by="diferencia_puntos", ascending=False)
    print(df_res.to_string(index=False))

if __name__ == "__main__":
    main()
