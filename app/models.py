from django.db import models
import os
import datetime
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
#from multiselectfield import MultiSelectField
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name','password1', 'password2']


# a=[
#         ('action', 'Action'),
#         ('adventure', 'Adventure'),
#         ('rpg', 'Role-playing'),
#         ('strategy', 'Strategy'),
#         ('simulation', 'Simulation'),
#     ]
# OPTION_A = 'A'
# OPTION_B = 'B'
# OPTION_C = 'C'

# CHOICES = [
#         (OPTION_A, 'Option A'),
#         (OPTION_B, 'Option B'),
#         (OPTION_C, 'Option C'),
#     ]
# Create your models here.

# class Customer(models.Model):
#     customer_id = models.CharField(max_length=10, primary_key= True)
#     customer_name = models.TextField(max_length= 40, blank = True)
#     customer_address = models.TextField(max_length= 100,  blank = True)
#     phone = models.TextField(max_length=10,  blank = True)
#     email = models.TextField(max_length=40,  blank = True)
#     customer_password = models.TextField(max_length=50,  blank = True)

# class Product(models.Model):
#     product_id = models.CharField(max_length =32 ,   primary_key= True)
#     product_name = models.TextField(max_length= 100,  blank = True)
#     price = models.TextField(max_length=20,  blank = True)
#     product_detail = models.TextField(max_length=400,  blank = True)
#     publisher = models.CharField(max_length=2, choices = CHOICES)
#     genre = models.TextField(max_length=100, blank = True)
#     year = models.TextField(max_length=20, blank = True)
#     status = models.TextField(max_length=10, blank = True)
#     img = models.ImageField(null= True,blank=True)

#     OPTION_A = 'A'
#     OPTION_B = 'B'
#     OPTION_C = 'C'

#     CHOICES = [
#         (OPTION_A, 'Option A'),
#         (OPTION_B, 'Option B'),
#         (OPTION_C, 'Option C'),
#     ]
# class Staff(models.Model):
#     staff_id = models.CharField(max_length=20, primary_key= True)
#     staff_name = models.TextField(max_length=40, blank = True)
#     phone = models.TextField(max_length=10, blank = True)
#     email = models.TextField(max_length=40, blank = True)
#     staff_password = models.TextField(max_length=40, blank = True)

# class Order(models.Model):
#     order_id = models.CharField(max_length=20, primary_key= True)
#     order_price = models.TextField(max_length=50, blank = True)
#     date_created = models.TextField(max_length=10, blank = True)
#     customer_id = models.ForeignKey("customer", verbose_name=(""), on_delete=models.DO_NOTHING)
#     product_id = models.ForeignKey("product", verbose_name=(""), on_delete=models.DO_NOTHING)
#     staff_id = models.ForeignKey("staff", verbose_name=(""), on_delete=models.DO_NOTHING)
    
#     def __str__(self):
#         return str(self.id)
#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all() #lay het tu orderitems
#         total = sum([item.quantity for item in orderitems])
#         return total
# class Invoice(models.Model):
#     invoice_id = models.CharField(max_length=10, primary_key= True)
#     invoice_cost = models.TextField(max_length= 50, blank = True)
#     Payment_methods = models.TextField(max_length=50, blank = True)
#     date_created = models.TextField(max_length= 10, blank = True)
#     status = models.TextField(max_length=20, blank = True)
#     order_id = models.ForeignKey("order", verbose_name=(""), on_delete=models.DO_NOTHING)
#     customer_id = models.ForeignKey("customer", verbose_name=(""), on_delete=models.DO_NOTHING)

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=False)
#     order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=False)
#     quantity = models.IntegerField(default=0,null=True,blank=True)
#     date_added = models.DateTimeField(auto_now_add = True)
class Category(models.Model):
    name = models.CharField(max_length=500,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=500,null=True)
    price = models.FloatField()
    img = models.ImageField(null=True, blank=True)
    publisher = models.CharField(max_length=20,null=True, blank=True )
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
            return url
    def photo(self):
        return mark_safe('<img src ="{}" width = 60>'.format(self.ImageURL))
class Order(models.Model):
    
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    complete = models.BooleanField(default=False,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200,null=True)
    total = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() #lay het tu orderitems
        total = sum([item.quantity for item in orderitems])
        return total
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() #lay het tu orderitems
        total = sum([item.get_total for item in orderitems])
        self.total = total
        self.save()
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=False)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=False)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null= True)
    address = models.CharField(max_length=100,null=True,blank=True)
    townOrCity = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    mail = models.CharField(max_length=100,null=True,blank=True)
    note = models.CharField(max_length=200,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    

