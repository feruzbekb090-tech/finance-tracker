"""Balans, hisobotlar va filtrlash."""

import database
import utils


def total_by_type(t_type):
    """Berilgan turdagi (income/expense) tranzaksiyalar yig'indisi."""
    return sum(t["amount"] for t in database.transactions if t["type"] == t_type)


def calculate_balance():
    """Balans = jami daromad - jami xarajat."""
    return total_by_type("income") - total_by_type("expense")


def get_biggest_expense():
    """Eng katta xarajat dict'i yoki None (xarajat bo'lmasa)."""
    expenses = [t for t in database.transactions if t["type"] == "expense"]
    if not expenses:
        return None
    return max(expenses, key=lambda t: t["amount"])


def filter_by_category(category):
    """Kategoriya bo'yicha (katta-kichik harfga bog'liq emas) filtrlash."""
    wanted = category.strip().lower()
    return [t for t in database.transactions if t["category"].lower() == wanted]


def expenses_above(limit):
    """Faqat chegaradan KATTA xarajatlar."""
    return [
        t
        for t in database.transactions
        if t["type"] == "expense" and t["amount"] > limit
    ]


def top_expense_category():
    """Eng ko'p pul sarflangan kategoriya (challenge). (nom, summa) yoki None."""
    totals = {}
    for t in database.transactions:
        if t["type"] == "expense":
            key = t["category"].lower()
            totals[key] = totals.get(key, 0) + t["amount"]
    if not totals:
        return None
    name = max(totals, key=totals.get)
    return name, totals[name]


# ---- Ko'rsatish funksiyalari ----


def show_balance():
    print(f"Joriy balans: {utils.format_amount(calculate_balance())}")


def show_summary():
    print("\n--- UMUMIY HISOBOT ---")
    print(f"Jami daromad : {utils.format_amount(total_by_type('income'))}")
    print(f"Jami xarajat : {utils.format_amount(total_by_type('expense'))}")
    print(f"Joriy balans : {utils.format_amount(calculate_balance())}")
    print(f"Tranzaksiyalar soni: {len(database.transactions)}")

    biggest = get_biggest_expense()
    if biggest is None:
        print("Eng katta xarajat: xarajatlar hali yo'q.")
    else:
        print(
            f"Eng katta xarajat: {utils.format_amount(biggest['amount'])} "
            f"({biggest['category']} - {biggest['description']})"
        )

    top = top_expense_category()
    if top:
        print(
            f"Eng ko'p sarflangan kategoriya: {top[0]} ({utils.format_amount(top[1])})"
        )


def show_filtered_by_category():
    category = utils.read_non_empty("Kategoriya: ")
    result = filter_by_category(category)
    if not result:
        print(f"'{category}' kategoriyasida tranzaksiya topilmadi.")
        return
    utils.print_transactions(result)


def show_expenses_above():
    limit = utils.read_positive_int("Chegara summasi (so'm): ")
    result = expenses_above(limit)
    if not result:
        print(f"{utils.format_amount(limit)} dan katta xarajatlar topilmadi.")
        return
    utils.print_transactions(result)
