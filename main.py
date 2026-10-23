"""Personal Finance Tracker - menu va dastur oqimi."""

import transactions
import reports

MENU = """
===== PERSONAL FINANCE TRACKER =====
1. Daromad qo'shish
2. Xarajat qo'shish
3. Barcha tranzaksiyalarni ko'rish
4. Tranzaksiyani o'chirish
5. Joriy balansni ko'rish
6. Umumiy hisobot
7. Kategoriya bo'yicha filtrlash
8. Ma'lum summadan yuqori xarajatlarni ko'rish
0. Chiqish"""

ACTIONS = {
    "1": transactions.add_income,
    "2": transactions.add_expense,
    "3": transactions.show_all,
    "4": transactions.delete_transaction,
    "5": reports.show_balance,
    "6": reports.show_summary,
    "7": reports.show_filtered_by_category,
    "8": reports.show_expenses_above,
}


def main():
    while True:
        print(MENU)
        choice = input("Tanlang: ").strip()
        if choice == "0":
            print("Xayr!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Xato: menyudagi raqamlardan birini tanlang.")
            continue
        action()


main()
