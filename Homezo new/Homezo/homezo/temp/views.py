from django.shortcuts import render, get_object_or_404
from add_product.models import AddProduct
from catagory.models import Catagory

# Create your views here.
def admin(request):
    categories = Catagory.objects.all()
    return render(request, 'temp/admin.html', {'categories': categories})

def buyer(request):
    products = AddProduct.objects.all()[:4]
    return render(request, 'temp/buyer.html', {'products': products})

def seller(request):
    return render(request, 'temp/seller.html')

def home(request):
    products = AddProduct.objects.all()
    return render(request, 'temp/home.html', {'products': products})

# Products by category
def products_by_category(request, cat_name):
    categories = Catagory.objects.all()
    if cat_name == 'all':
        products = AddProduct.objects.all()
    else:
        products = AddProduct.objects.filter(cat__catagory=cat_name)
    
    # Apply sorting
    sort = request.GET.get('sort')
    if sort == 'low':
        products = products.order_by('product_price')
    elif sort == 'high':
        products = products.order_by('-product_price')
        
    context = {
        'd': products,
        'categories': categories,
        'selected_category': cat_name,
        'selected_sort': sort
    }
    return render(request, 'temp/view_products.html', context)

# Single product detail page
def product_detail(request, pro_id):
    product = get_object_or_404(AddProduct, pk=pro_id)
    categories = Catagory.objects.all()
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'temp/product_details.html', context)
