import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score

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

try:
    from usar_modelo import es_posible
except ImportError:
    es_posible = None

def construir_pipeline(class_weight=None):
    preparacion = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ]
    )
    return Pipeline([
        ("preparacion", preparacion),
        ("arbol", DecisionTreeClassifier(max_depth=8, min_samples_leaf=5, random_state=42, class_weight=class_weight))
    ])

def main():
    csv_path = BASE_DIR / "envios_medios.csv"
    if not csv_path.exists():
        print(f"Error: No se encontró {csv_path}")
        return

    datos = pd.read_csv(csv_path)
    x = datos[NUMERICAS + CATEGORICAS]
    y = datos[OBJETIVO]

    # Separación limpia: 80% entreno, 20% prueba
    x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=42
    )

    total_drones_reales = (y_prueba == "dron").sum()
    print(f"Envíos en prueba: {len(y_prueba)} (Drones reales en prueba: {total_drones_reales})\n")

    filas_tabla = []

    def evaluar_estrategia(nombre, x_tr, y_tr, class_weight=None, x_te=x_prueba, y_te=y_prueba):
        pipe = construir_pipeline(class_weight=class_weight)
        pipe.fit(x_tr, y_tr)
        preds = pipe.predict(x_te)

        acc = accuracy_score(y_te, preds)
        prec_dron = precision_score(y_te, preds, labels=["dron"], average=None, zero_division=0)[0]
        rec_dron = recall_score(y_te, preds, labels=["dron"], average=None, zero_division=0)[0]
        veces_dron = (preds == "dron").sum()

        imposibles = 0
        if es_posible:
            df_preds = x_te.copy()
            df_preds["medio_predicho"] = preds
            imp_mask = df_preds.apply(lambda r: not es_posible(r["medio_predicho"], r), axis=1)
            imposibles = imp_mask.sum()

        filas_tabla.append({
            "Estrategia": nombre,
            "Envíos entreno": len(x_tr),
            "Exactitud": f"{acc*100:.1f}%",
            "Precision dron": f"{prec_dron:.3f}",
            "Recall dron": f"{rec_dron:.3f}",
            "Veces predice dron": veces_dron,
            "Sugerencias imposibles": imposibles
        })

    # 1. Sin balancear
    evaluar_estrategia("Sin balancear", x_entreno, y_entreno)

    # 2. class_weight="balanced"
    evaluar_estrategia("Ponderar clases (class_weight)", x_entreno, y_entreno, class_weight="balanced")

    # 3. Oversampling: Repetir drones en el conjunto de entrenamiento
    df_tr = x_entreno.copy()
    df_tr["target"] = y_entreno
    df_drones = df_tr[df_tr["target"] == "dron"]
    # Duplicar drones hasta igualar promedio de otras clases
    n_repetir = int((len(df_tr) / 4) - len(df_drones))
    if n_repetir > 0:
        drones_extra = df_drones.sample(n=n_repetir, replace=True, random_state=42)
        df_over = pd.concat([df_tr, drones_extra])
        evaluar_estrategia("Repetir drones (Oversampling)", df_over[NUMERICAS + CATEGORICAS], df_over["target"])

    # 4. Undersampling: Reducir las clases mayoritarias
    n_drones = len(df_drones)
    partes = []
    for clase, grupo in df_tr.groupby("target"):
        partes.append(grupo.sample(n=min(len(grupo), n_drones * 2), random_state=42))
    df_under = pd.concat(partes)
    evaluar_estrategia("Reducir mayoritarias (Undersampling)", df_under[NUMERICAS + CATEGORICAS], df_under["target"])

    # 5. Trampa a propósito: Balancear ANTES de separar datos (data leakage)
    df_total = x.copy()
    df_total["target"] = y
    df_dron_tot = df_total[df_total["target"] == "dron"]
    drones_tot_extra = df_dron_tot.sample(n=len(df_total)//2, replace=True, random_state=42)
    df_trampa = pd.concat([df_total, drones_tot_extra])
    x_tr_t, x_te_t, y_tr_t, y_te_t = train_test_split(
        df_trampa[NUMERICAS + CATEGORICAS], df_trampa["target"], test_size=0.2, stratify=df_trampa["target"], random_state=42
    )
    evaluar_estrategia("Trampa (Repetir antes de separar)", x_tr_t, y_tr_t, x_te=x_te_t, y_te=y_te_t)

    print("=== RESULTADOS COMPARATIVOS ===")
    tabla_final = pd.DataFrame(filas_tabla)
    print(tabla_final.to_string(index=False))

if __name__ == "__main__":
    main()
