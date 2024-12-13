import unittest
from datetime import datetime
from bond_price import Bond

class TestBond(unittest.TestCase):
    def test_nominal_bond(self):
        bond = Bond(
            settle = datetime(2022, 11, 22),
            maturity = datetime(2034, 5, 15),
            coupon = 0.0425,
            ytm = 0.04355
        )
        self.assertAlmostEqual(bond.calculate_dirty_price(), 99.1405640616, places=10)
        self.assertAlmostEqual(bond.calculate_accrued_interest(), 0.0821823204, places=10)
        self.assertAlmostEqual(bond.calculate_clean_price(), 99.0583817412, places=10)
    
    def test_nominal_bond_final_coupon(self):
        bond = Bond(
            settle = datetime(2051, 4, 15),
            maturity = datetime(2051, 5, 15),
            coupon = 0.0275,
            ytm = 0.05348
        )

        self.assertAlmostEqual(bond.calculate_clean_price(), 99.7842450753699, places=10)
        self.assertAlmostEqual(bond.calculate_accrued_interest(), 1.1470994475, places=10)
        self.assertAlmostEqual(bond.calculate_dirty_price(), 100.93134452287, places=10)

    def test_inflation_indexed_bond(self):
        bond = Bond(
            settle=datetime(2022, 8, 31),
            maturity=datetime(2035, 9, 20),
            coupon=0.025,
            ytm=0.0219,
            freq=4,
            p_value=1.63,
            kt_factor=116.69
        )
        self.assertAlmostEqual(bond.calculate_dirty_price(), 120.932155367, places=10)
        self.assertAlmostEqual(bond.calculate_accrued_interest(), 0.5707663043, places=10)
        self.assertAlmostEqual(bond.calculate_clean_price(), 120.3613890627, places=10)

    def test_inflation_indexed_bond_record_date(self):
        bond = Bond(
            settle=datetime(2022, 9, 18),
            maturity=datetime(2035, 9, 20),
            coupon=0.025,
            ytm=0.0219,
            freq=4,
            p_value=1.63,
            kt_factor=116.69
        )
        self.assertAlmostEqual(bond.calculate_dirty_price(), 120.7160176389, places=10)
        self.assertAlmostEqual(bond.calculate_accrued_interest(), -0.01585461956521739, places=10)
        self.assertAlmostEqual(bond.calculate_clean_price(), 120.7318722585, places=10)

    def test_treasury_bill(self):
        t_bill = Bond(
            settle=datetime(2023, 9, 26),
            maturity=datetime(2024, 7, 31),
            ytm=0.05,
            freq=1
        )
        self.assertAlmostEqual(t_bill.calculate_dirty_price(), 95.9390195821, places=10)
        self.assertAlmostEqual(t_bill.calculate_accrued_interest(), 0, places=10)
        self.assertAlmostEqual(t_bill.calculate_clean_price(), 95.9390195821, places=10)

if __name__ == "__main__":
    unittest.main()
