from django.db import models
from common.models import AbstractBase


# Create your models here.

class Company(AbstractBase):
    """A model to store the company details."""
    name = models.CharField(null=True, blank=True, max_length=50)
    description = models.CharField(null=True, blank=True, max_length=100)
    establishment_date = models.DateTimeField(null=True, blank=True)
    website = models.CharField(null=True, blank=True, max_length=255)
    no_of_employees = models.IntegerField()
    phone_number = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        db_table = "company"


class CompanyAddress(AbstractBase):
    """A model to store the companies address."""
    company = models.ForeignKey(Company, related_name="company_address", on_delete=models.CASCADE)
    street = models.CharField(null=True, blank=True, max_length=30)
    city = models.CharField(null=True, blank=True, max_length=30)
    zipcode = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self) -> str:
        return self.street + self.city

    class Meta:
        verbose_name = "companyaddress"
        verbose_name_plural = "companyaddresses"
        db_table = "companyaddress"



    

