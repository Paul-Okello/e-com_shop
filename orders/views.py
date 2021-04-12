from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    #Obtain cart from session
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        #validate data sent in the form
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['price'],
                                         quantity=item['quantity'])
            #clear the cart
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form
    })
