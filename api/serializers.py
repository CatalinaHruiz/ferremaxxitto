# En serializers.py de tu aplicación
from rest_framework import serializers
from django.contrib.auth.models import User
from Pag.models import usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = ['rut_usu', 'nombre_usu', 'correo_usu', 'contrasena_usu', 'direccion_usu', 'telefono_usu', 'rol_usu', 'id_preg']
