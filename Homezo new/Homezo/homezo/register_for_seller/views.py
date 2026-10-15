from django.shortcuts import render
from .models import RegisterForSeller
from login.models import Login
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
# Create your views here.
def reg(request):
    if request.method=='POST':
        obj=RegisterForSeller()
        obj.name=request.POST.get('text')
        obj.address=request.POST.get('address')
        obj.status='pending'
        obj.age=request.POST.get('age')
        obj.phone=request.POST.get('phone')
        obj.password=request.POST.get('Password')
        obj.brand_name=request.POST.get('Brand')
        obj.city=request.POST.get('City')
        obj.email=request.POST.get('Email')
        # obj.photo=request.POST.get('photo')
        my_file = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(my_file.name, my_file)
        obj.photo = my_file.name
        obj.save()

        ob=Login()
        ob.username=obj.name
        ob.password=obj.password
        ob.type='seller'
        ob.u_id=obj.sreg_id
        ob.save()
        return HttpResponseRedirect('/login/log/')
    return render(request,'register_for_seller/register2.html')

def manage(request):
    obj=RegisterForSeller.objects.all()
    c={
        'a':obj
    }

    return render(request,'register_for_seller/Manage seller.html',c)

def accept(request,idd):
    ob=RegisterForSeller.objects.get(sreg_id=idd)
    ob.status='accepted'
    ob.save()
    return manage(request)

def reject(request,idd):
    ob=RegisterForSeller.objects.get(sreg_id=idd)
    ob.status='rejected'
    ob.save()
    return manage(request)


def view_seller(request):
    ss=request.session['u_id']
    obj = RegisterForSeller.objects.filter(sreg_id=ss)
    c = {
        'a': obj
    }

    return render(request, 'register_for_seller/view_seller.html', c)

def update(request,idd):
    obj = RegisterForSeller.objects.get(sreg_id=idd)
    c = {
        'a': obj
    }
    if request.method == 'POST':
        obj = RegisterForSeller.objects.get(sreg_id=idd)
        obj.name = request.POST.get('text')
        obj.address = request.POST.get('address')
        obj.status = 'pending'
        obj.age = request.POST.get('age')
        obj.phone = request.POST.get('phone')
        obj.password = request.POST.get('Password')
        obj.brand_name = request.POST.get('Brand')
        obj.city = request.POST.get('City')
        obj.email = request.POST.get('Email')
        # obj.photo=request.POST.get('photo')
        if 'photo' in request.FILES:
            my_file = request.FILES['photo']
            fs = FileSystemStorage()
            fs.save(my_file.name, my_file)
            obj.photo = my_file.name
        obj.save()
        return view_seller(request)
    return render(request, 'register_for_seller/update.html', c)
