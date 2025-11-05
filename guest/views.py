from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import *
import random
import pyotp, qrcode
from io import BytesIO
import base64

def verify_otp_google(request):
    message = ""
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        auth_type = request.session.get("auth_type")
        auth_id = request.session.get("auth_id")

        if auth_type == "user":
            user = User.objects.get(id=auth_id)
            totp = pyotp.TOTP(user.secret_key)
            if totp.verify(otp_entered):
                request.session["user_id"] = user.id
                return redirect("user:homepage")
            else:
                message = "Invalid OTP"

        if auth_type == "seller":
            seller = Seller.objects.get(id=auth_id)
            totp = pyotp.TOTP(seller.secret_key)
            if totp.verify(otp_entered):
                request.session["seller_id"] = seller.id
                return redirect("seller:homepage")
            else:
                message = "Invalid OTP"

    return render(request, "guest/google_otp_verify.html", {"message": message})




def generate_qr(request):
    secret = request.session.get("qr_secret")
    email = request.session.get("qr_email")

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name="YourAppName")

    qr = qrcode.make(uri)
    stream = BytesIO()
    qr.save(stream, format="PNG")
    qr_code = base64.b64encode(stream.getvalue()).decode()

    return render(request, "guest/display_qr.html", {"qr_code": qr_code})

# Create your views here.
def guest_home(request):
    return render(request,'guest/guest_home.html')

def guest_login(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        # Try User
        try:
            user = User.objects.get(user_email=email)
            if check_password(password, user.user_password):
                request.session["auth_type"] = "user"
                request.session["auth_id"] = user.id                
                return redirect("guest:verify_otp_google")
            else:
                return render(request, "guest/login.html", {"message": "Incorrect password"})
        except User.DoesNotExist:
            pass

        # Try Seller
        try:
            seller = Seller.objects.get(seller_email=email)
            if check_password(password, seller.seller_password):
                request.session["auth_type"] = "seller"
                request.session["auth_id"] = seller.id
                return redirect("guest:verify_otp_google")
            else:
                return render(request, "guest/login.html", {"message": "Incorrect password"})
        except Seller.DoesNotExist:
            return render(request, "guest/login.html", {"message": "Email not registered"})

    return render(request, "guest/login.html")


def user_register(request):
    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        secret = pyotp.random_base32()  # new Google Authenticator secret
        hashed_password = make_password(password)

        user = User.objects.create(
            user_name=name,
            user_email=email,
            user_password=hashed_password,
            secret_key=secret
        )

        request.session["qr_secret"] = secret
        request.session["qr_email"] = email
        return redirect("guest:generate_qr")
    else:
        return render(request, "guest/user_registration.html")



def seller_register(request):
    message = ""
    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        # Check duplicate email
        if Seller.objects.filter(seller_email=email).exists():
            message = "Email already registered"
            return render(request, "guest/seller_registration.html", {"message": message})
        
        secret = pyotp.random_base32()  # new Google Authenticator secret

        hashed_password = make_password(password)  # Argon2 hashing

        Seller.objects.create(
            seller_name=name,
            seller_email=email,
            seller_password=hashed_password,
            secret_key=secret

        )

        request.session["qr_secret"] = secret
        request.session["qr_email"] = email
        return redirect("guest:generate_qr")
    else:
        return render(request, "guest/seller_registration.html")