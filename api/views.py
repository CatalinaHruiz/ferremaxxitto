import json
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from Pag.models import usuario
from .serializers import UsuarioSerializer
from rest_framework.response import Response

#API VERIFICACION DE CORREO
# Obténgo el modelo de usuario desde la app `Pag`
User = apps.get_model('Pag', 'usuario')

@csrf_exempt
def chequeo_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos de la solicitud:", data)  # Imprime los datos de la solicitud en la consola de Django
            email = data.get('correo_usu')  # Accede al campo 'correo_usu' en los datos de la solicitud
            print("Correo recibido:", email)  # Esto imprimirá el correo electrónico en la consola de Django
            if email:
                user_exists = usuario.objects.filter(correo_usu=email).exists()  # Filtra por el campo 'correo_usu'
                return JsonResponse({'exists': user_exists})
            else:
                return JsonResponse({'error': 'El campo de correo es requerido'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


#API DE CREACION DE USUARIOS
@api_view(['POST'])
def creausuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)