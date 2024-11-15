import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from seapp.models import Persona, EstudioRealizado  # Asegúrate de que la ruta sea correcta


fake = Faker()

"""def create_fake_personas(num_personas):
    for _ in range(num_personas):
        try:
            # Crear un usuario
            username = fake.email()  # Cambia a un nombre de usuario único
            email = fake.email()
            password = fake.password()
            
            # Asegúrate de que el nombre de usuario y el email sean únicos
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            while User.objects.filter(email=email).exists():
                email = fake.email()

            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_staff=False,
                is_superuser=False
            )

            # Crear una persona asociada al usuario
            Persona.objects.create(
                usuario=user,
                dni=fake.ssn(),
                cuit=fake.ssn(),
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                telefono=fake.phone_number(),
                direccion=fake.address(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=65),
                sexo=random.choice([1, 2, 3]),  # Asumiendo que 1=Masculino, 2=Femenino, 3=Otro
                localidad=fake.city(),
                provincia=fake.state(),
                pais=fake.country(),
                email=email,  # Asegúrate de que este campo exista en tu modelo
                image=None,  # Puedes agregar una imagen si lo deseas
                es_persona_fisica=True,  # Asegúrate de que este campo exista en tu modelo
            )
        except Exception as e:
            print(f"Error al crear persona: {e}")

if __name__ == "__main__":
    create_fake_personas(100)
    print("Creacion de 100 registros de personas completado.")"""



"""def create_fake_estudios_realizados(num_estudios):


    personas = Persona.objects.all()  # Obtener todas las personas
    for _ in range(num_estudios):
        if not personas:
            print("No hay personas disponibles para asociar estudios realizados.")
            return

        persona = random.choice(personas)  # Seleccionar una persona aleatoria
        carrera = fake.job()  # Puedes cambiar esto a un nombre de carrera real
        niv_academico = random.randint(0, 3)  # Asumiendo que los niveles académicos son 0, 1, 2, 3
        esta_estudios = random.randint(0, 1)  # Asumiendo que 0 = No, 1 = Sí

        # Crear el estudio realizado
        EstudioRealizado.objects.create(
            carrera=carrera,
            niv_academico=niv_academico,
            esta_estudios=esta_estudios,
            estudiospersona=persona
        )

if __name__ == "__main__":
    create_fake_estudios_realizados(130)  # Cambia el número según lo que necesites
    print("200 registros de estudios realizados han sido creados.")"""



import os
import django
import random
from faker import Faker
from seapp.models import Persona, ExperienciaLaboral  # Asegúrate de que la ruta sea correcta

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # Cambia 'tu_proyecto' por el nombre de tu proyecto
django.setup()

fake = Faker()

def create_fake_experiencias_laborales(num_experiencias):
    personas = Persona.objects.all()  # Obtener todas las personas
    for _ in range(num_experiencias):
        if not personas:
            print("No hay personas disponibles para asociar experiencias laborales.")
            return

        persona = random.choice(personas)  # Seleccionar una persona aleatoria
        empresa = fake.company()  # Generar un nombre de empresa
        sec_empresa = random.randint(0, 10)  # Generar un sector de empresa (0 a 10)

        # Crear la experiencia laboral
        ExperienciaLaboral.objects.create(
            empresa=empresa,
            sec_empresa=sec_empresa,
            experienciapersona=persona
        )

if __name__ == "__main__":
    create_fake_experiencias_laborales(130)  # Cambia el número según lo que necesites
    print("200 registros de experiencias laborales han sido creados.")