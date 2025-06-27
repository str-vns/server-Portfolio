from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name=_("last name")
    )
    firebase_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

class gitProject(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Project Title"))
    description = models.TextField(verbose_name=_("Project Description"))
    repository_url = models.URLField(verbose_name=_("Repository URL"))
    images = models.ImageField(
        upload_to="projects/", verbose_name=_("Project Images")
    )
    tools = models.CharField(max_length=255, verbose_name=_("Tools Used"))
    languages = models.CharField(
        max_length=255, verbose_name=_("Programming Languages")
    )
    Features = models.TextField(verbose_name=_("Project Features"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Git Project")
        verbose_name_plural = _("Git Projects")
        ordering = ["-created_at"]
