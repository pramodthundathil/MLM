from django.db import models
from Home.models import CustomUser

class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))
    

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=15,
        # validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    gst_number = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(15), MaxLengthValidator(15)])
    city = models.CharField(max_length=255)
    state = models.CharField(null=True,max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    contact_info = models.TextField(blank=True, null=True)
    supply_product = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staus = models.BooleanField(default=True)
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=20)
    # image = models.FileField(upload_to='category_images')
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=255)
    product_sub_name = models.CharField(max_length=255, null=True, blank=True, default=" ")
    price = models.FloatField()
    status = models.BooleanField(default=True)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    product_BV = models.FloatField()
    stock_alert_value = models.FloatField(default=0)
    image_primary = models.FileField(upload_to="product_image",null=True, blank=True)
    image_s1 = models.FileField(upload_to="product_image", null=True, blank=True)
    image_s2 = models.FileField(upload_to="product_image", null=True, blank=True)

    # Additional fields
    price_before_tax = models.FloatField(null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)

    # Tax calculation
    TAX_CHOICES = (
        ("Inclusive", "Inclusive"),
        ("Exclusive", "Exclusive"),
    )
    tax = models.CharField(max_length=20, choices=TAX_CHOICES)
    tax_value = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None:
            self.price = float(self.price)  # Ensure self.price is a float
            if self.tax_value:
                tax_rate = self.tax_value.tax_percentage / 100
                if self.tax == "Exclusive":
                    self.tax_amount = round(self.price * tax_rate, 2)
                    self.price_before_tax = round(self.price, 2)
                    self.price = round(self.price + self.tax_amount, 2)
                elif self.tax == "Inclusive":
                    self.price_before_tax = round(self.price / (1 + tax_rate), 2)
                    self.tax_amount = round(self.price - self.price_before_tax, 2)
            else:
                self.price_before_tax = round(self.price, 2)
                self.tax_amount = 0.0
        else:
            self.price_before_tax = 0.0
            self.tax_amount = 0.0

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
    total_bv = models.FloatField(default=0)
    status = models.BooleanField(default=True)


class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    house_house = models.CharField(max_length=20)
    Place = models.CharField(max_length=20)
    City = models.CharField(max_length=20)
    district  = models.CharField(max_length=20)
    state  = models.CharField(max_length=20)
    landmark = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return str(self.first_name + self.house_house + self.Place + self.City + self.district)


class Order(models.Model):
    order_numer = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order_amount = models.FloatField()
    order_tax = models.FloatField()
    order_bv = models.FloatField()
    order_date = models.DateField(auto_now_add=True)
    
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    delivery_history_address = models.CharField(max_length=255, null=True, blank=True) 

    order_completion = models.BooleanField(default=False)
    
    payment_status = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=20, null=True, default='Cash On delivery')
    payment_ref_number = models.CharField(max_length=20, null=True, blank=True)

    order_status = models.BooleanField(default=False)



class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
    total_bv = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    order_progress = models.CharField(max_length=20, choices=(
                                                                ("Ordered","Ordered"),
                                                                ("Accepted","Accepted"),
                                                                ("Despached","Despached"),
                                                                ("Out For Delivery","Out For Delivery"),
                                                                ("Delivered","Delivered")
                                                              ),
                                                              default="Ordered")


    


    


