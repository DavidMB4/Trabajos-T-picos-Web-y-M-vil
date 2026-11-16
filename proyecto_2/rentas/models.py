from django.db import models

class Herramienta(models.Model):
    TIPO_CHOICES = [
        ('individual', 'Herramienta Individual'),
        ('kit', 'Kit Completo'),
    ]

    CATEGORIA_CHOICES = [
        ('demolicion', 'Demolición y Construcción'),
        ('carpinteria', 'Carpintería'),
        ('plomeria', 'Plomería'),
        ('electricidad', 'Electricidad'),
        ('jardineria', 'Jardinería y Poda'),
        ('pintura', 'Pintura y Acabados'),
    ]

    nombre = models.CharField(max_length=150, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='individual')
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    precio_dia = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=5)
    descripcion = models.TextField(blank=True)
    incluye_epp = models.BooleanField(default=False, help_text="Incluye Equipo de Protección Personal")

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) - ${self.precio_dia}/día"


class Renta(models.Model):
    ESTADO_CHOICES = [
        ('Registrado', 'Registrado'),
        ('En curso', 'En curso / Entregado'),
        ('Devuelto', 'Devuelto y Finalizado'),
    ]

    cliente_nombre = models.CharField(max_length=150)
    herramienta_sugerida = models.CharField(max_length=150)
    es_kit = models.BooleanField(default=False)
    tipo_trabajo = models.CharField(max_length=50)
    duracion_dias = models.IntegerField(default=1)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Registrado')

    confianza_modelo = models.FloatField(default=1.0)
    corregido_por_reglas = models.BooleanField(default=False)
    motivo_regla = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def codigo_folio(self):
        prefijo = (self.tipo_trabajo[:3] if self.tipo_trabajo else "HER").upper()
        periodo = self.fecha_creacion.strftime("%Y%m") if self.fecha_creacion else "202611"
        return f"{prefijo}-{periodo}-{self.id:04d}"

    def __str__(self):
        return f"{self.codigo_folio}: {self.cliente_nombre} - {self.herramienta_sugerida}"
