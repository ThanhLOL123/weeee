from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
import datetime
from django.contrib import messages
from .models import *
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required 
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
#        user_not_login = "hidden"
#        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
#        user_not_login = "show"
#        user_login = "hidden"
    products = Product.objects.annotate(total_quantity_sold=Sum('orderitem__quantity')).order_by('-total_quantity_sold')[:8]

    context = {'products':products, 'cartItems':cartItems} #,'user_not_login': user_not_login,'user_login':user_login,}
    return render(request, 'home.html',context)

def blog(request):
    return render(request, 'blog.html')
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if username is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('register')
    context = {}
    return render(request,'login.html', context)
def shop(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
    else:
        items = []
        cartItems = 0
    
    products = Product.objects.all()
    
    # Phân trang sản phẩm
    paginator = Paginator(products, 8)  # Số sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categorys = Category.objects.all()
    context = {
        'products': page_obj,  # Chuyển đối tượng phân trang vào context
        'items': items,
        'cartItems': cartItems,
        'categorys': categorys
    }
    return render(request, 'shop.html', context)
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request,'register.html', context)
def logoutPage(request):
    logout(request)
    return redirect ('home')
def contact(request):
    return render(request,'contact.html')

def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
    else:
        items = []
    # Truy vấn sản phẩm được mua nhiều nhất và có giá rẻ nhất
    most_purchased_and_cheapest_product = Product.objects.annotate(
        total_purchased=Count('orderitem')
    ).order_by('-total_purchased', 'price').first()
    top_selling_products = Product.objects.annotate(total_quantity_sold=Sum('orderitem__quantity')).order_by('-total_quantity_sold')[:4]
    top_10 = Product.objects.annotate(total_quantity_sold=Sum('orderitem__quantity')).order_by('-total_quantity_sold')[:6]
    products = Product.objects.all()
    categorys = Category.objects.all()
    
    context = {'products':products, 'items':items , 'categorys':categorys,'bestChoice':most_purchased_and_cheapest_product,'top':top_selling_products,'top10':top_10}
    return render(request,'index.html',context)
@login_required
def manage_cart(request):
    data = json.loads(request.body)
    action = data.get('action')
    product_id = data.get('productId')
    quantity = data.get('quantity', 1)

    if product_id:
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        
        if action == 'add':
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += quantity
            order_item.save()

        elif action == 'update':
            order_item = OrderItem.objects.get(order=order, product=product)
            order_item.quantity = quantity
            order_item.save()

        elif action == 'remove':
            order_item = OrderItem.objects.get(order=order, product=product)
            order_item.delete()
        order.get_cart_total()  # Update order total

        return JsonResponse(f'{action.capitalize()}d cart item successfully', safe=False)
    
def addCart(request):
    if request.method == 'POST':
        id = request.POST['iddddd']
        quantity = request.POST['quantity']
        product = Product.objects.get(id=id)
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += int(quantity)
        order_item.save()
        order.get_cart_total()
        return redirect(f'/detail?id={id}')
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
#        user_not_login = "hidden"
#        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
#        user_not_login = "show"
#        user_login = "hidden"
    id = request.GET.get('id','')
    product = Product.objects.filter(id=id)
    categorys = Category.objects.all()
    context = {'product':product, 'cartItems':cartItems,'categorys':categorys,'items':items}
    return render(request,'product-details.html',context)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer= customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = Order.get_cart_items
        else:
            items = []
            order = {'get_cart_items': 0,'get_cart_total':0}
            cartItems = ['order.get_cart_items']
    context = {"searched": searched, "products": keys, 'items':items}
    return render(request,'search.html', context)
def search1(request):
    if request.method == "POST":
        searched = request.POST["searched1"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
#        user_not_login = "hidden"
#        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
#        user_not_login = "show"
#        user_login = "hidden"

    products = Product.objects.all()
    return render(request,'search.html', {"searched": searched, "keys": keys, 'products': products,'items':items})
def processOrder(request):
    if request.user.is_authenticated:
        return redirect('shop_cart')
    else:
        return redirect('login')
    
def category(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    
    categories = Category.objects.filter()
    active_category = request.GET.get('category','')#cái danh mục đang đc người dùng chọn
    products = Product.objects.all()
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories,'products': products, 'active_category': active_category,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'category.html', context)

def dashboard(request):
    return HttpResponseRedirect("https://app.powerbi.com/reportEmbed?reportId=1cc483a0-315f-4b4c-9c4d-21ecbecf6c1a&autoAuth=true&ctid=e7572e92-7aee-4713-a3c4-ba64888ad45f")
def community(request):
    return render(request,'community.html')
def shop_cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = Order.get_cart_items
    else:
        items = []
        cartItems=[]
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {'products':products, 'items':items ,'cartItems':cartItems,'categorys':categorys,'order':order}
    return render(request,'shop_cart.html',context)
def shop_checkout(request):  
    transaction_id = datetime.datetime.now().timestamp()
    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        phone = request.POST['phone']
        email = request.POST['email']
        note = request.POST['note']
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        payment = Payment.objects.create(order = order)
        payment.payment_method = 'Cash'
        payment.payment_id =transaction_id
        payment.amount = order.get_cart_total()
        payment.townOrCity= city
        payment.address = address
        payment.phone= phone
        payment.mail= email
        payment.note= note
        orderP= order
        order.complete = True
        payment.save()
        order.save()
        context ={ 'orderP' :orderP,'payment':payment}
        return render(request,'complete.html',context)
    return render(request,'shop_checkout.html')


