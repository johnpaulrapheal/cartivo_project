from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.text import slugify


class MyLoginAdapter(DefaultAccountAdapter):
    """
    Custom adapter for Allauth login flow.
    Handles custom logic for email-based authentication.
    """
    
    def clean_email(self, email):
        """
        Ensures email is cleaned and validated properly.
        """
        email = email.strip().lower()
        return super().clean_email(email)
    
    def save_user(self, request, sociallogin=None, form=None):
        """
        Custom user save logic for regular auth.
        """
        return super().save_user(request, sociallogin, form)


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for Allauth social account (OAuth) flow.
    Handles auto-linking and email-based authentication for social providers.
    """
    
    def _generate_unique_username(self, email="", preferred_username=""):
        """
        Build a unique username for models that still enforce unique usernames.
        """
        user_model = get_user_model()
        username_field = user_model._meta.get_field("username")
        max_len = getattr(username_field, "max_length", 150) or 150

        base_source = (preferred_username or "").strip()
        if not base_source:
            base_source = ((email or "").split("@")[0]).strip()
        if not base_source:
            base_source = "user"

        base = slugify(base_source).replace("-", "")
        if not base:
            base = "user"

        base = base[:max_len]
        candidate = base
        suffix = 0

        while user_model.objects.filter(username=candidate).exists():
            suffix += 1
            suffix_text = f"_{suffix}"
            head_len = max_len - len(suffix_text)
            candidate = f"{base[:max(1, head_len)]}{suffix_text}"

        return candidate

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user is logged in via a social provider but
        before the login is actually processed.
        
        Can be used to perform custom checks or connect existing user accounts
        based on email.
        """
        # Check if user exists with the same email
        if sociallogin.is_existing:
            return
        
        user = getattr(sociallogin, "user", None) or sociallogin.account.user
        email = (getattr(user, "email", "") or "").strip().lower()
        if not email:
            return

        user_model = get_user_model()
        try:
            existing_user = user_model.objects.get(email__iexact=email)
        except user_model.DoesNotExist:
            # No existing account with this email; allauth will create one.
            return
        except user_model.MultipleObjectsReturned:
            # Defensive fallback if legacy duplicate emails exist.
            existing_user = user_model.objects.filter(email__iexact=email).order_by("id").first()
            if not existing_user:
                return

        sociallogin.connect(request, existing_user)
    
    def save_user(self, request, sociallogin, form=None, **kwargs):
        """
        Custom user save logic for social auth.
        """
        user = getattr(sociallogin, "user", None) or sociallogin.account.user
        email = (getattr(user, "email", "") or "").strip().lower()
        user.email = email
        user.username = self._generate_unique_username(
            email=email,
            preferred_username=getattr(user, "username", "") or "",
        )

        try:
            return super().save_user(request, sociallogin, form=form, **kwargs)
        except IntegrityError as exc:
            if "username" not in str(exc).lower():
                raise
            user.username = self._generate_unique_username(email=email, preferred_username="")
            return super().save_user(request, sociallogin, form=form, **kwargs)
