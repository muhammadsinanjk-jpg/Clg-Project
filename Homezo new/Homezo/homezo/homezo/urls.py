from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add this line to redirect the root URL directly to your login page
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    
    path('add_product/', include('add_product.urls')),
    path('catagory/', include('catagory.urls')),
    path('login/', include('login.urls')),
    # ... your other paths
]