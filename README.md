# Bond pricing engine
A Python-based tool for calculating clean and dirty bond prices, accrued interest, and supporting fixed-income instruments such as nominal bonds, inflation-indexed bonds, and Treasury bills. The pricing methods are based on formulas outlined in the respective New Zealand Government Security Information Memorandums. This tool is useful for fixed-income analysts, portfolio managers, and financial developers, particularly those involved in the New Zealand Government Securities market.

## Features
- Calculate clean and dirty bond prices.
- Compute accrued interest for nominal and inflation-indexed bonds.
- Support for discount instruments like Treasury bills.
- Customizable day count conventions and coupon frequencies.
- Formulae based on New Zealand Government Security Information Memorandums.

## Installation

### Clone the Repository
```bash
git clone https://github.com/jsanford-dev/bond_pricing_engine.git
cd bond_pricing_engine
```

### Run Tests
Ensures results reconcile with prices published on term sheets and Bloomberg's BXT<Go>.
```bash
python -m unittest discover tests
```

## Usage

### Example: Nominal Bond
```python
from bond_price import Bond
from datetime import datetime

bond = Bond(
    settle=datetime(2022, 11, 22),
    maturity=datetime(2034, 5, 15),
    coupon=0.0425,
    ytm=0.04355
)

print("Dirty Price:", bond.calculate_dirty_price())
print("Clean Price:", bond.calculate_clean_price())
print("Accrued Interest:", bond.calculate_accrued_interest())
```

### Example: Inflation Indexed Bonds
```python
from bond_price import Bond
from datetime import datetime

bond = Bond(
    settle=datetime(2022, 8, 31),
    maturity=datetime(2035, 9, 20),
    coupon=0.025,
    ytm=0.0219,
    freq=4,
    p_value=1.63,
    kt_factor=116.69
)

print("Dirty Price:", bond.calculate_dirty_price())
print("Clean Price:", bond.calculate_clean_price())
print("Accrued Interest:", bond.calculate_accrued_interest())
```

### Example: Treasury Bill
```python
from bond_price import Bond
from datetime import datetime

t_bill = Bond(
    settle=datetime(2023, 9, 26),
    maturity=datetime(2024, 7, 31),
    ytm=0.05,
    freq=1
)
print("Dirty Price:", t_bill.calculate_dirty_price())
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The pricing formulas in this tool are based on the **New Zealand Government Bonds Information Memorandums**.

## Links
[New Zealand Debt Management - website](https://debtmanagement.treasury.govt.nz/)

[New Zealand Inflation Indexed bond factors](https://debtmanagement.treasury.govt.nz/investor-resources/data)

[GitHub Repository](https://github.com/jsanford-dev/bond_pricing_engine)
