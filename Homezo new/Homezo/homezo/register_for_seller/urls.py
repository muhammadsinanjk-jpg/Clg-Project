from django.urls import path,re_path
from register_for_seller import views
urlpatterns = [
    path('add/',views.reg),
    path('manage_s/',views.manage),
    re_path('accept/(?P<idd>\w+)',views.accept),
    re_path('reject/(?P<idd>\w+)',views.reject),
    path('v_seller/', views.view_seller),
    re_path('up/(?P<idd>\w+)', views.update),

]