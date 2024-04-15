from django.shortcuts import render, redirect
from .models import Products, Orders
from .models import PetProfile
from django.contrib.auth.decorators import login_required



from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here
def index(request):
    product_objects = Products.objects.all()
#search code
    item_name =request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = Products.objects.filter(title__icontains=item_name)

#paginator code
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    return render(request, 'shop/index.html',{'product_objects':product_objects})


def detail(request, id):
    product_object = Products.objects.get(id=id)
    return render(request, 'shop/detail.html',{'product_object':product_object})



@login_required
def view_profile(request):
    user = request.user
    pets = PetProfile.objects.filter(owner=user)
    return render(request, 'shop/profile.html')



def checkout(request):
    if request.method == 'POST':
        # Variables are initialized via POST data
        items=request.POST.get('items', "")
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zip = request.POST.get('zip', "")
        total=request.POST.get('total', "")

        # Create and save the order when POST data is received
        order = Orders(items=items, name=name, email=email, address=address, city=city, state=state, zip=zip,total=total)
        order.save()

        # Redirect to a success page or render a template directly
        return render(request, 'shop/checkout.html')
    else:
        # For GET and other methods, typically you show the form to fill out
        # You could also include initial data or context if necessary
        return render(request, 'shop/checkout.html')