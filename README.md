# Django Billing System

A production-ready **Billing System** built using **Django**, featuring dynamic billing, tax calculation, denomination-based change calculation, PDF invoice generation, and **asynchronous email delivery with PDF attachment**.

This project was developed as a mini-task to demonstrate strong **Model–View architecture**, background processing, and real-world billing logic.

---

## ✅ Key Features

* ✅ Product management with tax support
* ✅ Dynamic billing form (Add multiple products)
* ✅ Stock validation & real-time updates
* ✅ Automatic tax calculation
* ✅ Rounded net price calculation
* ✅ Denomination-based balance breakdown
* ✅ Invoice generation (HTML + PDF)
* ✅ **Asynchronous email delivery with PDF attachment**
* ✅ View previous purchases by customer email
* ✅ Detailed purchase history per bill
* ✅ Django Admin for easy data management

---

## 🧰 Tech Stack

* **Backend:** Django 5+
* **Database:** SQLite (default)
* **PDF Generation:** xhtml2pdf
* **Email:** SMTP (Gmail with App Password)
* **Frontend:** HTML, CSS (Basic level as required)

---

## 📁 Project Structure

```
django-billing-system/
│
├── billing/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── utils.py
│   ├── pdf_utils.py
│   └── templates/
│       └── billing/
│           ├── billing_form.html
│           ├── billing_summary.html
│           ├── previous_purchases.html
│           ├── purchase_detail.html
│           └── invoice_pdf.html
│
├── billing_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions (Run Locally)

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-billing-system.git
cd django-billing-system
```

---

### ✅ 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### ✅ 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### ✅ 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### ✅ 5. Create Superuser

```bash
python manage.py createsuperuser
```

---

### ✅ 6. Configure Email (Gmail SMTP Required)

In `settings.py`:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "yourgmail@gmail.com"
EMAIL_HOST_PASSWORD = "your_google_app_password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> ⚠️ You **must use a Gmail App Password**, not your actual Gmail password.

---

### ✅ 7. Run the Server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/billing/
```

---

## 🔐 Django Admin Setup

Open:

```
http://127.0.0.1:8000/admin/
```

Login using superuser and add:

### ✅ Products

| Name   | Product ID | Stock | Unit Price | Tax % |
| ------ | ---------- | ----- | ---------- | ----- |
| Laptop | P001       | 10    | 50000      | 18    |
| Mouse  | P002       | 50    | 500        | 5     |

### ✅ Denominations

| Value | Count |
| ----- | ----- |
| 500   | 10    |
| 200   | 10    |
| 100   | 10    |
| 50    | 10    |
| 20    | 10    |

---

## 🧾 How the Billing System Works

1. Enter customer email
2. Add products dynamically
3. Enter shop denomination availability
4. Enter cash paid by customer
5. Click **Generate Bill**
6. System will:

   * Calculate tax & totals
   * Generate invoice
   * Send **PDF invoice via email (async)**
   * Show full summary on screen

---

## 📩 Email & PDF Invoice

* Invoice is generated as a PDF using **xhtml2pdf**
* PDF is automatically attached to the bill email
* Email is sent asynchronously using `threading`

---

## 📜 View Previous Purchases

Open:

```
http://127.0.0.1:8000/billing/purchases/
```

* Enter customer email
* View all previous purchases
* Click on any bill to view full details

---

## ✅ Best Practices Followed

* Clean Model–View separation
* Asynchronous background email sending
* Atomic database transactions
* Proper stock consistency
* Production safety via `.gitignore`
* Requirements managed in `requirements.txt`

---

## 📌 Assumptions

* All cash & balances are handled in **whole Rupees**
* Net price is **rounded down** before balance calculation
* If full change is not possible, remaining amount is shown

---

## ⭐ Future Enhancements (Optional)

* PDF download button in UI
* Authentication system
* REST API support
* Bootstrap-based UI
* Stock low alerts

---

## 👤 Developer

**Manikandan**
Full Stack Python / Django Developer

---

✅ This project is fully functional and ready for evaluation.
