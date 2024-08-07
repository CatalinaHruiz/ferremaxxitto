from django.contrib import admin
from . import views
from django.urls import path
from .views import (
    mostrarhome, mostrarcarrito, mostrarherramientas, mostrarinicio, mostrarvendedor,
    iniciarsesion, registrar, finsesion, mostraragregar, agregarproducto, eliminarproducto,
    modificarproducto, mostrarproducto, mostrarnuevotrabajador, mostrarmenulogin,
    webpay_plus_create, webpay_plus_commit, error, rechazo, password_recovery_view,
    password_recovery_success
)

urlpatterns = [
    path('', mostrarhome, name="MenuPrincipal"),
    path('Carrito/', mostrarcarrito, name="Carrito"),
    path('Herramientas/', mostrarherramientas, name="Herramientas"),
    path('Inicio/', mostrarinicio, name="Sesion"),
    path('Vendedor/', mostrarvendedor, name="Vendedor"),
    path('MenuPrincipalLogin/', mostrarmenulogin, name="MenuPrincipalLogin"),
    path('mostrarproducto/', mostraragregar, name="mostrarcategoria"),
    path('mostrarnuevotrabajador/', mostrarnuevotrabajador, name="mostrarnuevotrabajador"),
    path('iniciarsesion/', iniciarsesion, name='iniciarsesion'),   
    path('registrar/', registrar, name="registrar"),
    path('finsesion/', finsesion, name='finsesion'),
    path('agregarproducto/', agregarproducto, name='agregarproducto'),
    path('eliminarproducto/<id_prod>', eliminarproducto, name='eliminarproducto'),
    path('mostrarproducto/<int:id_prod>', mostrarproducto, name='mostrarproducto'),
    path('modificarproducto/<int:id_prod>', modificarproducto, name='modificarproducto'),
    path('create-webpay/', webpay_plus_create, name='create-webpay'),  # Asegúrate de que la URL termine con '/'
    path('commit-webpay/', webpay_plus_commit, name='commit-webpay'),  # Asegúrate de que la URL termine con '/'
    path('error-compra/', error, name='error-compra'),
    path('compra-rechazada/', rechazo, name='compra-rechazada'),
    path('recuperar_contrasena/', password_recovery_view, name='recover_password'),  # Asegúrate de que usa la vista correcta
    path('password_recovery_success/', password_recovery_success, name='password_recovery_success'),
]
