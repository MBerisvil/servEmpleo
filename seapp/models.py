from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from typing import Any
from datetime import datetime

# Create your models here.
class Persona(models.Model):
    dni = models.CharField(max_length=20, null=False, blank=False)
    cuit = models.CharField(max_length=20, null=False, blank=False)
    nombre: str = models.CharField(max_length=100)
    apellido = models.CharField(max_length= 100,null=False, blank=False)
    email: str = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=False, blank=False)
    direccion = models.CharField(max_length=202, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=True, blank=False)
    SEXO =  [(1, "Masculino"),
            (2, "Femenino"),
            (3, "Otro"),]
    sexo = models.PositiveSmallIntegerField(choices = SEXO,null=True, blank=False)
    localidad = models.CharField(max_length=120, null=False, blank=False)
    provincia = models.CharField(max_length=120, null=False, blank=False)
    pais = models.CharField(max_length=120, verbose_name="país", null=False, blank=False)
    email = models.EmailField(unique=True)  # Asegúrate de que este campo exista y sea único
    image = models.ImageField(upload_to="imgPerfil", null=True, blank=True, verbose_name="perfil")
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='persona')
    es_persona_fisica = models.BooleanField(default=True)  # Asegúrate de que este campo existaexit
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    search_filter = ('nombre','apellido','dni','cuit','estudios_realizados')


    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.email})"

    def get_full_info(self) -> dict[str, Any]:
        return {
            'nombre': self.nombre,
            'email': self.email,
            'es_empresa': self.usuario.is_enterprise
        }

class IdiomaPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='idiomas')
    idioma = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)  # Ejemplo: "Básico", "Intermedio", "Avanzado"

    def __str__(self):
        return f"{self.idioma} - {self.nivel} ({self.persona.nombre} {self.persona.apellido})"

    class Meta:
        verbose_name = "idioma"
        verbose_name_plural = "idiomas"
        ordering = ["-id"]

    def __str__(self):
        return self.idioma


class EstudioRealizado(models.Model):
    carrera = models.CharField(max_length=150)
    nivel_academico = [ (1, "Primario"),
                        (2, "Secundario"),
                        (3, "Terciario"),
                        (4, "Universitario"), ]
    niv_academico = models.PositiveSmallIntegerField (choices= nivel_academico, verbose_name="Nivel Academico")
    estado_estudios = [ (1, "Completo"),
                        (2, "Incompleto"),
                        (3, "En curso"), ]
    esta_estudios = models.PositiveSmallIntegerField (choices= estado_estudios, verbose_name="Estado de Estudios")
    estudiospersona = models.ForeignKey (Persona, null=True, blank=True,  on_delete=models.CASCADE, related_name='estudios_realizados')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "estudio realizado"
        verbose_name_plural = "estudios realizados"
        ordering = ["-id"]

    def __str__(self):
        return self.carrera

class ExperienciaLaboral(models.Model):
    puesto = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    sec_empresa = models.PositiveSmallIntegerField(choices=[
        (1, "Recursos Humanos"),
        (2, "Producción"),
        (3, "Finanzas / Contabilidad"),
        (4, "Marketing y Ventas"),
        (5, "Tecnología"),
        (6, "Servicio al Cliente"),
        (7, "Sistemas"),
        (8, "Calidad"),
        (9, "Logística"),
        (10, "Ingeniería"),
        (11, "Dirección Ejecutiva"),
        (12, "Otros"),
    ], verbose_name="Sector")
    experienciapersona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)

class InformacionAdicional(models.Model):
    curso = models.CharField(max_length=150, verbose_name="Capacitación Tomada")
    instituto_cursado = models.CharField( max_length=120,)
    informacionpersona = models.ForeignKey (Persona, null=True, blank=True,  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "información adicional"
        verbose_name_plural = "informaciones adicionales"
        ordering = ["-id"]

    def __str__(self):
        return self.curso

class Contacto(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre Completo")
    email = models.EmailField()
    asunto = models.CharField(max_length=60, verbose_name="Asunto de su consulta")
    mensaje = models.TextField("Mensaje", blank=False , null= False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
    


"""
COMANDOS DE CONSOSA GITBASH
 *python manage.py makemigrations - Prepara migrrcion de models
 * python manage.py migrate - Ejecuta migrarion de models
 *python manage.py runserver - Levanta servidor de desarrollo
"""