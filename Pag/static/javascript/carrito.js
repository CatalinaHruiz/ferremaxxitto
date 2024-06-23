function renderCart() {
    cartItemsContainer.innerHTML = '';
    let totalPrice = 0;

    cartItems.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        totalPrice += itemTotal;

        const itemElement = document.createElement('li');
        itemElement.textContent = `${item.name} x ${item.quantity} - $${itemTotal.toFixed(0)} CLP`;
        
        // Agrega un botón de eliminar para cada producto en el carrito
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Eliminar';
        deleteButton.addEventListener('click', () => {
            cartItems.splice(index, 1); // Elimina el producto del carrito
            renderCart(); // Vuelve a renderizar el carrito
        });

        itemElement.appendChild(deleteButton);
        cartItemsContainer.appendChild(itemElement);
    });

    cartTotalElement.textContent = totalPrice.toFixed(0);
}
