from decimal import Decimal
import threading

from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Product, Denomination, Bill, BillItem, BillChangeDenomination
from .pdf_utils import round_down_to_rupee, compute_change_breakup
from .pdf_utils import render_to_pdf

def send_invoice_email_async(bill):
    def _send():
        # Plain-text body
        message_lines = [
            f"Dear Customer ({bill.customer_email}),",
            "",
            f"Total without tax: {bill.total_without_tax}",
            f"Total tax: {bill.total_tax}",
            f"Rounded net price: {bill.rounded_net_price}",
            f"Cash paid: {bill.cash_paid}",
            f"Balance to you: {bill.balance_to_customer}",
            "",
            "Please find your invoice attached as a PDF.",
            "",
            "Thank you for your purchase.",
        ]
        body = "\n".join(message_lines)

        subject = f"Invoice for Bill #{bill.id}"

        # Render PDF
        pdf_bytes = render_to_pdf(
            "billing/invoice_pdf.html",
            {
                "bill": bill,
                "items": bill.items.all(),
                "change_denoms": bill.change_denominations.all(),
            },
        )

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[bill.customer_email],
        )

        # Attach PDF if generation succeeded
        if pdf_bytes:
            filename = f"invoice_bill_{bill.id}.pdf"
            email.attach(filename, pdf_bytes, "application/pdf")

        # Optional: debug print to console
        print(f"Sending invoice email with PDF to {bill.customer_email}")
        email.send(fail_silently=False)

    threading.Thread(target=_send, daemon=True).start()

@transaction.atomic
def billing_page(request):
    if request.method == "GET":
        denominations = Denomination.objects.all()
        return render(request, "billing/billing_form.html", {
            "denominations": denominations,
        })

    # POST
    customer_email = request.POST.get("customer_email", "").strip()
    if not customer_email:
        return HttpResponseBadRequest("Customer email is required")

    product_ids = request.POST.getlist("product_id")
    quantities = request.POST.getlist("quantity")

    if not product_ids:
        return HttpResponseBadRequest("At least one product is required")

    # Collect denomination counts in shop for this bill
    denom_values = {}
    for denom in Denomination.objects.all():
        field_name = f"denom_{denom.value}"
        count_str = request.POST.get(field_name, "0") or "0"
        denom.count_available = int(count_str)
        denom_values[denom.value] = denom.count_available

    cash_paid = Decimal(request.POST.get("cash_paid", "0") or "0")

    # Compute line items
    total_without_tax = Decimal("0.00")
    total_tax = Decimal("0.00")

    items_data = []

    for pid, qty_str in zip(product_ids, quantities):
        if not pid or not qty_str:
            continue
        product = get_object_or_404(Product, product_id=pid)
        qty = int(qty_str)

        if qty <= 0:
            continue

        if qty > product.available_stocks:
            # Assumption: we just fail the request; can be improved
            return HttpResponseBadRequest(
                f"Not enough stock for product {product.product_id}"
            )

        unit_price = product.unit_price
        purchase_price = unit_price * qty
        tax_for_item = purchase_price * product.tax_percentage / Decimal("100")
        total_price_for_item = purchase_price + tax_for_item

        total_without_tax += purchase_price
        total_tax += tax_for_item

        items_data.append({
            "product": product,
            "quantity": qty,
            "unit_price": unit_price,
            "purchase_price": purchase_price,
            "tax_for_item": tax_for_item,
            "total_price_for_item": total_price_for_item,
        })

    if not items_data:
        return HttpResponseBadRequest("No valid items")

    net_price = total_without_tax + total_tax
    rounded_net_price = round_down_to_rupee(net_price)

    balance_to_customer = cash_paid - rounded_net_price
    if balance_to_customer < 0:
        return HttpResponseBadRequest("Cash paid is less than bill amount")

    # Compute change breakup using denominations
    denom_qs = Denomination.objects.all()
    change_result, remaining = compute_change_breakup(
        Decimal(balance_to_customer),
        denom_qs
    )

    # Save Bill + BillItems + Change denominations
    bill = Bill.objects.create(
        customer_email=customer_email,
        total_without_tax=total_without_tax,
        total_tax=total_tax,
        net_price=net_price,
        rounded_net_price=rounded_net_price,
        cash_paid=cash_paid,
        balance_to_customer=balance_to_customer,
    )

    for item in items_data:
        BillItem.objects.create(
            bill=bill,
            product=item["product"],
            unit_price=item["unit_price"],
            quantity=item["quantity"],
            purchase_price=item["purchase_price"],
            tax_for_item=item["tax_for_item"],
            total_price_for_item=item["total_price_for_item"],
        )
        # Reduce stock
        item["product"].available_stocks -= item["quantity"]
        item["product"].save()

    for denom_obj, used_count in change_result:
        BillChangeDenomination.objects.create(
            bill=bill,
            value=denom_obj.value,
            count=used_count,
        )
    # Send email with PDF invoice in background
    send_invoice_email_async(bill)

    # Render Page 2 (summary)
    return render(request, "billing/billing_summary.html", {
        "bill": bill,
        "items": bill.items.all(),
        "change_denoms": bill.change_denominations.all(),
        "remaining_change": remaining,
    })
from django.core.paginator import Paginator


def previous_purchases(request):
    email = request.GET.get("email", "").strip()
    bills = Bill.objects.none()

    if email:
        bills = Bill.objects.filter(customer_email=email).order_by('-created_at')

    paginator = Paginator(bills, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "billing/previous_purchases.html", {
        "email": email,
        "page_obj": page_obj,
    })


def purchase_detail(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    return render(request, "billing/purchase_detail.html", {
        "bill": bill,
        "items": bill.items.all(),
        "change_denoms": bill.change_denominations.all(),
    })
