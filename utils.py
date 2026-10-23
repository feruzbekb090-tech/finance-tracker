"""Input tekshirish va formatlash yordamchilari."""

TYPE_LABELS = {"income": "DAROMAD", "expense": "XARAJAT"}


def read_positive_int(prompt):
    """Musbat butun son kiritilguncha so'raydi."""
    while True:
        raw = input(prompt).strip().replace(" ", "")
        if not raw.isdigit():
            print("Xato: faqat butun son kiriting (masalan, 45000).")
            continue
        value = int(raw)
        if value <= 0:
            print("Xato: summa 0 dan katta bo'lishi kerak.")
            continue
        return value


def read_non_empty(prompt):
    """Bo'sh bo'lmagan matn kiritilguncha so'raydi."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Xato: bo'sh qoldirib bo'lmaydi.")


def read_int(prompt):
    """Ixtiyoriy butun son (ID uchun). Noto'g'ri bo'lsa None qaytaradi."""
    raw = input(prompt).strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    print("Xato: butun son kiriting.")
    return None


def format_amount(amount):
    """45000 -> '45 000 so'm'."""
    return f"{amount:,}".replace(",", " ") + " so'm"


def print_transactions(items):
    """Tranzaksiyalar ro'yxatini jadval ko'rinishida chiqaradi."""
    if not items:
        print("Tranzaksiyalar topilmadi.")
        return
    print(f"{'ID':<4} {'TURI':<9} {'SUMMA':>16}  {'KATEGORIYA':<14} IZOH")
    print("-" * 64)
    for t in items:
        label = TYPE_LABELS[t["type"]]
        sign = "+" if t["type"] == "income" else "-"
        amount = sign + format_amount(t["amount"])
        print(
            f"{t['id']:<4} {label:<9} {amount:>16}  {t['category']:<14} {t['description']}"
        )
