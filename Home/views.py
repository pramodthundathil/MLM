from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .models import *

from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ecom.models import *

def SentRefrelLink(request):
    if request.method == "POST":
        try:
            userdetails = request.user
            activationkey = userdetails.id_number
        except:
            userdetails = request.user
            activationkey = userdetails.id_number
            
        email = request.POST['email']
        current_site = get_current_site(request)
        mail_subject = 'Direct Selling Employees Socity Joining Link'
        path = "SignUp"
        message = render_to_string('emailbody.html', {'user': request.user,
                                                                        'domain': current_site.domain,
                                                                        'path':path,
                                                                        'token':activationkey,})

        email = EmailMessage(mail_subject, message, to=[email])
        email.send(fail_silently=True)
                    
        return redirect("ProfileScreen")

import uuid
import random

def generate_otp(user):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])  # Generate a 4-digit OTP
    UserOTP.objects.create(user=user, otp=otp)
    return otp

def generate_unique_id_number():
    return str(uuid.uuid4().hex[:5]).upper()

def SignUp(request,token):
    form = CustomUserCreationForm()
    sponser = CustomUser.objects.get(id_number = token)
    
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        village = request.POST.get('village')
        district = request.POST.get('district')
        address = request.POST.get('address')
        religion = request.POST.get('religion')
        cast = request.POST.get('cast')
        pan = request.POST.get('pan')
        ac_num = request.POST.get('ac_num')
        branch = request.POST.get('branch')
        ifsc = request.POST.get('ifsc')
        nomine = request.POST.get('nomine')
        id_card = request.FILES.get('id_card')
        pnum = request.POST.get('pnum')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        cpassword = request.POST.get('cpassword')

        if pswd != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            user = CustomUser.objects.create(
                email=email,
                id_number=generate_unique_id_number(),
                first_name=fname,
                last_name=lname,
                date_of_birth=dob,
                age=age,
                village=village,
                district=district,
                address=address,
                religion=religion,
                cast=cast,
                pancard=pan,
                phone_number=pnum,
                role='user',
                parent = sponser,
                is_active = False
            )
            user.set_password(pswd)
            user.save()
            otp = generate_otp(user)

            Business_Volume.objects.create(user=user)
            AccountDetails.objects.create(
                user=user,
                ifsc_code=ifsc,
                branch_name=branch,
                account_number=ac_num
            )
            Nominee.objects.create(
                user=user,
                nominee_name=nomine,
                id_proof=id_card
            )
            email = request.POST['email']
            current_site = get_current_site(request)
            mail_subject = 'OTP for Account Creation DSES'
            path = "SignUp"
            message = render_to_string('emailbody_otp.html', {'user': user,
                                                                'domain': current_site.domain,
                                                                'path':path,
                                                                'token':otp,})

            email = EmailMessage(mail_subject, message, to=[email])
            email.send(fail_silently=True)

            messages.success(request, "User registered successfully.")
            return redirect('OTPverification', pk = user.id)
        except ValidationError as e:
            messages.error(request, e.messages)
            return redirect('register')

    # return redirect(SignUp, token = token)


    context = {
        "form":form,
        "sponsor":sponser
    }
    return render(request,'register.html',context)

def OTPverification(request,pk):
    user = CustomUser.objects.get(id = pk)

    context = {
        "user":user
    }
    return render(request,"otpvalidation.html",context)

def verify_otp(request, pk):
    if request.method == 'POST':
        otp = request.POST['otp']
        user = CustomUser.objects.get(id = pk)
        try:
            user_otp = UserOTP.objects.get(user=user, otp=otp)
            if user_otp:
                # OTP is correct
                user.is_active = True
                user.save()
                user_otp.delete()
                return redirect('VeryfiedOTP')
        except UserOTP.DoesNotExist:
            # OTP is incorrect
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verified_otp.html')
def VeryfiedOTP(request):
    return render(request, 'verified_otp.html')

def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pswd = request.POST['pswd']
        user = authenticate(request,email = uname, password = pswd)
        if user is not None:
            user = login(request,user)
            return redirect('Index')
        else:
            messages.error(request,"username or password in correct")
            return redirect("SignIn")
    else:
        return render(request,"login.html")
    
def SignOut(request):
    logout(request)
    return redirect("Index")

def Index(request):
    product = Product.objects.all()[:9]


    context = {
        "products":product
    }

    return render(request,"index.html",context)



def ProfileScreen(request):
    user = request.user
    BV = Business_Volume.objects.get(user = user)
    bankdetails = AccountDetails.objects.get(user = user)
    noinee = Nominee.objects.get(user = user)
    # print(user.first_name,"------------------------------------")
    context = {
        "BV":BV,
        "bankdetails":bankdetails,
        "noinee":noinee
    }
    return render(request,"userprofile.html",context)


# views.py

@csrf_exempt
def get_child_users(request, user_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        userid = request.POST.get('userId')

        print(userid,"---------------------------------------------")
        user = CustomUser.objects.get(id=int(userid))
        children = CustomUser.objects.filter(parent = user)  # Use related_name 'children'
        
        child_data = []
        for child in children:
            child_data.append({
                'id': child.id,
                'first_name': child.first_name,
                'status': child.role,  # Assuming status is based on the role
                'left_count': 0,  # Adjust based on actual logic
                'right_count': 0  # Adjust based on actual logic
            })
        
        return JsonResponse(child_data, safe=False)
    
def about(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')




