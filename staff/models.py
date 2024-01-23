from django.db import models
from master.models import BaseClass, CounterTable
from django.core.mail import send_mail
from django.conf import settings
from master.utils import generate_unique_id


class StaffRole(BaseClass):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class StaffRegister(BaseClass):
    staff_id = models.CharField(primary_key=True,max_length=255, blank=True)
    role = models.ForeignKey(StaffRole, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank =True)
    login_credential_sent = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, default="658734", blank=True)
    is_activated = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.staff_id} {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
       
        if not self.staff_id:
            
            last_id = CounterTable.objects.get(id=2)
            last_id.last_staff_id = last_id.last_staff_id + 1
            last_id.save()
            self.staff_id = 'MC000' + str(last_id.last_staff_id)
            
        if not self.password:
            self.password = generate_unique_id.genrate_password()

        if not self.login_credential_sent:
            subject = f'Login credential from | Medi-Center for {self.first_name} {self.last_name}'
            message = f'STAFF_ID = {self.staff_id}\nPASSCODE = {self.password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [f'{self.email}']
            send_mail(subject, message, from_email, recipient_list)
            self.login_credential_sent = True

        super(StaffRegister, self).save(*args, **kwargs)
