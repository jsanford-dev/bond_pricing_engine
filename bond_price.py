from datetime import datetime
from dateutil.relativedelta import relativedelta

class Bond:
    """
    Base class for calculating bond prices (dirty and clean) and accrued interest.
    Supports both nominal bonds and inflation-indexed bonds, as well as Treasury Bills.

    Parameters:
        settle: Settlement date (datetime)
        maturity: Maturity date (datetime)
        coupon: Annual coupon rate (float, defaults to 0 for T-bills)
        ytm: Yield to maturity (float)
        face_value: Face value of the bond (float)
        freq: Coupon frequency per year (int, defaults to 2 for nominal bonds)
        day_count: Days in a year for day count convention (float, defaults to 365)
        p_value: Base inflation adjustment factor (float, defaults to 0 for nominal bonds)
        kt_factor: Current inflation adjustment factor (float, defaults to 0 for nominal bonds)
    """

    def __init__(self, settle: datetime, maturity: datetime, coupon: float = 0.0, ytm: float = 0.0, face_value: float = 100.0, 
                 freq: int = 2, day_count:int = 365, p_value:float = 0.0, kt_factor: float = 0.0) -> None:
        self.settle = settle
        self.maturity = maturity
        self.coupon = coupon
        self.ytm = ytm
        self.face_value = face_value
        self.freq = freq
        self.day_count = day_count
        self.p_value = p_value
        self.kt_factor = kt_factor

        # Validate inputs
        self.validate_inputs()

        # Calculate key attributes
        self.last_coupon = self.get_last_coupon()
        self.next_coupon = self.get_next_coupon()
        self.n = self.determine_n()
        self.c = self.determine_c()
        self.a = self.determine_a()
        self.b = self.determine_b()

    def validate_inputs(self):
        """Validate inputs to ensure consistent and logical parameters."""
        if self.settle >= self.maturity:
            raise ValueError("Settlement date must be before maturity date.")
        if self.face_value <= 0:
            raise ValueError("Face value must be positive.")

    def get_last_coupon(self):
        """Calculate the date of the last coupon paid."""
        last_coupon = self.maturity
        while last_coupon > self.settle:
            last_coupon -= relativedelta(months=12 // self.freq)
        return last_coupon

    def get_next_coupon(self):
        """Calculate the date of the next coupon due."""
        return self.last_coupon + relativedelta(months=12 // self.freq)

    def determine_n(self):
        """Calculate the number of remaining coupon payments."""
        return round(((self.maturity - self.next_coupon).days / self.day_count) * self.freq)

    def determine_c(self):
        """Determine if the bond is ex-coupon."""
        ex_coupon_date = self.next_coupon - relativedelta(days=10)
        return 0 if self.settle > ex_coupon_date else 1

    def determine_a(self):
        """Calculate the number of days from settlement to the next coupon."""
        return (self.next_coupon - self.settle).days

    def determine_b(self):
        """Calculate the number of days between coupon payments."""
        return (self.next_coupon - self.last_coupon).days

    def calculate_accrued_interest(self):
        """Calculate accrued interest for the bond."""
        if self.c == 1:
            # General case
            accrued_interest = ((self.coupon / self.freq) * self.face_value * max(1, self.kt_factor / 100)) * ((self.b - self.a) / self.b)
        else:
            # Special case: Settlement date after record date
            accrued_interest = ((self.coupon / self.freq) * self.face_value * max(1, self.kt_factor / 100)) * (-self.a / self.b)
        return accrued_interest

    def calculate_dirty_price(self):
        """Calculate the bond settlement (Dirty) price."""
        if self.n == 0:
            # Special case: Only one coupon remaining
            price = self.face_value * (1 + (self.coupon / self.freq)) / (1 + (self.ytm * ((self.maturity - self.settle).days / self.day_count)))
        else:
            # General case
            discount_factor = 1 / (1 + (self.ytm / self.freq)) ** self.n
            annuity_factor = (1 - discount_factor) / (self.ytm / self.freq)
            coupon_payment = (self.coupon / self.freq) * (self.c + annuity_factor)
            adjustment_factor = (1 + (self.ytm / self.freq)) ** (self.a / self.b)

            inflation_factor = max(1, (self.kt_factor * (1 + self.p_value / 100) ** (-self.a / self.b)) / 100)

            price = (discount_factor + coupon_payment) / adjustment_factor * self.face_value * inflation_factor
        return price

    def calculate_clean_price(self):
        """Calculate the clean price of the bond."""
        dirty_price = self.calculate_dirty_price()
        accrued_interest = self.calculate_accrued_interest()
        clean_price = dirty_price - accrued_interest
        return clean_price
