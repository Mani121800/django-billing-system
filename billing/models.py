from decimal import Decimal
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product_id} - {self.name}"


class Denomination(models.Model):
    """
    Denomination notes/coins available in the shop.
    Example values: 500, 100, 50, 20, 10, 5, 2, 1
    """
    value = models.PositiveIntegerField(unique=True)
    count_available = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-value']  # always highest first

    def __str__(self):
        return str(self.value)


class Bill(models.Model):
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    total_without_tax = models.DecimalField(max_digits=12, decimal_places=2)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2)
    net_price = models.DecimalField(max_digits=12, decimal_places=2)
    rounded_net_price = models.DecimalField(max_digits=12, decimal_places=2)

    cash_paid = models.DecimalField(max_digits=12, decimal_places=2)
    balance_to_customer = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Bill #{self.id} - {self.customer_email}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_for_item = models.DecimalField(max_digits=12, decimal_places=2)
    total_price_for_item = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_id} x {self.quantity}"


class BillChangeDenomination(models.Model):
    """
    How the balance was returned to the customer for a bill.
    """
    bill = models.ForeignKey(Bill, related_name='change_denominations',
                             on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    count = models.PositiveIntegerField()

    class Meta:
        ordering = ['-value']

    def __str__(self):
        return f"{self.value} x {self.count}"
