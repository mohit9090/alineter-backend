from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new Users
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating Users
    """
    password = ReadOnlyPasswordHashField() # Can only read

    class Meta:
        model = User
        fields = ['username', 'password', 'is_active']

    def clean_password(self):
        return self.initial["password"]