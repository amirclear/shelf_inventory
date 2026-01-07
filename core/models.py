from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    weekly_sales_estimate = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.20'), validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def investment_score(self):
        """Calculate investment score heuristic"""
        if self.stock <= 0:
            return 0
        numerator = self.weekly_sales_estimate * float(self.profit_margin)
        denominator = max(1, self.stock)
        return numerator / denominator


class DetectionRun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    result_json = models.JSONField(default=dict)  # Store detected items: {"coke": 3, "pepsi": 2}
    bbox_image_path = models.CharField(max_length=500, default='')  # Path to static bbox image

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Detection {self.id} by {self.user.username} at {self.created_at}"

    def get_detected_items(self):
        """Return detected items as dict"""
        return self.result_json if isinstance(self.result_json, dict) else {}


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_no = models.CharField(max_length=50, unique=True, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    related_detection = models.ForeignKey(DetectionRun, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_no}"

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f"{self.product.name} x{self.qty} in {self.invoice.invoice_no}"

