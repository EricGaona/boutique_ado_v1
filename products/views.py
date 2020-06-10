from django.shortcuts import render,  redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    #   ----------    inicio del codigo para la query   -------------
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        #   ----------    inicio del codigo para la query -- sort  -------------
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':           #  __________   estas 2 lineas de codigo de aqui se anaden en el video part2
                sortkey = 'category__name'      #  __________   estas 2 lineas de codigo de aqui se anaden en el video part2
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        #   ----------    fin del codigo para la query  -- sort -------------
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    #   ----------    fin del codigo para la query   -------------

    current_sorting = f'{sort}_{direction}'    #   ----------    tambien es codigo para la query  --  sort -------------

    context = {
        'products': products,
        'search_term': query,       #   ----------    tambien es codigo para la query   -------------
        'current_categories': categories,
        'current_sorting': current_sorting,     #   ----------    tambien es codigo para la query  --  sort -------------
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)