from decimal import Decimal
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import transaction

from .models import Product, DetectionRun, Invoice, InvoiceItem
from .forms import ProductForm, ImageUploadForm


# -----------------------------
# Auth + Landing
# -----------------------------
def landing_page(request):
    return render(request, "core/landing.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html")


# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    context = {
        "products_count": Product.objects.count(),
        "invoices_count": Invoice.objects.filter(user=request.user).count(),
        "detections_count": DetectionRun.objects.filter(user=request.user).count(),
    }
    return render(request, "core/dashboard.html", context)


# -----------------------------
# Product CRUD
# -----------------------------
@login_required
def product_list(request):
    products = Product.objects.all().order_by("name")
    return render(request, "core/product_list.html", {"products": products})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "core/product_form.html", {"form": form, "action": "Create"})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request, "core/product_form.html", {"form": form, "product": product, "action": "Edit"}
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")
    return render(request, "core/product_delete.html", {"product": product})


# -----------------------------
# MVP Detection Rules (Filename based)
# -----------------------------
# این‌ها تعدادها و مسیر bbox رو مشخص می‌کنن (همون فایل‌هایی که جدا کردی)
FILENAME_RULES = [
    # IMPORTANT: shelf2_alt باید قبل shelf2 بررسی بشه
    {
        "key": "shelf2_alt",
        "counts": {"chips": 3},
        "bbox": "bboxes/shelf2_alt_bbox.jpg",
    },
    {
        "key": "shelf1",
        "counts": {"coke": 14, "pepsi": 5},
        "bbox": "bboxes/shelf1_bbox.jpg",
    },
    {
        "key": "shelf2",
        "counts": {"chips": 5, "coke": 1},
        "bbox": "bboxes/shelf2_bbox.jpg",
    },
    {
        "key": "shelf3",
        "counts": {"water": 13, "chips": 3, "coke": 3},
        "bbox": "bboxes/shelf3_bbox.jpg",
    },
]

DEFAULT_COUNTS = {"unknown": 0}
DEFAULT_BBOX = "bboxes/unknown_bbox.jpg"


def detect_items_from_filename(filename: str):
    """
    Fake detection logic based on filename.
    Returns: (counts_dict, bbox_rel_path)
    bbox_rel_path is relative to static/ (so template uses {% static detection.bbox_image_path %})
    """
    f = (filename or "").lower()

    for rule in FILENAME_RULES:
        if rule["key"] in f:
            return rule["counts"], rule["bbox"]

    return DEFAULT_COUNTS, DEFAULT_BBOX


# -----------------------------
# Detection class -> Product SKU mapping
# (تو MVP بهتره SKUها دقیق باشند)
# -----------------------------
DETECTION_TO_SKU_MAPPING = {
    "coke": "COKE-001",
    "pepsi": "PEPSI-001",
    "chips": "CHIPS-001",
    "water": "WATER-001",
    # "unknown": None
}


# -----------------------------
# Upload + Detect
# -----------------------------
@login_required
def upload_detect(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            detection_run = form.save(commit=False)
            detection_run.user = request.user

            filename = detection_run.uploaded_image.name  # مثل shelf1.jpg
            counts, bbox_path = detect_items_from_filename(filename)

            # اگر مدل DetectionRun.result_json از نوع JSONField است می‌تونی dict ذخیره کنی
            # اگر TextField است هم می‌تونی dict ذخیره کنی و در get_detected_items آن را parse کنی
            detection_run.result_json = counts
            detection_run.bbox_image_path = bbox_path
            detection_run.save()

            return redirect("detect_result", pk=detection_run.pk)
    else:
        form = ImageUploadForm()

    return render(request, "core/upload_detect.html", {"form": form})


# -----------------------------
# Show detection result
# -----------------------------
@login_required
def detect_result(request, pk):
    detection = get_object_or_404(DetectionRun, pk=pk, user=request.user)
    detected_items = detection.get_detected_items()  # dict

    detected_items_list = []
    warnings = []

    for class_name, qty in detected_items.items():
        item_info = {
            "class_name": class_name,
            "qty": qty,
            "sku": None,
            "product": None,
            "available_stock": 0,
        }

        if class_name.lower() == "unknown":
            warnings.append(f"Unknown item detected (qty={qty}).")
            detected_items_list.append(item_info)
            continue

        sku = DETECTION_TO_SKU_MAPPING.get(class_name.lower())
        item_info["sku"] = sku

        if not sku:
            warnings.append(f"No SKU mapping found for detected class: {class_name}")
            detected_items_list.append(item_info)
            continue

        try:
            product = Product.objects.get(sku=sku)
            item_info["product"] = product
            item_info["available_stock"] = product.stock
        except Product.DoesNotExist:
            warnings.append(f"Product not found for class: {class_name} (expected SKU: {sku})")

        detected_items_list.append(item_info)

    context = {
        "detection": detection,
        "detected_items": detected_items,
        "detected_items_list": detected_items_list,
        "warnings": warnings,
    }
    return render(request, "core/detect_result.html", context)


# -----------------------------
# Generate invoice from detection
# -----------------------------
@login_required
@transaction.atomic
def generate_invoice(request, detection_pk):
    detection = get_object_or_404(DetectionRun, pk=detection_pk, user=request.user)
    detected_items = detection.get_detected_items()

    invoice_items_data = []
    total_amount = Decimal("0.00")
    errors = []

    # 1) validate + compute
    for class_name, qty in detected_items.items():
        if class_name.lower() == "unknown":
            continue
        if qty is None or qty <= 0:
            continue

        sku = DETECTION_TO_SKU_MAPPING.get(class_name.lower())
        if not sku:
            continue

        try:
            product = Product.objects.select_for_update().get(sku=sku)

            if product.stock < qty:
                errors.append(
                    f"Insufficient stock for {product.name}. Available={product.stock}, Required={qty}"
                )
                continue

            subtotal = (product.unit_price or Decimal("0.00")) * Decimal(qty)
            total_amount += subtotal

            invoice_items_data.append(
                {
                    "product": product,
                    "qty": qty,
                    "unit_price": product.unit_price,
                    "subtotal": subtotal,
                }
            )
        except Product.DoesNotExist:
            errors.append(f"Product not found for SKU: {sku}")

    if errors:
        messages.error(request, "Cannot generate invoice: " + " ; ".join(errors))
        return redirect("detect_result", pk=detection_pk)

    if not invoice_items_data:
        messages.error(request, "No valid items to invoice.")
        return redirect("detect_result", pk=detection_pk)

    # 2) create invoice
    invoice = Invoice.objects.create(
        user=request.user,
        total_amount=total_amount,
        related_detection=detection,
    )

    # 3) create items + deduct stock
    for item in invoice_items_data:
        InvoiceItem.objects.create(
            invoice=invoice,
            product=item["product"],
            qty=item["qty"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"],
        )

        item["product"].stock -= item["qty"]
        item["product"].save()

    messages.success(request, f"Invoice {invoice.invoice_no} generated successfully!")
    return redirect("invoice_detail", pk=invoice.pk)


# -----------------------------
# Invoice pages
# -----------------------------
@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "core/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    return render(request, "core/invoice_detail.html", {"invoice": invoice})


# -----------------------------
# Analytics
# -----------------------------
@login_required
def analytics(request):
    products = Product.objects.all()

    products_with_scores = []
    for product in products:
        score = product.investment_score()
        products_with_scores.append({"product": product, "score": round(score, 2)})

    products_with_scores.sort(key=lambda x: x["score"], reverse=True)

    chart_data_json = json.dumps(
        {
            "labels": [p["product"].name for p in products_with_scores],
            "scores": [p["score"] for p in products_with_scores],
        }
    )

    context = {
        "products_with_scores": products_with_scores,
        "chart_data_json": chart_data_json,
    }
    return render(request, "core/analytics.html", context)
