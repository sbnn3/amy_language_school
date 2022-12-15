from django.shortcuts import render
from .forms import MessageForm
from django.contrib import messages


def message(request):
    """
    Saves the contact form to database
    """
    form = MessageForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent to Admin!')
            
            return render(request, "home/index.html")
        else:
            messages.error(request, 'Failed to send a message. Please, make sure the form is valid!')
    else:
        form = MessageForm()
        context = {
            'form': form,
        }
        return render(request, 'contact/contact.html', context)
    return render(request, 'contact/contact.html')