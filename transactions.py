"""Tranzaksiya qo'shish, ko'rish va o'chirish."""

import database
import utils

VALID_TYPES = ("income", "expense")


def add_transaction(t_type, amount, category, description):
    """Tranzaksiyani tekshirib, bazaga qo'shadi. Qo'shilgan dict'ni qaytaradi."""
    if t_type not in VALID_TYPES:
        raise ValueError("Noto'g'ri tranzaksiya turi.")
    if not isinstance(amount, int) or amount <= 0:
        raise ValueError("Summa musbat butun son bo'lishi kerak.")
    if not category.strip():
        raise ValueError("Kategoriya bo'sh bo'lmasligi kerak.")

    transaction = {
        "id": database.get_next_id(),
        "type": t_type,
        "amount": amount,
        "category": category.strip(),
        "description": description.strip(),
    }
    database.transactions.append(transaction)
    return transaction


def _ask_and_add(t_type):
    """Daromad va xarajat uchun umumiy input oqimi."""
    amount = utils.read_positive_int("Summa (so'm): ")
    category = utils.read_non_empty("Kategoriya: ")
    description = utils.read_non_empty("Izoh: ")
    t = add_transaction(t_type, amount, category, description)
    print(f"Saqlandi! (ID: {t['id']})")


def add_income():
    _ask_and_add("income")


def add_expense():
    _ask_and_add("expense")


def show_all():
    utils.print_transactions(database.transactions)


def find_by_id(transaction_id):
    """ID bo'yicha tranzaksiyani topadi, topilmasa None."""
    for t in database.transactions:
        if t["id"] == transaction_id:
            return t
    return None


def delete_transaction():
    if not database.transactions:
        print("Tranzaksiyalar yo'q, o'chirish uchun hech narsa yo'q.")
        return
    transaction_id = utils.read_int("O'chiriladigan tranzaksiya ID si: ")
    if transaction_id is None:
        return
    t = find_by_id(transaction_id)
    if t is None:
        print(f"ID={transaction_id} bo'lgan tranzaksiya topilmadi.")
        return
    database.transactions.remove(t)
    print(f"ID={transaction_id} tranzaksiya o'chirildi.")
