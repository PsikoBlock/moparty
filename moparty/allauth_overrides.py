from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
import allauth.account.forms as allauthforms
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        raise ValidationError("Can not disconnect") 


class MemberChangePasswordForm(allauthforms.ChangePasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot change password.'))


class MemberSetPasswordForm(allauthforms.SetPasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot set password.'))


class MemberResetPasswordForm(allauthforms.ResetPasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot reset password.'))


class MemberAddEmailForm(allauthforms.AddEmailForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot add an email.'))
