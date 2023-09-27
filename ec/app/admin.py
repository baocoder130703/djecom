from django.contrib import admin
from . models import Product ,Customer , Cart ,Payment ,OrderPlaced ,Wishlish
# Register your models here.
@admin.register(Product)
class ProductModeAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']
    

@admin.register(Cart)
class CartModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    

@admin.register(Payment)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    
@admin.register(OrderPlaced)
class OrderPlacedModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','payment']
    
    
@admin.register(Wishlish)
class WishlistModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
    