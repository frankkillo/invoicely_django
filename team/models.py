from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator


class Team(models.Model):
    name = models.CharField(
        max_length=255, 
        validators=[MinLengthValidator(2, 
                "Name must be greater than 2 characters")]
    )
    org_num = models.CharField(max_length=255, blank=True, null=True)
    bankaccount = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    first_invoice_number = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='teams',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name