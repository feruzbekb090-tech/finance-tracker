# Personal Finance Tracker

Terminalda ishlaydigan shaxsiy moliya hisoblagichi. Dastur daromad va xarajatlarni qayd etadi, balansni hisoblaydi va oddiy hisobotlar chiqaradi.

Loyiha faqat Python standart imkoniyatlaridan foydalanadi: `list`, `dict`, funksiyalar, modullar, sikllar, shartlar, filtrlash va aggregatsiya. `class`, tashqi kutubxonalar va haqiqiy ma'lumotlar bazasi ishlatilmagan.

---

## Mundarija

1. [Imkoniyatlar](#1-imkoniyatlar)
2. [Talablar](#2-talablar)
3. [Ishga tushirish](#3-ishga-tushirish)
4. [Fayllar tuzilmasi](#4-fayllar-tuzilmasi)
5. [Ma'lumotlar modeli](#5-malumotlar-modeli)
6. [Menyu](#6-menyu)
7. [Balans qanday hisoblanadi](#7-balans-qanday-hisoblanadi)
8. [Hisobotlar qaysi funksiyalarga tayanadi](#8-hisobotlar-qaysi-funksiyalarga-tayanadi)
9. [Funksiyalar ro'yxati](#9-funksiyalar-royxati)
10. [Xatoliklarni qayta ishlash](#10-xatoliklarni-qayta-ishlash)
11. [Demo](#11-demo)
12. [Sinov rejasi](#12-sinov-rejasi)
13. [Qabul qilish mezonlari](#13-qabul-qilish-mezonlari)
14. [Qo'shimcha challenge](#14-qoshimcha-challenge)
15. [Cheklovlar va kelajak rejalari](#15-cheklovlar-va-kelajak-rejalari)

---

## 1. Imkoniyatlar

- Daromad va xarajat qo'shish (ID avtomatik beriladi).
- Barcha tranzaksiyalarni jadval ko'rinishida ko'rish.
- Tranzaksiyani ID orqali o'chirish.
- Joriy balansni ko'rish.
- Umumiy hisobot: jami daromad, jami xarajat, balans, tranzaksiyalar soni, eng katta xarajat.
- Kategoriya bo'yicha filtrlash (katta-kichik harfga bog'liq emas).
- Ma'lum summadan yuqori xarajatlarni ko'rish.
- Noto'g'ri inputdan himoya: dastur foydalanuvchi xatosi sababli to'xtab qolmaydi.

## 2. Talablar

- Python 3.8 yoki yangiroq.
- Qo'shimcha kutubxona o'rnatish shart emas.

Python versiyasini tekshirish:

```bash
python --version
```

## 3. Ishga tushirish

1. Loyiha papkasiga o'ting:

    ```bash
    cd moliya_hisobchisi
    ```

2. Dasturni `main.py` orqali ishga tushiring:

    ```bash
    python main.py
    ```

    (Ba'zi tizimlarda `python3 main.py`.)

3. Menyudan kerakli raqamni kiriting. Chiqish uchun `0` ni tanlang.

> Ma'lumotlar faqat dastur ishlab turganda xotirada saqlanadi. Dastur yopilsa, tranzaksiyalar yo'qoladi (topshiriq shartiga ko'ra faylga saqlash hozircha shart emas).

## 4. Fayllar tuzilmasi

```text
moliya_hisobchisi/
├── main.py
├── transactions.py
├── reports.py
├── utils.py
├── database.py
└── README.md
```

| Fayl              | Vazifasi                                               |
| ----------------- | ------------------------------------------------------ |
| `main.py`         | Menyu va dastur oqimini boshqaradi.                    |
| `transactions.py` | Daromad/xarajat qo'shish, ko'rish va o'chirish.        |
| `reports.py`      | Balans, jami daromad/xarajat, filtrlash va hisobotlar. |
| `utils.py`        | Input tekshirish va formatlash yordamchilari.          |
| `database.py`     | Tranzaksiyalar ro'yxati va keyingi ID.                 |

### Modullar orasidagi bog'liqlik

```text
main.py ──► transactions.py ──► utils.py
   │              │
   │              └──────────► database.py
   └──────────► reports.py ──► utils.py
                    │
                    └────────► database.py
```

`database.py` hech qaysi modulga bog'liq emas, u eng quyi qatlam. `utils.py` ham mustaqil. `main.py` esa faqat menyuni boshqaradi va ishni boshqa modullarga topshiradi.

## 5. Ma'lumotlar modeli

Har bir tranzaksiya `dict` ko'rinishida saqlanadi:

```python
{
    "id": 1,
    "type": "expense",
    "amount": 45000,
    "category": "food",
    "description": "Tushlik"
}
```

| Kalit         | Turi  | Izoh                                                                                |
| ------------- | ----- | ----------------------------------------------------------------------------------- |
| `id`          | `int` | Avtomatik beriladi, 1 dan boshlab oshib boradi. O'chirilgan ID qayta ishlatilmaydi. |
| `type`        | `str` | Faqat `"income"` (daromad) yoki `"expense"` (xarajat).                              |
| `amount`      | `int` | Musbat butun son, so'mda.                                                           |
| `category`    | `str` | Bo'sh bo'lmagan matn.                                                               |
| `description` | `str` | Izoh.                                                                               |

**Nega summa `int`?** Float sonlarda aniqlik muammosi bor (masalan, `0.1 + 0.2` natijasi `0.30000000000000004` chiqadi). Pul hisobida bunday xato bo'lmasligi uchun summalar butun so'mda saqlanadi.

Barcha tranzaksiyalar `database.tranzaksiyalar` ro'yxatida turadi. Keyingi ID `database.keyingi_id_olish()` funksiyasi orqali beriladi.

## 6. Menyu

```text
===== PERSONAL FINANCE TRACKER =====
1. Daromad qo'shish
2. Xarajat qo'shish
3. Barcha tranzaksiyalarni ko'rish
4. Tranzaksiyani o'chirish
5. Joriy balansni ko'rish
6. Umumiy hisobot
7. Kategoriya bo'yicha filtrlash
8. Ma'lum summadan yuqori xarajatlarni ko'rish
0. Chiqish
```

Menyu `0` tanlanguncha takrorlanadi. Menyu tanlovlari `main.py` dagi `HARAKATLAR` lug'atida saqlanadi (`"1"` → `transactions.daromad_qoshish` va hokazo). Noto'g'ri raqam kiritilsa, xato xabari chiqadi va menyu qayta ko'rsatiladi.

## 7. Balans qanday hisoblanadi

Formula:

```text
Balans = jami daromad − jami xarajat
```

Kodda bu ikki funksiya orqali amalga oshiriladi (`reports.py`):

```python
def tur_boyicha_jami(tur):
    return sum(tr["amount"] for tr in database.tranzaksiyalar if tr["type"] == tur)

def balansni_hisoblash():
    return tur_boyicha_jami("income") - tur_boyicha_jami("expense")
```

Bosqichlari:

1. `tur_boyicha_jami("income")` barcha daromadlar summasini qo'shadi.
2. `tur_boyicha_jami("expense")` barcha xarajatlar summasini qo'shadi.
3. `balansni_hisoblash()` birinchidan ikkinchisini ayiradi.

Xarajat summasi bazada **musbat** son sifatida saqlanadi. Uni balansdan ayirish faqat hisobot funksiyasida (`balansni_hisoblash`) bajariladi. Shu sababli `income` va `expense` turlari aralashib ketmaydi.

**Misol:**

| ID  | Turi    | Summa     |
| --- | ------- | --------- |
| 1   | income  | 5 000 000 |
| 2   | expense | 45 000    |
| 3   | expense | 300 000   |

Jami daromad = 5 000 000, jami xarajat = 45 000 + 300 000 = 345 000, balans = 5 000 000 − 345 000 = **4 655 000 so'm**.

Bo'sh ro'yxatda `sum()` 0 qaytaradi, shuning uchun tranzaksiya bo'lmaganda balans 0 bo'ladi va xato chiqmaydi.

## 8. Hisobotlar qaysi funksiyalarga tayanadi

Hisob-kitob faqat bir joyda yoziladi, ko'rsatuvchi funksiyalar esa tayyor hisoblovchi funksiyalarni chaqiradi. Shu tufayli kod takrorlanmaydi.

| Ko'rsatuvchi funksiya             | Tayanadigan hisoblovchi funksiyalar                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `balansni_korsatish()`            | `balansni_hisoblash()` → `tur_boyicha_jami()`                                                          |
| `umumiy_hisobotni_korsatish()`    | `tur_boyicha_jami()`, `balansni_hisoblash()`, `eng_katta_xarajat()`, `eng_kop_sarflangan_kategoriya()` |
| `kategoriya_filtrini_korsatish()` | `kategoriya_boyicha_filtrlash()`                                                                       |
| `yuqori_xarajatlarni_korsatish()` | `yuqori_xarajatlar()`                                                                                  |

Umumiy hisobotdagi har bir qator manbasi:

| Hisobot qatori                 | Qaysi funksiyadan olinadi         |
| ------------------------------ | --------------------------------- |
| Jami daromad                   | `tur_boyicha_jami("income")`      |
| Jami xarajat                   | `tur_boyicha_jami("expense")`     |
| Joriy balans                   | `balansni_hisoblash()`            |
| Tranzaksiyalar soni            | `len(database.tranzaksiyalar)`    |
| Eng katta xarajat              | `eng_katta_xarajat()`             |
| Eng ko'p sarflangan kategoriya | `eng_kop_sarflangan_kategoriya()` |

## 9. Funksiyalar ro'yxati

### `database.py`

| Funksiya / o'zgaruvchi | Vazifasi                                               |
| ---------------------- | ------------------------------------------------------ |
| `tranzaksiyalar`       | Barcha tranzaksiyalar ro'yxati (`list` ichida `dict`). |
| `_holat`               | Keyingi ID ni saqlovchi `dict`.                        |
| `keyingi_id_olish()`   | Yangi ID qaytaradi va hisoblagichni 1 ga oshiradi.     |

### `utils.py`

| Funksiya                             | Vazifasi                                                            |
| ------------------------------------ | ------------------------------------------------------------------- |
| `musbat_son_olish(savol)`            | Musbat butun son kiritilguncha qayta so'raydi.                      |
| `bosh_emas_matn_olish(savol)`        | Bo'sh bo'lmagan matn kiritilguncha qayta so'raydi.                  |
| `butun_son_olish(savol)`             | Butun son o'qiydi, noto'g'ri bo'lsa `None` qaytaradi (ID uchun).    |
| `summani_formatlash(summa)`          | `45000` → `45 000 so'm`.                                            |
| `tranzaksiyalarni_chiqarish(royxat)` | Tranzaksiyalarni jadval qilib chiqaradi, bo'sh bo'lsa xabar beradi. |
| `TUR_NOMLARI`                        | `income` → `DAROMAD`, `expense` → `XARAJAT`.                        |

### `transactions.py`

| Funksiya                                            | Vazifasi                                            |
| --------------------------------------------------- | --------------------------------------------------- |
| `tranzaksiya_qoshish(tur, summa, kategoriya, izoh)` | Tekshiruvdan o'tkazib, bazaga qo'shadi.             |
| `daromad_qoshish()`                                 | Foydalanuvchidan ma'lumot olib, `income` qo'shadi.  |
| `xarajat_qoshish()`                                 | Foydalanuvchidan ma'lumot olib, `expense` qo'shadi. |
| `hammasini_korsatish()`                             | Barcha tranzaksiyalarni ko'rsatadi.                 |
| `id_boyicha_topish(tranzaksiya_id)`                 | ID bo'yicha topadi, topilmasa `None`.               |
| `tranzaksiya_ochirish()`                            | ID so'raydi, topilsa o'chiradi.                     |

### `reports.py`

| Funksiya                                   | Vazifasi                                                        |
| ------------------------------------------ | --------------------------------------------------------------- |
| `tur_boyicha_jami(tur)`                    | Berilgan turdagi tranzaksiyalar yig'indisi.                     |
| `balansni_hisoblash()`                     | Jami daromad − jami xarajat.                                    |
| `eng_katta_xarajat()`                      | Eng katta xarajat yoki `None`.                                  |
| `kategoriya_boyicha_filtrlash(kategoriya)` | Kategoriya bo'yicha ro'yxat (katta-kichik harfga bog'liq emas). |
| `yuqori_xarajatlar(chegara)`               | Chegaradan katta xarajatlar ro'yxati.                           |
| `eng_kop_sarflangan_kategoriya()`          | Eng ko'p sarflangan kategoriya va summa, yoki `None`.           |
| `balansni_korsatish()`                     | Balansni chiqaradi.                                             |
| `umumiy_hisobotni_korsatish()`             | Umumiy hisobotni chiqaradi.                                     |
| `kategoriya_filtrini_korsatish()`          | Kategoriya so'rab, natijani chiqaradi.                          |
| `yuqori_xarajatlarni_korsatish()`          | Chegara so'rab, natijani chiqaradi.                             |

### `main.py`

| Nom          | Vazifasi                                               |
| ------------ | ------------------------------------------------------ |
| `MENYU`      | Menyu matni.                                           |
| `HARAKATLAR` | Menyu raqami → funksiya lug'ati.                       |
| `asosiy()`   | Menyu sikli: tanlov oladi va mos funksiyani chaqiradi. |

## 10. Xatoliklarni qayta ishlash

| Holat                                | Dastur xatti-harakati                                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Manfiy yoki nol summa                | "Summa 0 dan katta bo'lishi kerak" xabari, qayta so'raydi.                                                  |
| Summa o'rniga matn                   | "Faqat butun son kiriting" xabari, qayta so'raydi.                                                          |
| Bo'sh kategoriya yoki izoh           | "Bo'sh qoldirib bo'lmaydi" xabari, qayta so'raydi.                                                          |
| Noto'g'ri tranzaksiya turi           | `tranzaksiya_qoshish` `ValueError` ko'taradi (menyu orqali bu holat bo'lmaydi, tur dasturning o'zi beradi). |
| Mavjud bo'lmagan ID                  | "Tranzaksiya topilmadi" xabari, hech narsa o'chirilmaydi.                                                   |
| ID o'rniga matn                      | "Butun son kiriting" xabari.                                                                                |
| Bo'sh ro'yxatni ko'rish              | "Tranzaksiyalar topilmadi" xabari.                                                                          |
| Tranzaksiya yo'q holda hisobot       | Hamma qiymatlar 0, "xarajatlar hali yo'q" yozuvi.                                                           |
| Xarajat yo'q holda eng katta xarajat | `eng_katta_xarajat()` `None` qaytaradi, `max()` bo'sh ro'yxatda chaqirilmaydi.                              |
| Kategoriya topilmasa                 | "Kategoriyada tranzaksiya topilmadi" xabari.                                                                |
| Menyuda noto'g'ri raqam              | "Menyudagi raqamlardan birini tanlang" xabari.                                                              |

Himoya ikki qatlamli: avval `utils.py` funksiyalari inputni tekshiradi, keyin `tranzaksiya_qoshish` funksiyasi ma'lumotni yana bir bor tekshiradi.

## 11. Demo

Quyidagi ketma-ketlik: 5 000 000 so'm daromad, ikkita xarajat, ro'yxat, filtr, hisobot va o'chirish.

```text
===== PERSONAL FINANCE TRACKER =====
...
Tanlang: 1
Summa (so'm): 5000000
Kategoriya: Maosh
Izoh: Oylik
Saqlandi! (ID: 1)

Tanlang: 2
Summa (so'm): 45000
Kategoriya: Food
Izoh: Tushlik
Saqlandi! (ID: 2)

Tanlang: 2
Summa (so'm): 300000
Kategoriya: Transport
Izoh: Taksi
Saqlandi! (ID: 3)

Tanlang: 3
ID   TURI                 SUMMA  KATEGORIYA     IZOH
----------------------------------------------------------------
1    DAROMAD    +5 000 000 so'm  Maosh          Oylik
2    XARAJAT       -45 000 so'm  Food           Tushlik
3    XARAJAT      -300 000 so'm  Transport      Taksi

Tanlang: 7
Kategoriya: FOOD
ID   TURI                 SUMMA  KATEGORIYA     IZOH
----------------------------------------------------------------
2    XARAJAT       -45 000 so'm  Food           Tushlik

Tanlang: 8
Chegara summasi (so'm): 100000
ID   TURI                 SUMMA  KATEGORIYA     IZOH
----------------------------------------------------------------
3    XARAJAT      -300 000 so'm  Transport      Taksi

Tanlang: 5
Joriy balans: 4 655 000 so'm

Tanlang: 6

--- UMUMIY HISOBOT ---
Jami daromad : 5 000 000 so'm
Jami xarajat : 345 000 so'm
Joriy balans : 4 655 000 so'm
Tranzaksiyalar soni: 3
Eng katta xarajat: 300 000 so'm (Transport - Taksi)
Eng ko'p sarflangan kategoriya: transport (300 000 so'm)

Tanlang: 4
O'chiriladigan tranzaksiya ID si: 2
ID=2 tranzaksiya o'chirildi.

Tanlang: 0
Xayr!
```

Kategoriya `FOOD` deb kiritilganda ham `Food` kategoriyasi topilganiga e'tibor bering: taqqoslash katta-kichik harfga bog'liq emas.

## 12. Sinov rejasi

Quyidagi holatlarni qo'lda sinab ko'ring:

| #   | Harakat                                    | Kutilgan natija                                  |
| --- | ------------------------------------------ | ------------------------------------------------ |
| 1   | Yangi ishga tushirib, `3` (ko'rish)        | "Tranzaksiyalar topilmadi"                       |
| 2   | Yangi ishga tushirib, `6` (hisobot)        | Hamma 0, "xarajatlar hali yo'q"                  |
| 3   | Yangi ishga tushirib, `4` (o'chirish)      | "O'chirish uchun hech narsa yo'q"                |
| 4   | Daromad qo'shishda summa `-5`              | Xato, qayta so'raydi                             |
| 5   | Summa `0`                                  | Xato, qayta so'raydi                             |
| 6   | Summa `abc`                                | Xato, qayta so'raydi                             |
| 7   | Kategoriyani bo'sh qoldirish (Enter)       | Xato, qayta so'raydi                             |
| 8   | O'chirishda mavjud bo'lmagan ID (`99`)     | "Topilmadi", ro'yxat o'zgarmaydi                 |
| 9   | Faqat daromad qo'shib, hisobot ochish      | Eng katta xarajat o'rniga "xarajatlar hali yo'q" |
| 10  | `Food` qo'shib, `fOOd` deb filtrlash       | Topiladi                                         |
| 11  | Mavjud bo'lmagan kategoriya                | "Topilmadi" xabari                               |
| 12  | Chegara 300000 bo'lganda 300000 li xarajat | Chiqmaydi (qat'iy katta)                         |
| 13  | Menyuda `9` yoki `abc`                     | "Menyudagi raqamlardan birini tanlang"           |

## 13. Qabul qilish mezonlari

- [x] Daromad va xarajat qo'shiladi.
- [x] Tranzaksiyalar ro'yxati ko'rsatiladi.
- [x] Tranzaksiya ID orqali o'chiriladi.
- [x] Balans formulasi to'g'ri ishlaydi.
- [x] Umumiy hisobot to'g'ri hisoblanadi.
- [x] Kategoriya bo'yicha filtrlash ishlaydi.
- [x] Musbat summa tekshiriladi.
- [x] Kod modullarga ajratilgan va funksiyalar qayta ishlatiladi.

## 14. Qo'shimcha challenge

| Challenge                                        | Holati                                                                 |
| ------------------------------------------------ | ---------------------------------------------------------------------- |
| Tranzaksiyalarni summa bo'yicha saralash         | Bajarilmagan                                                           |
| Eng ko'p pul sarflangan kategoriyani topish      | Bajarilgan (`eng_kop_sarflangan_kategoriya`, umumiy hisobotda chiqadi) |
| Faqat daromad yoki faqat xarajatlarni ko'rsatish | Bajarilmagan                                                           |
| JSON faylga saqlash va qayta yuklash             | Bajarilmagan                                                           |
| Matnli hisobot eksporti                          | Bajarilmagan                                                           |

## 15. Cheklovlar va kelajak rejalari

- Ma'lumotlar faylga saqlanmaydi, dastur yopilganda yo'qoladi. Keyingi qadam: `json` moduli bilan saqlash va yuklash.
- Tranzaksiyada sana yo'q. Sana qo'shilsa, oylik hisobot qilish mumkin.
- Kategoriyalar erkin matn. Kelajakda tayyor kategoriyalar ro'yxatidan tanlash qo'shilishi mumkin.
- Tranzaksiyani tahrirlash imkoniyati yo'q (faqat o'chirish).
