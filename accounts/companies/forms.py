from django import forms
from accounts.users.models import User, UserProfile
from django.contrib.auth.hashers import make_password

class CompanyAdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # Profile fields
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=UserProfile._meta.get_field("gender").choices, required=False)
    phone_1 = forms.CharField(required=False)
    phone_2 = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def save(self, commit=True, company=None):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["email"]
        user.company = company
        user.is_company_admin = True
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                middle_name=self.cleaned_data.get("middle_name"),
                gender=self.cleaned_data.get("gender"),
                phone_1=self.cleaned_data.get("phone_1"),
                phone_2=self.cleaned_data.get("phone_2"),
            )
        return user
