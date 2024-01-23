from django.shortcuts import render, redirect
from .models import StaffRegister
from master.utils.generate_unique_id import genrate_otp
from django.core.mail import send_mail
from django.conf import settings

def staff_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if 'staff_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login_view')  

    return wrapper

def login_view(request):
    print(request)
    if request.method == 'POST':
        login_id_ = request.POST['login_id']
        password_ = request.POST['password']
        try:
            print(login_id_, password_)
            get_staff = StaffRegister.objects.get(staff_id=login_id_)

        except StaffRegister.DoesNotExist:
            print("Invalid staff_id or password")
        else:
            if get_staff:
                print(password_ == get_staff.password)
                if password_ == get_staff.password:
                    request.session['staff_id'] = login_id_
                    request.session['role'] = get_staff.role.name
                    request.session['first_name'] = get_staff.first_name
                    request.session['last_name'] = get_staff.last_name
                    request.session['email'] = get_staff.email
                    request.session['mobile'] = get_staff.mobile
                    request.session['is_activated'] = get_staff.is_activated
                    return redirect('dashboard_view')
                    print("Now, you are logged in")
                else:
                    print("Your account is deactivated. Please contact to Admin.")
    return render(request, 'login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        try:
            check_user = StaffRegister.objects.get(email=email_)
        except StaffRegister.DoesNotExist:
            print("User doesn't exist")
        else:
            if check_user:
                otp_ = genrate_otp()
                subject = "Authentication Code for [Forgot password]"
                message = f"Code for [Password Change]: {otp_}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [f"{email_}"]
                send_mail(subject, message, from_email, recipient_list)
                check_user.otp = otp_
                check_user.save()
                context = {'email':email_}
                return render(request, 'otp-verification.html', context)
    return render(request, 'forgot-password.html')

def otp_verify_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']
        new_password_ = request.POST['new_password']
        confirm_password_ = request.POST['confirm_password']

        try:
            check_user = StaffRegister.objects.get(email=email_)
        except StaffRegister.DoesNotExist:
            print("User doesn't exist")
        else:
            if check_user:
                if check_user.otp == otp_:
                    if new_password_ == confirm_password_:
                        check_user.password = new_password_
                        check_user.save()
                        print("Password Changed")
                        return redirect('login_view')
                    else:
                        print("New password and confirm password  doesn't match")
                        context = {'email':email_}
                        return render(request, 'otp-verification.html', context)
                else:
                    print("Invalid OTP!!!")
                    context = {'email':email_}
                    return render(request, 'otp-verification.html', context)

    return render(request, 'otp-verification.html')

def logout(request):
    request.session.clear()
    return redirect('login_view')


# Create your views here.