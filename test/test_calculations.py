import pytest
from app import calculations

@pytest.fixture
def zero_bank_account():
    return calculations.BankAccount()

@pytest.fixture
def bank_account():
    return calculations.BankAccount(50)

@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, result):
    print("testing add function")
    assert calculations.add(num1,num2) == result

def test_subtract():
    print("testing subtract function")
    assert calculations.subtract(9,4) == 5

def test_multiply():
    print("testing multiplication function")
    assert calculations.multipy(5,4) == 20

def test_devide():
    print("testing divide function")
    assert calculations.devide(10,2) == 5

### test case for bank account class ###
# @pytest.mark.parametrize("value, result", [
#     (50,50),
#     (70,70),
#     (100,100)
# ])
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

@pytest.mark.parametrize("amount, result", [
    (10, 40),
    (20, 30),
    (50, 0)
])
def test_withdraw(amount,result, bank_account):
    bank_account.withdraw(amount)
    assert bank_account.balance == result

@pytest.mark.parametrize("amount, result", [
    (10, 60),
    (20, 70),
    (100, 150)
])
def test_deposit(bank_account, amount, result):
    bank_account.deposit(amount)
    assert bank_account.balance == result

def test_collect_intrest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, result", [
    (70,20, 50),
    (100,90, 10),
    (100, 100, 0),
])
def test_bank_transaction(deposited, withdrew, result, zero_bank_account):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == result

def test_insufficent_funds(bank_account):
    with pytest.raises(calculations.insufficent_funds):
        bank_account.withdraw(100)

