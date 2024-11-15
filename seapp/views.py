"""----------------DEPENDENCIAS----------------"""

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import View,TemplateView, FormView,CreateView
from .forms import Persona_Form,Empresa_Form, EstudioRealizado_Form, Contacto_Form, CrearUsuarioForm, InformacionAdicional_Form, \
    ExperienciaLaboral_Form, UserRegistrationForm, GroupUserForm
from .models import Persona, EstudioRealizado, InformacionAdicional, ExperienciaLaboral
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Persona
from .forms import Persona_Form


#VIEWS GENERALS
# Create your views here.
def base(request):
    return render(request, "seapp/base.html")

def index(request):
    return render(request, "seapp/index.html")

def nosotros(request):
    return render(request, "seapp/nosotros.html")

def contacto(request):

    
    if request.method == 'POST':
        form = Contacto_Form(data=request.POST)
        if form.is_valid():
            send_mail(
                'Serv.Empleo:' + form.cleaned_data['asunto'],
                form.cleaned_data['mensaje'], 
                form.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
        )
        form.save()
        messages.success(request, "Mensaje enviado.")

    return render(request, "seapp/contacto.html")

   
    """
    data = {
        'form' : Contacto_Form()
    }

    if request.method == 'POST':
        formulario = Contacto_Form(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Consulta enviada.")
            data["message"] = "Consulta Enviada"
        else:
            data["form"] = formulario
    return render(request, "seapp/contacto.html", data)
    

    -----ASI ENVIA EMAIL----
    def contacto(request):
    
    data = {
        'form' : Contacto_Form()
    }

    if request.method == 'POST':
        formulario = Contacto_Form(data=request.POST)
        if formulario.is_valid():
            send_mail(
                formulario.cleaned_data['asunto'],
                formulario.cleaned_data['mensaje'], 
                formulario.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
        )
            messages.success(request, "Mensaje enviada.")

    return render(request, "seapp/contacto.html",data)
    

    """

def registrarse(request):

    data = {
        'form' : CrearUsuarioForm()
    }
    if request.method == 'POST':
        formulario = CrearUsuarioForm(data=request.POST)
        if formulario.is_valid():

            #Send Email Welcome
            send_mail(
                'Bienvenido a Serv.Empleo',
                'Gracias por registrarte en nuestra plataforma. Esperamos que encuentres un buen puesto de trabajo o candidato.',
                formulario.cleaned_data["username"],
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            if user.is_enterprise:
                group = Group.objects.get(name='Empresas')
                user.groups.add(group)  
                messages.success(request, "Te has registrado correctamente")
                return redirect(to="index.html")
            else:
                group = Group.objects.get(name='Candidatos')
                user.groups.add(group)
                messages.success(request, "Te has registrado correctamente")
            #redirigir al Home
            return redirect(to="index.html")
        data ["form"] = formulario

    return render(request, "registration/registrarse.html", data)
    

"""----------------VIEWS DE CANDIDATES----------------"""
@login_required
def persona(request):
    user = request.user  # Obtener el usuario logueado
    persona, created = Persona.objects.get_or_create(usuario=user)  # Asegúrate de que se obtenga o cree correctamente

    if request.method == 'POST':
        form = Persona_Form(request.POST, request.FILES, instance=persona)  # Asegúrate de que el formulario esté vinculado a la instancia correcta
        if form.is_valid():
            form.save()  # Guarda los datos del formulario
            messages.success(request, "Datos actualizados correctamente.")
            return redirect('persona.html')  # Redirige después de guardar
    else:
        form = Persona_Form(instance=persona)  # Carga el formulario con la instancia existente

    context = {
        'form': form,
        'persona': persona,
        'Persona': user.persona  # Pasar el objeto usuario
    }

    return render(request, "seapp/persona.html", context)

@login_required
def modificar_persona(request, pk):

    persona = get_object_or_404(Persona, id=pk)

    data = {
        'persona' : Persona_Form(instance=persona),
        'empresa' : Empresa_Form(instance=persona)
    }

    if request.method == 'POST':
        formulario = Persona_Form(data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="persona.html")
        data['persona'] = formulario

    if request.method == 'POST':
        formulario = Empresa_Form(data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="persona.html")
        data['empresa'] = formulario
  

    return render(request, "seapp/modificarpersona.html", data)

# -- REVISAR FORMULARIO --***
@login_required
def estudiorealizado(request):
    user = request.user
    estudiorealizado = EstudioRealizado.objects.filter(estudiospersona__usuario=user)

    if request.method == 'POST':
        formulario = EstudioRealizado_Form(data=request.POST)
        if formulario.is_valid():
            nuevo_estudio = formulario.save(commit=False)
            nuevo_estudio.estudiospersona = user.persona  # Asignar la persona del usuario logueado
            nuevo_estudio.save()
            messages.success(request, "Datos Cargados.")
            return redirect('estudiorealizado.html')  # Redirigir a la misma vista para actualizar la lista
        else:
            messages.error(request, "Error al guardar los datos.")
    else:
        formulario = EstudioRealizado_Form()

    data = {
        'Persona': user.persona,
        'EstudioRealizado': estudiorealizado,
        'form': formulario,
        'message': messages.get_messages(request),
    }

    return render(request, "seapp/estudiorealizado.html", data)

@login_required
def eliminar_estudiorealizado(request, pk):
    estudiorealizado = get_object_or_404(EstudioRealizado, id=pk)
    estudiorealizado.delete()
    messages.success(request, "Estudio eliminado Correctamente.")
    return redirect(to="estudiorealizado.html")

@login_required
def informacionadicional(request):
    user = request.user
    # Filtrar las capacitaciones del usuario logueado
    informacionadicional = InformacionAdicional.objects.filter(informacionpersona__usuario=user)

    if request.method == 'POST':
        formulario = InformacionAdicional_Form(data=request.POST)
        if formulario.is_valid():
            nueva_capacitacion = formulario.save(commit=False)
            nueva_capacitacion.informacionpersona = user.persona  # Asignar la persona del usuario logueado
            nueva_capacitacion.save()
            messages.success(request, "Capacitación registrada correctamente!")
            return redirect('informacionadicional.html')  # Redirigir a la misma vista para actualizar la lista
        else:
            messages.error(request, "Error al guardar los datos.")
    else:
        formulario = InformacionAdicional_Form()

    data = {
        'Persona': user.persona,
        'InformacionAdicional': informacionadicional,
        'form': formulario,
        'message': messages.get_messages(request),
    }

    return render(request, "seapp/informacionadicional.html", data)

@login_required
def eliminar_informacion(request, pk):
    informacionadicional = get_object_or_404(InformacionAdicional, id=pk)
    informacionadicional.delete()
    messages.success(request, "Capacitacion eliminada correctamente.")
    return redirect(to="informacionadicional.html")

@login_required
def experiencialaboral(request):
    user = request.user
    # Filtrar las experiencias laborales del usuario logueado
    experiencialaboral = ExperienciaLaboral.objects.filter(experienciapersona__usuario=user)

    if request.method == 'POST':
        formulario = ExperienciaLaboral_Form(data=request.POST)
        if formulario.is_valid():
            nueva_experiencia = formulario.save(commit=False)
            nueva_experiencia.experienciapersona = user.persona  # Asignar la persona del usuario logueado
            nueva_experiencia.save()
            messages.success(request, "Experiencia Laboral Registrada!")
            return redirect('experiencialaboral.html')  # Redirigir a la misma vista para actualizar la lista
        else:
            messages.error(request, "Error al guardar los datos.")
    else:
        formulario = ExperienciaLaboral_Form()

    data = {
        'Persona': user.persona,
        'ExperienciaLaboral': experiencialaboral,
        'form': formulario,
        'message': messages.get_messages(request),
        'now': timezone.now(),  # Pasar la fecha actual al contexto
    }

    return render(request, "seapp/experiencialaboral.html", data)

@login_required
def eliminar_experiencia(request, id):  # Cambia 'pk' a 'id' si estás usando 'id' en la URL
    experiencia = get_object_or_404(ExperienciaLaboral, id=id)
    experiencia.delete()
    messages.success(request, "Experiencia laboral eliminada correctamente.")
    return redirect('experiencialaboral.html')


"""----------------VIEWS DE COMPANIES----------------"""


@login_required
def listado_candidatos(request):
    query = request.GET.get('q','')  # Obtener la consulta de búsqueda
    personas = Persona.objects.all()  # Obtener todas las personas 

    if query:
        personas = Persona.objects.filter(
            # Filtrar por nombre, apellido, email o teléfono    
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(usuario__email__icontains=query) | 
            Q(telefono__icontains=query) |
            Q(estudios_realizados__carrera__icontains=query)
        )
   

    paginator = Paginator(personas, 10)  # Mostrar 10 candidatos por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener la página correspondiente

    # Crear una lista para almacenar la información de los candidatos
    candidatos_info = []
    for persona in page_obj:
        estudios = persona.estudios_realizados.all()  # Obtener los estudios relacionados
        candidatos_info.append({
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'email': persona.usuario.email,  # Asegúrate de que el usuario esté relacionado
            'telefono': persona.telefono,
            'estudios': estudios,  # Agregar los estudios a la información del candidato
        })

    return render(request, "seapp/listadocandidatos.html", {'candidatos': candidatos_info, 'page_obj': page_obj,  'query': query})

@login_required
def listado_experiencia(request):
    experiencialaboral = ExperienciaLaboral.objects.all()

    data = {
        'ExperienciaLaboral' : experiencialaboral,
    }

    return render(request, "seapp/experiencialaboral.html", data)


@login_required
def ver_candidato(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    estudios = persona.estudios_realizados.all()
    return render(request, "seapp/ver_candidato.html", {
        'persona': persona,
        'estudios': estudios,
    })



"""----------------VIEWS OF MANAGER----------------"""
@login_required
def dashboard(request):
    busqueda = request.POST.get("buscar")
    usuarios = User.objects.all()

    if busqueda:
        usuarios = User.objects.filter(
            Q(username__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) | 
            Q(email__icontains=busqueda)
        ).distinct()
    else:
        messages.error(request, "No se encontraron resultados para la búsqueda")

    # Configuración de la paginación
    paginator = Paginator(usuarios, 10)  # Mostrar 10 usuarios por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener la página correspondiente


    data = {
        'User': page_obj,  # Pasar la página de usuarios a la plantilla
    }

    return render(request, 'seapp/dashboard.html', data)

@login_required
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administrador').exists())
def eliminar_usuario(request, pk):

    usuario = get_object_or_404(User, id=pk)
    if usuario:
        usuario.delete()
        
        messages.success(request, "Usuario eliminado correctamente")


    return redirect(to="dashboard.html")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administrador').exists())
def desactivar_usuario(request, pk):

    usuario = get_object_or_404(User, id=pk)
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, "Usuario desactivado correctamente")
    else:
        usuario.is_active = True
        usuario.save()
        messages.success(request, "Usuario activado correctamente")


    return redirect(to="dashboard.html")


def send_test_email(request):
    send_mail(
        'Asunto de prueba',
        'Este es un correo de prueba enviado desde Django usando SendGrid.',
        'administrador@servicioempleo.com',  # Remitente
        ['email'],  # Cambia esto por un correo de destino
        fail_silently=False,
    )
    return HttpResponse("Correo enviado.")


"""----------------DISCARDED CODE----------------"""
"""def email_bienvenida_email(user):

    email = EmailMessage(
        subject='Bienvenido a Sistema de Empleo',
        body='Hola'+ user.username + 
        if user.is_enterprise():
                ', bienvenido al sistema de empresas, aquí las empresas podrán publicar sus vacantes y buscar candidatos.'
        else:
        ', bienvenido al sistema de empleo, aquí podrás aplicar a empleo y buscar empleos.'
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    email.send()"""
"""def registrarseOpc(request):

    return render(request, "registration/registrarseOpc.html")

def registrarseCan(request):

    data = {
        'form' : CrearUsuarioForm()
    }
    if request.method == 'POST':
        formulario = CrearUsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            group = Group.objects.get(name='Candidatos')
            user.groups.add(group)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al Home
            return redirect(to="index.html")
        data ["form"] = formulario

    return render(request, "registration/registrarseCan.html",data)

def registrarseEmp(request):

    data = {
        'form' : CrearUsuarioForm()
    }
    if request.method == 'POST':
        formulario = CrearUsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            group = Group.objects.get(name='Empresas')
            user.groups.add(group)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al Home
            return redirect(to="index.html")
        data ["form"] = formulario

    return render(request, "registration/registrarseEmp.html", data)"""
