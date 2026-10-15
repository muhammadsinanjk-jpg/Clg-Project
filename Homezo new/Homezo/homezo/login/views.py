import smtplib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Login
from register_for_buyer.models import RegisterForBuyer
from register_for_seller.models import RegisterForSeller


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Safely fetch the matching user record
        ob = Login.objects.filter(username=username, password=password).first()

        if not ob:
            return render(request, 'login/login.html', {
                'msg': 'Invalid Username or Password'
            })

        tp = ob.type
        uid = ob.u_id

        # 1. ADMIN
        if tp == 'admin':
            request.session['u_id'] = uid
            request.session['type'] = 'admin'
            return HttpResponseRedirect('/temp/admin/')

        # 2. BUYER
        elif tp == 'buyer':
            request.session['u_id'] = uid
            request.session['type'] = 'buyer'
            return HttpResponseRedirect('/temp/buyer/')

        # 3. SELLER
        elif tp == 'seller':
            try:
                seller = RegisterForSeller.objects.get(sreg_id=uid)

                if seller.status == 'accepted':
                    request.session['u_id'] = uid
                    request.session['type'] = 'seller'
                    return HttpResponseRedirect('/temp/seller/')
                elif seller.status == 'pending':
                    msg = 'Your seller account is pending approval.'
                elif seller.status == 'rejected':
                    msg = 'Your seller account has been rejected.'
                else:
                    msg = 'Invalid seller status.'

            except RegisterForSeller.DoesNotExist:
                msg = 'Seller account not found.'

            return render(request, 'login/login.html', {'msg': msg})

        # Fallback for unexpected user type
        return render(request, 'login/login.html', {'msg': 'Unauthorized user type.'})

    return render(request, 'login/login.html')


def forgotpassword(request):
    if request.method == 'POST':
        em = request.POST.get('email')

        # Check seller table first
        seller = RegisterForSeller.objects.filter(email=em).first()

        if seller:
            email = "projectmailbg@gmail.com"
            sub = "Password Recovery"
            msg = seller.password
        else:
            # Check buyer table
            buyer = RegisterForBuyer.objects.filter(email=em).first()
            if buyer:
                email = "projectmailbg@gmail.com"
                sub = "Password Recovery"
                msg = buyer.password
            else:
                return render(request, 'login/forgott.html', {
                    'error': 'Email not registered'
                })

        try:
            text = f"Subject: {sub}\n\nYour password is: {msg}"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, "iqjjrhsyerovorav")
            server.sendmail(email, em, text)
            server.quit()

            return render(request, 'login/forgott.html', {
                'success': 'Password sent to your email.'
            })
        except Exception as e:
            return render(request, 'login/forgott.html', {
                'error': f'Failed to send email: {str(e)}'
            })

    return render(request, 'login/forgott.html')


def logout(request):
    request.session.flush()  # Completely flushes session data and cookie
    return HttpResponseRedirect('/login/log/')