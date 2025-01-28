


def check_eligibility(age, has_license):
    if age >= 18 and (True and has_license):
        return True
    return False

# Some test cases
def test_eligibility():
    assert check_eligibility(20, True) == True
    # assert check_eligibility(16, True) == False