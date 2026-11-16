# entrenamiento del asistente de intenciones

import joblib
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

BASE = Path(__file__).parent
DATOS = BASE / "preguntas_comprador.csv"
SALIDA = BASE.parent / "rentas" / "modelo_asistente.joblib"


def main():
    datos = pd.read_csv(DATOS)
    x = datos["pregunta"]
    y = datos["intencion"]

    x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    modelo = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000, C=5.0)),
    ])

    modelo.fit(x_entreno, y_entreno)

    prediccion = modelo.predict(x_prueba)
    print(classification_report(y_prueba, prediccion, zero_division=0))

    joblib.dump(modelo, SALIDA)
    print(f"Modelo guardado en {SALIDA}")


if __name__ == "__main__":
    main()
