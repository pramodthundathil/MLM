from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='last name')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        verbose_name='phone number'
    )
    date_of_birth = models.DateField(auto_now_add=False)
    age = models.BigIntegerField()
    village = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    cast = models.CharField(max_length=20)
    religion = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True, verbose_name='address')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    role = models.CharField(max_length=20, 
                            choices=(
                                ("admin","admin"),
                                ("user","user"),
                                ("semi-admin","semi-admin"),
                                ("finance","finance"),
                                ("marketing","markenting"),
                                ("district_franchise","district_franchise"),
                                ("zonel_franchise","zonel_franchise"),
                                ("mobile_franchise","mobile_franchise"),
                                ("state_franchise","state_franchise"),
                            ),
                            default='user'
                            )
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='parent')
    pancard = models.CharField(max_length=20, unique=True, verbose_name='PAN card')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "pancard", "ifsc_code", "phone_number"]

    bv_active_status = models.BooleanField(default=False)
    designation = models.CharField(
        max_length=20,
        choices=(
            ("Executive","Executive"),
            ("Cheif Executive","Cheif Executive"),
            ("Manager","Manager"),
            ("General Manager","General Manager"),
            ("Director","Director"),
        ),
        default="Executive"
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        if not self.id_number:
            self.id_number = self.generate_unique_order_number()
        super(CustomUser, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        # Generate a unique order number using UUID
        return str(uuid.uuid4().hex[:5]).upper()
        
    def __str__(self):
        return self.email

class Business_Volume(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bv_amount = models.FloatField(default=0)
    balance_bv = models.FloatField(default=0)
    total_bv = models.FloatField(default=0)
    purchase_bv = models.FloatField(default=0)
    active_status = models.BooleanField(default=False)

class AccountDetails(models.Model):
    user  = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ifsc_code = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^[A-Za-z]{4}\d{7}$', message="IFSC code must be in the format: 'ABCD0123456'.")], verbose_name='IFSC code')
    branch_name = models.CharField(max_length=20)
    account_number = models.CharField(max_length=255)

class Nominee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nominee_name = models.CharField(max_length=20)
    id_proof = models.FileField(upload_to="nominee_id", null=True, blank=True)
    nominee_is_active = models.BooleanField(default=False)

class UserOTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.otp}" 





