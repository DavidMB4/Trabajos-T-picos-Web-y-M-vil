import json
from decimal import Decimal
from django.test import TestCase, Client
from .models import Herramienta, Renta


class RentasBackendTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear datos de prueba en la base de datos de test
        self.herramienta = Herramienta.objects.create(
            nombre="Rotomartillo individual",
            tipo="individual",
            categoria="demolicion",
            precio_dia=Decimal("350.00"),
            stock=5,
            descripcion="Rotomartillo de prueba"
        )

    def test_0_estado_api(self):
        # que la raiz responda 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertEqual(datos["estado"], "activo")

    def test_1_catalogo_endpoint(self):
        # que el catalogo traiga herramientas
        response = self.client.get('/api/catalogo/')
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertIn("catalogo", datos)
        self.assertGreaterEqual(datos["total"], 1)

    def test_2_recomendar_endpoint_exitoso(self):
        # mandar datos completos al recomendador
        payload = {
            "tipo_trabajo": "demolicion",
            "escala_trabajo": "obra_mayor",
            "experiencia_usuario": "profesional",
            "duracion_dias": 5,
            "area_trabajo": "exterior"
        }
        response = self.client.post(
            '/api/recomendar/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertIn("eleccion", datos)
        self.assertIn("confianza", datos)
        self.assertIn("ranking", datos)

    def test_3_recomendar_error_400_campos_faltantes(self):
        # si faltan datos debe regresar 400
        payload = {"tipo_trabajo": "demolicion"}
        response = self.client.post(
            '/api/recomendar/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_4_registrar_renta_crea_folio(self):
        # registrar renta y checar que cree el registro
        payload = {
            "cliente_nombre": "Carlos Perez",
            "herramienta_sugerida": "Rotomartillo individual",
            "es_kit": False,
            "tipo_trabajo": "demolicion",
            "duracion_dias": 2,
            "confianza_modelo": 1.0,
            "corregido_por_reglas": False,
            "motivo_regla": "Recomendación directa"
        }
        response = self.client.post(
            '/api/rentas/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        datos = response.json()
        self.assertIn("folio", datos)
        self.assertEqual(datos["cliente"], "Carlos Perez")
        self.assertEqual(Renta.objects.count(), 1)

    def test_5_consultar_renta_por_folio(self):
        # buscar renta por id
        renta = Renta.objects.create(
            cliente_nombre="Ana Lopez",
            herramienta_sugerida="Rotomartillo individual",
            es_kit=False,
            tipo_trabajo="demolicion",
            duracion_dias=3,
            costo_total=Decimal("1050.00"),
            estado="Registrado"
        )
        response = self.client.get(f'/api/rentas/{renta.id}/')
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertEqual(datos["folio"], renta.id)
        self.assertEqual(datos["cliente"], "Ana Lopez")

    def test_6_cors_headers(self):
        # validar cabeceras cors
        response = self.client.get('/api/catalogo/')
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")

        response_options = self.client.options('/api/recomendar/')
        self.assertEqual(response_options.status_code, 200)
        self.assertEqual(response_options.headers.get("Access-Control-Allow-Origin"), "*")
        self.assertIn("POST", response_options.headers.get("Access-Control-Allow-Methods", ""))
