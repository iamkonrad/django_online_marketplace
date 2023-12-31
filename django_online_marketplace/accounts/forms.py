from django import forms
from .models import User, UserProfile
from .validators import only_allow_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def clean (self):
        cleaned_data = super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords don't match!"
            )

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn-btn-info'}), validators=[only_allow_images_validator])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn-btn-info'}), validators=[only_allow_images_validator])
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address_line_1','address_line_2',
                  'country','province','city','postcode','latitude','longitude']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']