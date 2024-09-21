from decimal import Decimal


def normalize_or_quantize(d: Decimal) -> Decimal:
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
