"""Ma'lumotlar ombori: tranzaksiyalar ro'yxati va keyingi ID."""

transactions = []  # barcha tranzaksiyalar (dict'lar ro'yxati)
_state = {"next_id": 1}  # keyingi ID shu yerda saqlanadi


def get_next_id():
    """Yangi ID qaytaradi va hisoblagichni oshiradi."""
    new_id = _state["next_id"]
    _state["next_id"] += 1
    return new_id
