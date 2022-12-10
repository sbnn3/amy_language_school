from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at this time")
        return redirect(reverse('courses'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LpTaJGbUUYIYNsd6OgXBUWiW4SCdcxD0lBOH92TZnVWFiUCxSo7HC5NNYfJ9mpmaIfU84Smnz5sytOLUx7wJEGO00RhiP3u9i',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
