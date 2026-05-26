from django import forms
from django.contrib.auth.models import User
from .models import Teacher

class TeacherAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['password'].required = True
            self.fields['confirm_password'].required = True
        else:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")
        
        if not self.instance.pk:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists!")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists!")
        return cleaned_data

    def save(self, commit=True):
        teacher = super().save(commit=False)
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            teacher.user = user
        else:
            user = teacher.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            user.save()
            
        if commit:
            teacher.save()
        return teacher
