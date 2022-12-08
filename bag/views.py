from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from courses.models import Course


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    course = get_object_or_404(Course, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {course.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {course.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified course to the specified amount """

    course = get_object_or_404(Course, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {course.name} quantity to {bag[item_id]}')
    else:
        del bag[item_id]
        if not bag[item_id]:
            bag.pop(item_id)
            messages.success(request, f'Removed {course.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try: 
        course = get_object_or_404(Course, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {course.name} from your bag')

        request.session['bag'] = bag

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)