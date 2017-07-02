from django import forms

from member import models


class MemberEditForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)

    class Meta:
        model = models.Member
        fields = ['username', 'email', 'name',
                  'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password doesn't matched")
        return password2

    def save(self, commit=True):
        member = super(MemberEditForm, self).save(commit=False)
        member.set_password(self.cleaned_data['password1'])
        if commit:
            member.save()
        return member
