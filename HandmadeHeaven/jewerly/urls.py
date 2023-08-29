from django.conf.urls.static import static
from django.urls import path

from HandmadeHeaven import settings
from .views import *

urlpatterns = [
                  path('', home, name="home"),
                  path('store/', store, name="store"),
                  path('jewerly/<int:pk>/', jewerly_details, name="jewerly_details"),
                  path('login/', login_view, name="login"),
                  path('register/', register_view, name="register"),
                  path('logout/', logout_view, name="logout"),
                  path('faq/', faq_view, name="faq"),
                  path('cart/', cart_view, name="cart"),
                  path('successful_order/', successful_order_view, name="successful_order"),
                  path('my_orders/', my_orders_view, name="my_orders"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
