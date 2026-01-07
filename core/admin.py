from django.contrib import admin
from .models import Product, DetectionRun, Invoice, InvoiceItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'unit_price', 'stock', 'weekly_sales_estimate', 'profit_margin']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'sku']


@admin.register(DetectionRun)
class DetectionRunAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'user', 'created_at', 'total_amount']
    list_filter = ['created_at']
    readonly_fields = ['invoice_no', 'created_at']
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'product', 'qty', 'unit_price', 'subtotal']
    list_filter = ['invoice__created_at']

