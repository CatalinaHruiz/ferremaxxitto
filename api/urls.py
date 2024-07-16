from django.urls import path
from .views import chequeo_email,creausuario
from . import views

urlpatterns = [
    path('chequeoemail/', chequeo_email, name='chequeoemail'),
    path('creandousuario/', creausuario, name='creandousuario'),
      path('api/nada', views.api_nada_post, name='api_nada_post'),
    path('api/nada', views.api_nada_delete, name='api_nada_delete'),
]
