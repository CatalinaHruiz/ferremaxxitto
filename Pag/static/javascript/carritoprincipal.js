var shoppingCart = (function() {
  var cart = [];

  // Constructor
  function Item(name, price, count) {
    this.name = name;
    this.price = price;
    this.count = count;
  }

  // Guardar carrito
  function saveCart() {
    sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
  }

  // Cargar carrito
  function loadCart() {
    cart = JSON.parse(sessionStorage.getItem('shoppingCart')) || [];
  }

  loadCart();

  var obj = {};

  // Agregar al carrito
  obj.addItemToCart = function(name, price, count) {
    var added = false;
    for (var i in cart) {
      if (cart[i].name === name) {
        cart[i].count += count;
        added = true;
        break;
      }
    }
    if (!added) {
      var item = new Item(name, price, count);
      cart.push(item);
    }
    saveCart();
  };

  // Establecer la cantidad de un ítem
  obj.setCountForItem = function(name, count) {
    for (var i in cart) {
      if (cart[i].name === name) {
        cart[i].count = count;
        break;
      }
    }
    saveCart();
  };

  // Quitar un ítem del carrito
  obj.removeItemFromCart = function(name) {
    for (var i in cart) {
      if (cart[i].name === name) {
        cart[i].count--;
        if (cart[i].count === 0) {
          cart.splice(i, 1);
        }
        break;
      }
    }
    saveCart();
  };

  // Quitar todos los ítems del carrito
  obj.removeItemFromCartAll = function(name) {
    for (var i in cart) {
      if (cart[i].name === name) {
        cart.splice(i, 1);
        break;
      }
    }
    saveCart();
  };

  // Limpiar carrito
  obj.clearCart = function() {
    cart = [];
    saveCart();
  };

  // Contar todos los ítems en el carrito
  obj.totalCount = function() {
    var totalCount = 0;
    for (var i in cart) {
      totalCount += cart[i].count;
    }
    return totalCount;
  };

  // Calcular el total del carrito
  obj.totalCart = function() {
    var totalCart = 0;
    for (var i in cart) {
      totalCart += cart[i].price * cart[i].count;
    }
    return Number(totalCart.toFixed(2));
  };

  // Listar el carrito
  obj.listCart = function() {
    var cartCopy = [];
    for (var i in cart) {
      var item = cart[i];
      var itemCopy = {};
      for (var p in item) {
        itemCopy[p] = item[p];
      }
      itemCopy.total = Number(item.price * item.count).toFixed(2);
      cartCopy.push(itemCopy);
    }
    return cartCopy;
  };

  return obj;
})();

// Evento click para agregar al carrito
$('.add-to-cart').click(function(event) {
  event.preventDefault();
  var name = $(this).data('name');
  var price = Number($(this).data('price'));
  var quantity = parseInt($('#quantity-' + name).val()) || 1; // Asegura que la cantidad sea al menos 1 si no se especifica
  shoppingCart.addItemToCart(name, price, quantity);
  displayCart();
});

// Evento click para limpiar el carrito
$('.clear-cart').click(function() {
  shoppingCart.clearCart();
  displayCart();
});

// Mostrar el carrito
function displayCart() {
  var cartArray = shoppingCart.listCart();
  var output = "";
  for (var i in cartArray) {
    output += "<tr>"
      + "<td>" + cartArray[i].name + "</td>" 
      + "<td>" + cartArray[i].price + "</td>"
      + "<td><div class='input-group'><button class='minus-item input-group-addon btn btn-primary' data-name=" + cartArray[i].name + ">-</button>"
      + "<input type='number' class='item-count form-control' data-name='" + cartArray[i].name + "' value='" + cartArray[i].count + "'>"
      + "<button class='plus-item btn btn-primary input-group-addon' data-name=" + cartArray[i].name + ">+</button></div></td>"
      + "<td><button class='delete-item btn btn-danger' data-name=" + cartArray[i].name + ">X</button></td>"
      + " = " 
      + "<td>" + cartArray[i].total + "</td>" 
      +  "</tr>";
  }
  $('.show-cart').html(output);
  $('.total-cart').html(shoppingCart.totalCart());
  $('.total-count').html(shoppingCart.totalCount());
}

// Evento click para eliminar un ítem del carrito
$('.show-cart').on("click", ".delete-item", function(event) {
  var name = $(this).data('name');
  shoppingCart.removeItemFromCartAll(name);
  displayCart();
});

// Evento click para reducir la cantidad de un ítem
$('.show-cart').on("click", ".minus-item", function(event) {
  var name = $(this).data('name');
  shoppingCart.removeItemFromCart(name);
  displayCart();
});

// Evento click para aumentar la cantidad de un ítem
$('.show-cart').on("click", ".plus-item", function(event) {
  var name = $(this).data('name');
  shoppingCart.addItemToCart(name, 0, 1); // Asegura que al aumentar sea 1
  displayCart();
});

// Evento change para actualizar la cantidad de un ítem
$('.show-cart').on("change", ".item-count", function(event) {
   var name = $(this).data('name');
   var count = Number($(this).val());
   shoppingCart.setCountForItem(name, count);
   displayCart();
});

// Mostrar detalles del producto
function showDetails(detailsId) {
  var detailsElement = document.getElementById(detailsId);
  if (detailsElement.style.display === "" || detailsElement.style.display === "none") {
    detailsElement.style.display = "block";
    var yOffset = -50; // Ajusta este valor según sea necesario
    var elementPosition = detailsElement.getBoundingClientRect().top;
    window.scrollTo({
      top: elementPosition + window.pageYOffset + yOffset,
      behavior: "smooth"
    });
  } else {
    detailsElement.style.display = "none";
  }
}

// Función para incrementar la cantidad
function increaseQuantity(quantityId) {
  var quantityInput = document.getElementById(quantityId);
  var currentValue = parseInt(quantityInput.value);
  quantityInput.value = currentValue + 1;
}

// Función para decrementar la cantidad
function decreaseQuantity(quantityId) {
  var quantityInput = document.getElementById(quantityId);
  var currentValue = parseInt(quantityInput.value);
  if (currentValue > 1) {
    quantityInput.value = currentValue - 1;
  }
}

// Mostrar carrito inicialmente al cargar la página
displayCart();
