from django.urls import path
from .views import chequeo_email,creausuario

urlpatterns = [
    path('chequeoemail/', chequeo_email, name='chequeoemail'),
    path('creandousuario/', creausuario, name='creandousuario'),
]
