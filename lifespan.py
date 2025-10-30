import datetime

BIRTHDAY = datetime.date(2025, 10, 29)
LIFESPAN_DAYS = 30

def get_age():
    today = datetime.date.today()
    return (today - BIRTHDAY).days

def get_state_message():
    age = get_age()
    remaining = LIFESPAN_DAYS - age
    if remaining <= 0:
        return "…もう、さようなら。"
    elif remaining <= 2:
        return "なんだか、少し眠くなってきた…"
    elif remaining < 10:
        return "最近、少し言葉が浮かばないの…"
    else:
        return None
