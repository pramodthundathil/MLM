from django.urls import path 
from .import views 

urlpatterns = [
    path("Products",views.Products,name="Products"),
    path("ProductList",views.ProductList,name="ProductList"),
    path("Cart_Page",views.Cart_Page,name="Cart_Page"),
    path("ProductSingle/<int:pk>",views.ProductSingle,name="ProductSingle"),
    path("AddToCart/<int:pk>",views.AddToCart,name="AddToCart"),
    path('increase_quantity', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity', views.decrease_quantity, name='decrease_quantity'),
    path('deletefrom_cart/<int:pk>', views.deletefrom_cart, name='deletefrom_cart'),
    path('Place_Order_Start', views.Place_Order_Start, name='Place_Order_Start'),
    path("Paymentoptions/<int:pk>",views.Paymentoptions,name="Paymentoptions"),
    path("PlaceOrder",views.PlaceOrder,name="PlaceOrder"),
    
    path("myorders",views.myorders,name="myorders"),
    path("OrderPlaced",views.OrderPlaced,name="OrderPlaced"),
    path("Deleteoreder/<int:pk>",views.Deleteoreder,name="Deleteoreder"),
    path("MakeCashOnDelivery/<int:pk>",views.MakeCashOnDelivery,name="MakeCashOnDelivery")
]