# entrenamiento del arbol de decision para renta de herramientas

import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, export_text

NUMERICAS = ["duracion_dias"]
CATEGORICAS = ["tipo_trabajo", "escala_trabajo", "experiencia_usuario", "area_trabajo"]
OBJETIVO = "herramienta_recomendada"

CARPETA_ACTUAL = Path(__file__).resolve().parent
RUTA_CSV_DEFAULT = CARPETA_ACTUAL / "herramientas_trabajos.csv"
RUTA_MODELO_DEFAULT = CARPETA_ACTUAL.parent / "rentas" / "modelo_herramientas.joblib"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datos", default=str(RUTA_CSV_DEFAULT))
    parser.add_argument("--profundidad", type=int, default=6)
    parser.add_argument("--salida", default=str(RUTA_MODELO_DEFAULT))
    args = parser.parse_args()

    datos = pd.read_csv(args.datos)
    x = datos[NUMERICAS + CATEGORICAS]
    y = datos[OBJETIVO]
    print(f"Total de registros para entrenar: {len(datos)}")

    # divide el dataset en 80% entrenamiento y 20% prueba
    x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # preparacion con one-hot encoding para textos
    preparacion = ColumnTransformer(
        [
            ("numericas", "passthrough", NUMERICAS),
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ]
    )

    # pipeline con preparacion y arbol de decision
    modelo = Pipeline(
        [
            ("preparacion", preparacion),
            (
                "arbol",
                DecisionTreeClassifier(
                    max_depth=args.profundidad, min_samples_leaf=1, random_state=42
                ),
            ),
        ]
    )

    # entrenar el pipeline
    modelo.fit(x_entreno, y_entreno)

    # evaluar exactitud
    prediccion = modelo.predict(x_prueba)
    exactitud = (prediccion == y_prueba).mean()
    print(f"Exactitud con datos de prueba: {exactitud:.1%}\n")

    # mostrar los primeros niveles del arbol
    nombres = list(modelo.named_steps["preparacion"].get_feature_names_out())
    nombres = [n.split("__", 1)[1] for n in nombres]
    print("Primeros niveles del árbol de decisión:")
    print(export_text(modelo.named_steps["arbol"], feature_names=nombres, max_depth=3))

    # guardar el modelo listo para Django
    joblib.dump(modelo, args.salida)
    print(f"[OK] Modelo guardado exitosamente en: {args.salida}")


if __name__ == "__main__":
    main()
