# Inventory MVP - Django Web Application

A modern, dark-themed inventory management web application with fake object detection capabilities. This MVP demonstrates a complete product/inventory system with detection, invoicing, and analytics features.

## Features

- **Landing Page**: Beautiful dark-themed landing page with feature highlights
- **User Authentication**: Django built-in authentication system
- **Product Management**: Full CRUD operations for products
- **Fake Detection System**: Filename-based detection (no real ML)
- **Invoice Generation**: Automatic invoice creation from detection results
- **Analytics Dashboard**: Investment score charts and rankings
- **Dark Theme UI**: Modern, premium dark interface using Bootstrap 5

## Project Structure

```
inventory_mvp/
├── manage.py
├── requirements.txt
├── README.md
├── inventory_mvp/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── templates/
│   ├── base.html
│   └── core/
│       ├── landing.html
│       ├── login.html
│       ├── dashboard.html
│       ├── product_list.html
│       ├── product_form.html
│       ├── product_delete.html
│       ├── upload_detect.html
│       ├── detect_result.html
│       ├── invoice_list.html
│       ├── invoice_detail.html
│       └── analytics.html
└── static/
    ├── css/
    │   └── dark-theme.css
    └── bboxes/
        └── (placeholder images)
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "C:\Users\Farasoo\Desktop\پروژه"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Setup

1. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

### 4. Static Files Setup

1. **Create static bbox images directory:**
   The directory `static/bboxes/` should already exist. You need to place placeholder images there:
   - `shelf1_bbox.jpg` - Bounding box result for shelf1 images
   - `shelf2_bbox.jpg` - Bounding box result for shelf2 images
   - `shelf3_bbox.jpg` - Bounding box result for shelf3/mixed images
   - `unknown.jpg` - Default bounding box result for unknown images

   **Note:** These can be any placeholder images (even simple colored rectangles) for MVP purposes. The app will use them when displaying detection results.

2. **Collect static files (for production):**
   ```bash
   python manage.py collectstatic
   ```

### 5. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage Guide

### 1. Initial Setup

1. **Login:** Navigate to the landing page and click "User Panel" to login (use the superuser credentials you created)

2. **Create Products:** 
   - Go to Products → Add Product
   - Create products with SKUs matching the detection mapping:
     - `COKE-001` for coke detection
     - `PEPSI-001` for pepsi detection
     - `CHIPS-001` for chips detection
     - `WATER-001` for water detection
   - Set initial stock, unit prices, weekly sales estimates, and profit margins

### 2. Detection System (MVP - Filename Based)

The detection system uses filename-based logic (no real ML):

- **shelf1** in filename → Detects: coke (3), pepsi (2)
- **shelf2** in filename → Detects: chips (5), coke (1)
- **shelf3** or **mixed** in filename → Detects: water (4), chips (2), coke (1)
- **Other filenames** → Detects: unknown (0)

**To test:**
1. Go to Upload/Detect
2. Upload an image with a filename containing "shelf1", "shelf2", "shelf3", or "mixed"
3. View detection results
4. Generate invoice if products are found and stock is sufficient

### 3. Invoice Generation

1. After detection, click "Generate Invoice"
2. The system will:
   - Match detected items to products by SKU
   - Validate stock availability
   - Create invoice and deduct stock
   - Show invoice details with remaining stock

### 4. Analytics

- View investment scores calculated using the heuristic formula
- See bar chart visualization of scores
- Review product rankings by investment score

## Detection Mapping

The system maps detected class names to product SKUs:

```python
DETECTION_TO_SKU_MAPPING = {
    'coke': 'COKE-001',
    'pepsi': 'PEPSI-001',
    'chips': 'CHIPS-001',
    'water': 'WATER-001',
}
```

Make sure to create products with these exact SKUs for detection to work properly.

## Investment Score Formula

The analytics page uses this MVP heuristic:

```
Investment Score = (Weekly Sales Estimate × Profit Margin) / max(1, Current Stock)
```

This is a simplified formula for MVP demonstration purposes, not real AI/ML analysis.

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials to:
- Manage products
- View detection runs
- View invoices
- Manage users

## Important Notes

1. **No Real ML:** This is an MVP with filename-based detection. No actual object detection is performed.

2. **Static Images:** Place placeholder bbox images in `static/bboxes/` directory. These are displayed as detection results.

3. **Stock Validation:** The system prevents negative stock. If detected quantity exceeds available stock, invoice generation will fail with an error.

4. **Media Files:** Uploaded images are stored in `media/uploads/` directory (created automatically).

## Troubleshooting

1. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATICFILES_DIRS` in settings.py

2. **Images not displaying:**
   - Ensure bbox images exist in `static/bboxes/`
   - Check file permissions

3. **Detection not working:**
   - Verify product SKUs match the detection mapping (COKE-001, PEPSI-001, etc.)
   - Check that uploaded image filename contains "shelf1", "shelf2", etc.

## Development

- **Database:** SQLite (default, for MVP)
- **Frontend:** Bootstrap 5 + Custom Dark Theme CSS
- **Charts:** Chart.js
- **Icons:** Bootstrap Icons

## License

This is an MVP project for demonstration purposes.

