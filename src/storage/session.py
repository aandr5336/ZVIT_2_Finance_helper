_user_id = None
_user_name = ""
_user_email = ""


class Session:
    @classmethod
    def login(cls, user_id: int, name: str, email: str):
        global _user_id, _user_name, _user_email
        _user_id = user_id
        _user_name = name
        _user_email = email

    @classmethod
    def logout(cls):
        global _user_id, _user_name, _user_email
        _user_id = None
        _user_name = ""
        _user_email = ""

    @classmethod
    def is_logged_in(cls) -> bool:
        return _user_id is not None

    @classmethod
    def user_id(cls):
        return _user_id

    @classmethod
    def user_name(cls) -> str:
        return _user_name

    @classmethod
    def user_email(cls) -> str:
        return _user_email
_currency = "UAH"
_usd_rate = 41.0

class Currency:
    @classmethod
    def get(cls) -> str:
        return _currency

    @classmethod
    def set(cls, code: str):
        global _currency
        _currency = code

    @classmethod
    def get_rate(cls) -> float:
        return _usd_rate

    @classmethod
    def set_rate(cls, rate: float):
        global _usd_rate
        _usd_rate = rate

    @classmethod
    def symbol(cls) -> str:
        return "₴" if _currency == "UAH" else "$"

    @classmethod
    def format(cls, amount: float) -> str:
        if _currency == "UAH":
            return f"₴ {amount:,.0f}".replace(",", " ")
        else:
            converted = amount / _usd_rate
            return f"$ {converted:,.2f}"