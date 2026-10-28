import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# Starter tests from test_car_insurance_premium.py
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600

def test_no_bonus():
    assert no_claim_bonus(0) == 0


# annual_premium: one test per line the starter tests never ran
def test_unknown_car_type_raises():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)

def test_driver_too_young_raises():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)

def test_young_driver_no_claims_anti_theft():
    # 8000 + 4000 = 12000 -> -20% = 9600 -> -500 = 9100
    assert annual_premium("hatchback", 22, 0, True) == 9100

def test_senior_driver_many_claims():
    # 15000 + 2000 = 17000 -> x2 = 34000
    assert annual_premium("suv", 65, 3, False) == 34000


# no_claim_bonus
def test_negative_years_raises():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)

def test_bonus_five_years():
    assert no_claim_bonus(5) == 50

def test_bonus_three_years():
    assert no_claim_bonus(3) == 35

def test_bonus_one_year():
    assert no_claim_bonus(1) == 20


# claim_payout
def test_negative_damage_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-1, 300000, 1000, False)

def test_total_loss_pays_insured_value():
    assert claim_payout(5000, 300000, 1000, True) == 300000

def test_damage_within_deductible_pays_nothing():
    assert claim_payout(800, 300000, 1000, False) == 0

def test_payout_capped_at_insured_value():
    assert claim_payout(500000, 300000, 1000, False) == 300000

def test_normal_payout():
    assert claim_payout(20000, 300000, 1000, False) == 19000


# ---- Added for branch coverage ----

# Missed branch 16->18: 1-2 claims means neither "claims == 0" nor "claims > 2"
def test_one_claim_no_adjustment():
    assert annual_premium("sedan", 40, 1, False) == 12000

def test_two_claims_no_adjustment():
    assert annual_premium("sedan", 40, 2, False) == 12000


# Age boundaries: 18 allowed, <25 young surcharge, >=60 senior surcharge
@pytest.mark.parametrize("age, expected", [
    (18, 12800),   # (12000 + 4000) - 3200
    (24, 12800),
    (25, 9600),    # 12000 - 2400
    (59, 9600),
    (60, 11200),   # (12000 + 2000) - 2800
])
def test_age_boundaries(age, expected):
    assert annual_premium("sedan", age, 0, False) == expected


# no_claim_bonus boundaries between the tiers
@pytest.mark.parametrize("years, expected", [
    (2, 20), (4, 35), (10, 50),
])
def test_bonus_tier_boundaries(years, expected):
    assert no_claim_bonus(years) == expected


# claim_payout: the second half of "damage_cost < 0 or deductible < 0"
def test_negative_deductible_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(5000, 300000, -1, False)

def test_damage_equal_to_deductible_pays_nothing():
    assert claim_payout(1000, 300000, 1000, False) == 0

def test_payout_equal_to_insured_value():
    assert claim_payout(301000, 300000, 1000, False) == 300000
