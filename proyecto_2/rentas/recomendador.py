"""Orquesta la inferencia del modelo (.joblib), cálculo de ranking y aplicación de reglas.

Adaptado del código base de clase: apuntes/plataforma-entregas/entregas/recomendador.py
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

try:
    from .reglas import es_posible, aplicar_reglas, HERRAMIENTAS_POR_OFICIO
except ImportError:
    from reglas import es_posible, aplicar_reglas, HERRAMIENTAS_POR_OFICIO

RUTA_MODELO = Path(__file__).resolve().parent / "modelo_herramientas.joblib"

CAMPOS_NUMERICOS = ["duracion_dias"]
CAMPOS_TEXTO = ["tipo_trabajo", "escala_trabajo", "experiencia_usuario", "area_trabajo"]
CAMPOS = CAMPOS_NUMERICOS + CAMPOS_TEXTO


@dataclass(frozen=True)
class Sugerencia:
    opcion: str
    motivo: str


@dataclass
class ResultadoRecomendacion:
    eleccion: str
    es_kit: bool
    motivo: str
    preferido_por_modelo: str
    corregido_por_reglas: bool
    confianza: float
    ranking: list
    descartados: list
    proceso: list = field(default_factory=list)

    def a_dict(self):
        return asdict(self)


class RecomendadorIA(ABC):
    @abstractmethod
    def sugerir(self, solicitud: dict) -> Sugerencia:
        pass

    @abstractmethod
    def explicar(self, solicitud: dict) -> ResultadoRecomendacion:
        pass


class RecomendadorHerramientas(RecomendadorIA):
    """Pipeline de scikit-learn con predict_proba -> Sugerencia + reglas de negocio."""

    def __init__(self, ruta: Path = RUTA_MODELO):
        if not ruta.exists():
            raise FileNotFoundError(
                f"No encuentro {ruta}. Primero ejecute python entrenar_arbol.py"
            )
        self._modelo = joblib.load(ruta)

    def sugerir(self, solicitud: dict) -> Sugerencia:
        resultado = self.explicar(solicitud)
        return Sugerencia(resultado.eleccion, resultado.motivo)

    def explicar(self, solicitud: dict) -> ResultadoRecomendacion:
        tipo_trabajo = solicitud.get("tipo_trabajo", "").lower()
        proceso = [
            {
                "paso": 1,
                "titulo": "Solicitud de trabajo recibida",
                "detalle": f"Trabajo: {tipo_trabajo}, escala: {solicitud.get('escala_trabajo')}, experiencia: {solicitud.get('experiencia_usuario')}.",
            },
            {
                "paso": 2,
                "titulo": "El modelo calcula probabilidades",
                "detalle": "predict_proba responde un porcentaje para cada herramienta y kit del catálogo.",
            },
        ]

        datos = pd.DataFrame([solicitud], columns=CAMPOS)
        probabilidades = self._modelo.predict_proba(datos)[0]
        ranking_crudo = sorted(
            [
                {"opcion": str(opcion), "confianza": round(float(p), 3)}
                for opcion, p in zip(self._modelo.classes_, probabilidades)
            ],
            key=lambda item: -item["confianza"],
        )

        # Solo tomamos en cuenta las herramientas del oficio que pidio
        validas_oficio = list(HERRAMIENTAS_POR_OFICIO.get(tipo_trabajo, {}).values())
        ranking_oficio = [item for item in ranking_crudo if item["opcion"] in validas_oficio]

        # Si alguna opcion no salio en el ranking, la agregamos con 0
        opciones_en_ranking = {item["opcion"] for item in ranking_oficio}
        for opc in validas_oficio:
            if opc not in opciones_en_ranking:
                ranking_oficio.append({"opcion": opc, "confianza": 0.0})

        # Ajustamos las probabilidades para que sumen 1.0 en este oficio
        suma_prob = sum(item["confianza"] for item in ranking_oficio)
        if suma_prob > 0:
            ranking_final = [
                {
                    "opcion": item["opcion"],
                    "confianza": round(item["confianza"] / suma_prob, 2),
                }
                for item in ranking_oficio
            ]
        else:
            ranking_final = ranking_oficio

        ranking_final = sorted(ranking_final, key=lambda x: -x["confianza"])

        preferido = ranking_final[0]["opcion"] if ranking_final else ranking_crudo[0]["opcion"]
        confianza_original = ranking_final[0]["confianza"] if ranking_final else ranking_crudo[0]["confianza"]

        proceso.append(
            {
                "paso": 3,
                "titulo": "Ranking del modelo",
                "detalle": f"El modelo sugiere '{preferido}' con {confianza_original:.0%} de confianza.",
                "ranking": ranking_final,
            }
        )

        # Pasamos la mejor opcion por las reglas de negocio
        elegido, corregido, motivo, confianza_final = aplicar_reglas(
            preferido, solicitud, confianza_original
        )
        es_kit_final = "kit" in elegido.lower()

        descartados = []
        if corregido:
            descartados.append(
                {
                    "opcion": preferido,
                    "confianza": confianza_original,
                    "razon": motivo,
                }
            )

        proceso.append(
            {
                "paso": 4,
                "titulo": "Validación con reglas de negocio",
                "detalle": motivo,
                "descartados": descartados,
            }
        )

        proceso.append(
            {
                "paso": 5,
                "titulo": "Decisión final",
                "detalle": motivo,
                "eleccion": elegido,
                "es_kit": es_kit_final,
                "corregido_por_reglas": corregido,
            }
        )

        return ResultadoRecomendacion(
            eleccion=elegido,
            es_kit=es_kit_final,
            motivo=motivo,
            preferido_por_modelo=preferido,
            corregido_por_reglas=corregido,
            confianza=confianza_final,
            ranking=ranking_final,
            descartados=descartados,
            proceso=proceso,
        )


@lru_cache(maxsize=1)
def obtener_recomendador() -> RecomendadorIA:
    return RecomendadorHerramientas()
