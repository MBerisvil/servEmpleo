from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


admin.site.site_header = "Servicio de Empleo"
admin.site.site_title = "Servicio de Empleo"
admin.site.index_title = "Servicio de Empleo"

urlpatterns = [
    path('', views.index, name='index.html'),
    path('nosotros/', views.nosotros, name='nosotros.html'),
    path('base/', views.base, name='base.html'),
    path('persona/', views.persona, name='persona.html'),
    path('estudiorealizado/', views.estudiorealizado, name='estudiorealizado.html'),
    path('eliminar_estudiorealizado/<int:pk>/', views.eliminar_estudiorealizado, name='eliminar_estudiorealizado.html'),
    path('contacto/', views.contacto, name='contacto.html'),
    path('listadocandidatos/', views.listado_candidatos, name='listadocandidatos.html'),
    path('modificarpersona/<int:pk>/', views.modificar_persona, name='modificarpersona.html'),
    path('registrarse/', views.registrarse, name='registrarse.html'),
    #path('registrarseOpc/', views.registrarseOpc, name='registrarseOpc.html'),
    #path('registrarseCan/', views.registrarseCan, name='registrarseCan.html'),
    #path('registrarseEmp/', views.registrarseEmp, name='registrarseEmp.html'),
    path('informacionadicional/', views.informacionadicional, name='informacionadicional.html'),
    path('eliminar_informacion/<int:pk>/', views.eliminar_informacion, name='eliminar_informacion.html'),
    path('experiencialaboral/', views.experiencialaboral, name='experiencialaboral.html'),
    path('eliminar_experiencia/<int:id>/', views.eliminar_experiencia, name='eliminar_experiencia.html'),  # Asegúrate de que este nombre coincida
    path('dashboard/', views.dashboard, name='dashboard.html'),
    path('desactivar_usuario/<int:pk>/', views.desactivar_usuario, name='desactivar_usuario.html'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario.html'),
    path('ver_candidato/<int:persona_id>/', views.ver_candidato, name='ver_candidato.html'),
    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send_test_email/', views.send_test_email, name='send_test_email'),
]