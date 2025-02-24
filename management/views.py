from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def product_list(request):
    """Vista para listar los productos disponibles"""
    products = Product.objects.all()
    return render(request, 'management/product_list.html', {'products': products})

@staff_member_required
def add_product(request):
    """Vista para agregar un nuevo producto"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:product_list')
    else:
        form = ProductForm()
    return render(request, 'management/product_form.html', {'form': form, 'action': 'Agregar'})

@staff_member_required
def edit_product(request, pk):
    """Vista para editar un producto existente"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('management:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'management/product_form.html', {'form': form, 'action': 'Editar'})
