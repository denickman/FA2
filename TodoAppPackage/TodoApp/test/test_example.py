import pytest




class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('Jonh', 'Doe', 'Computer Science', 3)



def test_person_init(default_employee):

    assert default_employee.first_name == 'Jonh', 'First name should be Jonh'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'

    assert default_employee.major == 'Computer Science', 'Major should be Computer Science'
    assert default_employee.years == 3



























def test_equal_or_not_equal():
    assert 3 == 3



def test_is_instance():
    assert isinstance('this is string', str)
    assert not isinstance('this string', int)