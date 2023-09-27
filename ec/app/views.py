from django.shortcuts import render , redirect
from urllib import request
from django.views import View
from django.http import HttpResponse , JsonResponse
from django.db.models import Count
from . forms import CustomerRegistrationForm, CutomerProfileForm
from django.contrib import messages
from . models import Customer ,Product ,Cart ,Wishlish
from django.db.models import Q
# Create your views here.
def home(req):
    totalitem = 0
    wishitem = 0
    if req.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = req.user))
        wishitem = len(Wishlish.objects.filter(user = req.user))
    return render(req,"app/home.html",locals())

def about(req):
    totalitem = 0
    wishitem = 0
    if req.user.is_authenticated:
        wishitem = len(Wishlish.objects.filter(user = req.user))
        totalitem = len(Cart.objects.filter(user = req.user))
    return render(req,'app/about.html',locals())
 
def contact(req):
    totalitem = 0
    wishitem = 0
    if req.user.is_authenticated:
        wishitem = len(Wishlish.objects.filter(user = req.user))
        totalitem = len(Cart.objects.filter(user = req.user))
    return render(req,"app/contact.html",locals())



class Category(View):
    def get(self,req,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title').annotate(total = Count('title'))
        totalitem = 0
        if req.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = req.user))
        return render(req,"app/category.html",locals())

class CategoryTitle(View):
     def get(self,req,val):
         product = Product.objects.filter(title = val)
         title = Product.objects.filter(category = product[0].category).values('title')
        
         return render(req,"app/category.html",locals())
     
class ProductDetail(View):
    def get(self,req,pk):
        product = Product.objects.get(pk = pk)
        wishlist = Wishlish.objects.filter(Q(product = product) & Q(user = req.user))
        
        totalitem = 0
        if req.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = req.user))
        return render(req,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,req):
        form = CustomerRegistrationForm()
        return render(req,'app/customerregistrantion.html',locals())
    def post(self,req):
         form = CustomerRegistrationForm(req.POST)
         if form.is_valid():
             form.save()
             messages.success(req," bạn đã đăng ký thành công ")
         else:
             messages.warning(req,'invalid input data')
             
         return render(req,'app/customerregistrantion.html',locals())
     
     
class ProfileView(View):
    def get(self,req):
        form = CutomerProfileForm()
        return render(req,'app/profile.html',locals())
    
    def post(self,req):
        form = CutomerProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = user,name=name,locality= locality ,city = city,mobile = mobile,state = state,zipcode = zipcode)
            reg.save()
            messages.success(req,'congratulation ! Profile Save successfull')
        else:
            messages.warning(req,'Invalid input data')
        return render(req,'app/profile.html',locals())
    
def address(req):
    add = Customer.objects.filter(user = req.user)
    return render(req,'app/address.html',locals())
class updateAddress(View):
    def get(self,req,pk):
        add = Customer.objects.get(pk=pk)
        form = CutomerProfileForm(instance=add)# hiện dữ liệu muốn thay
        return render(req,'app/updateAddress.html',locals())
    
    def post(self,req,pk):
        form = CutomerProfileForm(req.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            
            add.save()
            messages.success(req,'congratulation ! Profile Save successfull')
        else:
            messages.warning(req,'Invalid input data')
        return render(req,'app/updateAddress.html',locals())
    


def add_to_cart(req):
    user = req.user
    product_id = req.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user,product = product).save()
    return redirect('/cart')

def show_cart(req):
    user = req.user
    # lọc người dùng đăng nhập
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(req,'app/addtocart.html',locals())


class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request,'app/checkout.html',locals())
        
def plus_cart(req):
    if req.method == 'GET':
        prod_id = req.GET.get('prod_id')
        
        
        c = Cart.objects.get(Q(product = prod_id) & Q(user = req.user))
        c.quantity += 1
        c.save()
        user = req.user
        # lọc người dùng đăng nhập
        cart = Cart.objects.filter(user=user)
        
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def minus_cart(req):
    if req.method == 'GET':
        prod_id = req.GET.get('prod_id')
    
        c = Cart.objects.get(Q(product = prod_id) & Q(user = req.user))
        c.quantity -= 1
        c.save()
        user = req.user
        # lọc người dùng đăng nhập
        cart = Cart.objects.filter(user=user)
        
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(req):
    if req.method == 'GET':
        prod_id = req.GET.get('prod_id')
    
        c = Cart.objects.get(Q(product = prod_id) & Q(user = req.user))
        c.delete()
        user = req.user
        # lọc người dùng đăng nhập
        cart = Cart.objects.filter(user=user)
        
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



def plus_wishlist(req):
    if req.method == 'GET':
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = req.user
        Wishlish(user = user , product = product).save()
        data = {
            'message': 'wishlist added successfully',
        }
        return JsonResponse(data)
    
def minus_wishlist(req):
    if req.method == 'GET':
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = req.user
        Wishlish.objects.filter(user = user,product = product).delete()
        data = {
            'message': 'wishlist remove successfully',
        }
        return JsonResponse(data)
    


def search(req):
    query = req.GET['search']
    product = Product.objects.filter(Q(title__icontains = query))
    return render(req ,'app/search.html',locals())

def wish_list(req):
    user = req.user
    # lọc người dùng đăng nhập
    wish_list = Wishlish.objects.filter(user=user)
    
    
    return render(req,'app/wish_list.html',locals())
