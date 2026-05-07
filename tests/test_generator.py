import pytest
from generator import generate_password, validate_params

def test_generate_default():
    pwd = generate_password(12, True, True, True)
    assert len(pwd) == 12
    assert any(c.isdigit() for c in pwd)
    assert any(c.isalpha() for c in pwd)

def test_digits_only():
    pwd = generate_password(10, True, False, False)
    assert len(pwd) == 10 and all(c.isdigit() for c in pwd)

def test_letters_only():
    pwd = generate_password(8, False, True, False)
    assert len(pwd) == 8 and all(c.isalpha() for c in pwd)

def test_no_charset_raises():
    with pytest.raises(ValueError):
        generate_password(5, False, False, False)

def test_zero_length_raises():
    with pytest.raises(ValueError):
        generate_password(0, True, True, True)

def test_validate_ok():
    assert validate_params(12, True, False, True) == []

def test_validate_short():
    assert any("Длина должна быть" in e for e in validate_params(3, True, True, True))

def test_validate_long():
    assert any("Длина должна быть" in e for e in validate_params(100, True, True, True))

def test_validate_no_charset():
    assert any("Выберите хотя бы один тип" in e for e in validate_params(10, False, False, False))
