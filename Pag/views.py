from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import pregunta,usuario,rol,categoria,producto
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import random
import requests
import datetime as dt
import json
from django.http import JsonResponse
from django.shortcuts import render
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys 
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction 


# Create your views here.
def mostrarhome(request):
    productos = producto.objects.all()
    return render(request,'MenuPrincipal.html',{'productos':productos})

def mostrarherramientas(request):
    productos = producto.objects.all()
    return render(request,'herramientas.html',{'productos':productos})

def mostrarinicio(request):
    preguntas = pregunta.objects.all()
    
    # Pasar los datos al template
    return render(request, 'InicioSeccion_Registro.html', {'preguntas': preguntas})

def mostrarolvido(request):
    return render(request,'olvidocontraseña.html')

def mostrarcarrito(request):
    return render(request,'carrito.html')

def mostrarvendedor(request):
    productos = producto.objects.all()
    return render(request,'inventarioAct.html',{'productos':productos})

def mostraragregar(request):
    categorias = categoria.objects.all()
    return render(request,'addproducto.html',{'categorias':categorias})

def mostrarnuevotrabajador(request):
    preguntas = pregunta.objects.all()
    roles = rol.objects.all()
    return render(request,'agregar_trabajador.html',{'preguntas':preguntas,'roles':roles})

def mostrarmenulogin(request):
    productos = producto.objects.all()
    return render(request,'MenuPrincipallogin.html',{'productos':productos})

def mostrarproducto(request,id_prod):
    productos = producto.objects.get(id_prod=id_prod)
    categorias = categoria.objects.all()
    return render(request,'modificarproducto.html',{'productos':productos,'categorias':categorias})
def error(request):
    return render(request, 'transbank/error.html')
def rechazo(request):
    return render(request, 'transbank/rechazada.html')


#FUNCIONES DEL USUARIO

def registrar(request):
    rutU = request.POST['rut']
    nombreU = request.POST['name']
    direccionU = request.POST['direccion']
    correoU = request.POST['correo']
    contrasenaU = request.POST['password']
    telefonoU = request.POST['telefono']
    preguntaU = request.POST['pregunta']
    respuestaU = request.POST['rs']

    # Verificar si el correo electrónico ya está registrado
    
    if User.objects.filter(email=correoU).exists():
        return render(request, 'correo_registrado.html')  # Renderiza la plantilla con el modal
    

    user = User.objects.create_user(username = correoU,
                                    email= correoU,
                                    password= contrasenaU)
    if "@ferremax.com" in correoU:
        user.is_staff = True    
        roluser = rol.objects.get(nombre_rol = "Administrador")
    else:
        user.is_staff = False
        roluser = rol.objects.get(nombre_rol = "Cliente")
    registroPreg = pregunta.objects.get(id_preg = preguntaU)
    
    usuario.objects.create(rut_usu = rutU,nombre_usu = nombreU,correo_usu = correoU,
                           contrasena_usu = contrasenaU,direccion_usu = direccionU,telefono_usu = telefonoU ,
                           rol_usu = roluser, id_preg = registroPreg)
    
    user.is_active = True
    user.save()
    return redirect('Sesion')

def iniciarsesion(request):
    usuario1 = request.POST['correo']
    contra1 = request.POST['clave']

    try: 
        user1 = User.objects.get(username = usuario1)
    except User.DoesNotExist:
        messages.error(request, 'El usuario o la contraseña son incorrectas')
        return render(request,'InicioSeccion_Registro.html')

    pass_valida = check_password(contra1, user1.password)
    if not pass_valida:
        messages.error(request, 'El usuario o la contraseña son incorrectas')
        return render(request,'InicioSeccion_Registro.html')

    usuario2 = usuario.objects.get(correo_usu = usuario1, contrasena_usu= contra1)
    user = authenticate(username = usuario1, password=contra1)

    if user is not None:
        login(request, user)
        if(usuario2.rol_usu.nombre_rol == "Administrador" ):
            return redirect('Vendedor')

        else: 
            return redirect('MenuPrincipalLogin')

    else:
        print("8")

def finsesion(request):
    logout(request)
    return redirect('MenuPrincipal')


@csrf_exempt
def add_algo(request):
    print('add_producto')
    url = 'http://127.0.0.1:8000/api/nada'
    try:
        if request.method == 'POST':
            my_list = request.POST.getlist('diccionario', [])
            json_data = {"nada": my_list}

            print(json_data)
            response = requests.post(url, json=json_data)
            response.encoding = 'utf-8'
            print('response code: {0}'.format(response.status_code))
            print('response body -> {0}'.format(response.json()))
            
            return JsonResponse({'status': response.status_code, 'response': response.json()})
        else:
            return HttpResponse("Method not allowed", status=405)
    except requests.exceptions.RequestException as e:
        print(f"ERROR al hacer la solicitud a {url}: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_algo(request):
    print('delete_algo')
    url = 'http://127.0.0.1:8000/api/nada'
    try:
        if request.method == 'DELETE':
            response = requests.delete(url)
            print('response code: {0}'.format(response.status_code))
            print('response body: {0}'.format(response.text))
            
            return JsonResponse({'status': response.status_code, 'response': response.text})
        else:
            return HttpResponse("Method not allowed", status=405)
    except requests.exceptions.RequestException as e:
        print(f"ERROR al hacer la solicitud DELETE a {url}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


"""   Webpay  """ 

def webpay_plus_create(request):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = request.POST.get('total')
    return_url = 'http://localhost:8000/webpay/commit'

    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
    response = tx.create(buy_order, session_id, amount, return_url)

    if response:
        return redirect(response['url'])
    else:
        return render(request, 'transbank/error.html')
    
@csrf_exempt
def webpay_checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data['cart']
        total = data['total']

        # Crear transacción Webpay
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        return_url = 'http://localhost:8000/webpay/commit'

        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
        response = tx.create(buy_order, session_id, total, return_url)

        if response:
            # Guardar datos del carrito y transacción en sesión o base de datos si es necesario
            request.session['cart'] = cart
            request.session['buy_order'] = buy_order
            request.session['session_id'] = session_id
            return JsonResponse({'success': True, 'url': response['url']})
        else:
            return JsonResponse({'success': False, 'error': 'No se pudo crear la transacción'})

@csrf_exempt
def webpay_plus_commit(request):
    print('commitpay')
    print("request: {0}".format(request.POST))    
    token = request.GET.get('token_ws')

    TBK_TOKEN = request.POST.get('TBK_TOKEN')
    TBK_ID_SESION = request.POST.get('TBK_ID_SESION')
    TBK_ORDEN_COMPRA = request.POST.get('TBK_ORDEN_COMPRA')

    #TRANSACCIÓN REALIZADA
    if TBK_TOKEN is None and TBK_ID_SESION is None and TBK_ORDEN_COMPRA is None and token is not None:

        #APROBAR TRANSACCIÓN
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
        response = tx.commit(token=token)
        print("response: {}".format(response)) 

        status = response.get('status')
        print("status: {0}".format(status))
        response_code = response.get('response_code')
        print("response_code: {0}".format(response_code)) 
        #TRANSACCIÓN APROBADA
        if status == 'AUTHORIZED' and response_code == 0:

            state = ''
            if response.get('status') == 'AUTHORIZED':
                state = 'Aceptado'
            pay_type = ''
            if response.get('payment_type_code') == 'VD':
                pay_type = 'Tarjeta de Débito'
            amount = int(response.get('amount'))
            amount = f'{amount:,.0f}'.replace(',', '.')
            transaction_date = dt.datetime.strptime(response.get('transaction_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
            transaction_date = '{:%d-%m-%Y %H:%M:%S}'.format(transaction_date)
            transaction_detail = {  'card_number': response.get('card_detail').get('card_number'),
                                    'transaction_date': transaction_date,
                                    'state': state,
                                    'pay_type': pay_type,
                                    'amount': amount,
                                    'authorization_code': response.get('authorization_code'),
                                    'buy_order': response.get('buy_order'), }

            # Obtener el carrito de la sesión
            cart = request.session.get('cart', [])
       

            delete_algo()
          

            return render(request, 'transbank/commit.html', {'transaction_detail': transaction_detail})
        else:
        #TRANSACCIÓN RECHAZADA
            delete_algo()   
            return render(request, 'transbank/rechazada.html')
    else:
    #TRANSACCIÓN CANCELADA
        delete_algo()              
        return render(request, 'transbank/error.html')

# FIN ACCIONES USUARIO

#ACCIONES ADMINISTRADOR(AGREGAR/MODIFICAR/ELIMINAR PRODUCTOS)

def agregarproducto(request):
    imagenP = request.FILES['imagen']
    nombreP = request.POST['nombre']
    descP = request.POST['descripcion']
    precioP = request.POST['precio']
    stockP = request.POST['stock']
    categoriaP = request.POST['categoria']
    cateescogida = categoria.objects.get(id_categoria=categoriaP)

    producto.objects.create(imagen=imagenP,nombre_prod=nombreP,descripcion=descP,precio=precioP,stock=stockP,id_categoria=cateescogida)
    return render(request,'inventarioAct.html')


def eliminarproducto(request, id_prod):
        eliminar = producto.objects.get(id_prod = id_prod)
        eliminar.delete()
        return redirect('Vendedor')

def modificarproducto(request,id_prod):

    imagenP = request.FILES['imagen']
    nombreP = request.POST['nombre']
    descP = request.POST['descripcion']
    precioP = request.POST['precio']
    stockP = request.POST['stock']
    categoriaP = request.POST['categoria']
    cateescogida = categoria.objects.get(id_categoria=categoriaP)

    prod = producto.objects.get(id_prod=id_prod)

    prod.imagen = imagenP
    prod.nombre_prod = nombreP
    prod.descripcion = descP
    prod.precio = precioP
    prod.stock = stockP
    prod.id_categoria = cateescogida

    prod.save()

    return redirect('Vendedor')