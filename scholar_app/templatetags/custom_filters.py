"""
Custom template filters for AI-Scholar
"""

from django import template

register = template.Library()


@register.filter(name='inr')
def format_inr(amount):
    """
    Format amount in Indian Rupees with proper notation
    Example: 100000 -> ₹1.00 L, 10000000 -> ₹1.00 Cr
    """
    if not amount:
        return "₹0"
    
    try:
        amount = float(amount)
        
        if amount >= 10000000:  # 1 Crore (10 Million)
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh (100 Thousand)
            return f"₹{amount/100000:.2f} L"
        elif amount >= 1000:
            # Indian number system with commas
            return f"₹{amount:,.0f}"
        else:
            return f"₹{amount:.0f}"
    except (ValueError, TypeError):
        return f"₹{amount}"


@register.filter(name='indian_number')
def indian_number_format(number):
    """
    Format numbers in Indian numbering system (lakhs and crores)
    """
    try:
        number = int(number)
        if number >= 10000000:
            return f"{number/10000000:.1f} Cr"
        elif number >= 100000:
            return f"{number/100000:.1f} L"
        else:
            return f"{number:,}"
    except (ValueError, TypeError):
        return number
