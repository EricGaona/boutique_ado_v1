from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None    # esto y el if de abajo es para el SIZE
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    #   _____     aqui usamos SESSION guardar la informacion en la varible session    ______
    bag = request.session.get('bag', {})
    #   este if es para el SIZE
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        #   este if ya estaba aqui, pero ahora entra dentro del else 
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    # print(request.session['bag'])
    return redirect(redirect_url)