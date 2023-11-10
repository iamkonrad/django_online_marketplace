from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from django_countries.fields import CountryField




class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique = True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    country= CountryField(blank_label='(select a country)')
    province = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    address = models. CharField(max_length=300)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_status = Vendor.objects.get(pk=self.pk)
            if original_status.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    mail_subject = "You are now allowed to operate on our platform."
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject = "You are not eligible to trade on our platform. Please contact the customer service."
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)
