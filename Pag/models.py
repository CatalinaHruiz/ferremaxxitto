from django.db import models

#Tablas sin llaves foráneas 

class rol(models.Model):
    id_rol = models.AutoField(primary_key = True)
    nombre_rol = models.CharField(max_length= 40) 

class pregunta(models.Model):
    id_preg = models.AutoField(primary_key=True)
    nombre_preg = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_preg


class categoria(models.Model): 
    id_categoria = models.AutoField(primary_key = True)
    nombre_categoria = models.CharField(max_length= 60)


class proveedor(models.Model):
    id_prov = models.AutoField(primary_key = True)
    nombre_prov = models.CharField(max_length= 50)
    direccion_prov = models.CharField(max_length= 50)
    correo = models.CharField(max_length= 50) 
    telefono = models.IntegerField() 

# Tablas con 1 llave Foranea

class producto(models.Model):
    id_prod = models.AutoField(primary_key = True)
    imagen = models.ImageField()
    nombre_prod = models.CharField(max_length= 30)
    descripcion = models.CharField(max_length= 70)
    precio = models.IntegerField()
    stock = models.IntegerField()
    id_categoria = models.ForeignKey(categoria,on_delete=models.CASCADE)

class abastecimiento(models.Model):
    id_abastecimiento = models.AutoField(primary_key = True)
    fecha = models.DateField()
    total = models.IntegerField()
    id_proveedor = models.ForeignKey(proveedor,on_delete=models.CASCADE)
    

# Tablas con 2 claves foráneas

class usuario(models.Model):
    id_usuario = models.AutoField(primary_key= True)
    rut_usu = models.CharField(max_length= 60)  
    nombre_usu = models.CharField(max_length= 60)  
    correo_usu = models.CharField(max_length= 60)
    contrasena_usu = models.CharField(max_length=100,null=False, default='Gd01062018.')
    direccion_usu = models.CharField(max_length= 60)  
    telefono_usu = models.IntegerField()
    rol_usu = models.ForeignKey(rol,on_delete=models.CASCADE)
    id_preg = models.ForeignKey(pregunta,on_delete=models.CASCADE)


class detalle_abastecimiento (models.Model):
    id_detalle = models.AutoField(primary_key= True)
    cantidad = models.IntegerField()
    id_abastecimiento = models.ForeignKey(abastecimiento,on_delete=models.CASCADE)
    id_prod = models.ForeignKey(producto,on_delete=models.CASCADE)


class carrito(models.Model):
	id_carrito = models.AutoField(primary_key = True)
	fecha = models.DateField()
	total = models.IntegerField()
	id_usuario = models.ForeignKey(usuario,on_delete=models.CASCADE)


class detalle_carrito(models.Model):
    id_detalle = models.AutoField(primary_key= True)
    cantidad = models.IntegerField()
    id_carrito = models.ForeignKey(carrito,on_delete=models.CASCADE)
    id_producto = models.ForeignKey(producto,on_delete=models.CASCADE)