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
