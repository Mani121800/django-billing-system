from decimal import Decimal, ROUND_DOWN


def round_down_to_rupee(amount: Decimal) -> Decimal:
    # 2357.60 -> 2357.00
    return amount.quantize(Decimal('1.'), rounding=ROUND_DOWN)


def compute_change_breakup(balance: Decimal, denom_queryset):
    """
    balance: Decimal, e.g. 643
    denom_queryset: Denomination objects (already ordered desc)

    returns: list of (value, used_count), and also mutates counts
             in-memory; view will save them.
    """
    remaining = int(balance)  # assuming change is in whole rupees
    result = []

    for denom in denom_queryset:
        if remaining <= 0:
            break
        max_notes_possible = remaining // denom.value
        used = min(max_notes_possible, denom.count_available)
        if used > 0:
            result.append((denom, used))
            remaining -= used * denom.value

    # If remaining > 0 here, shop doesn’t have perfect change.
    # Assumption: we ignore that case or show a warning.
    return result, remaining
from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict=None):
    """
    Renders a Django template to PDF and returns bytes.
    Returns None if there is an error.
    """
    template = get_template(template_src)
    html = template.render(context_dict or {})

    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return None

    return result.getvalue()
