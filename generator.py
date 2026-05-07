import random
import string

MIN_LENGTH = 4
MAX_LENGTH = 64

def generate_password(length=12, digits=True, letters=True, special=True):
    if not (digits or letters or special):
        raise ValueError("Должен быть выбран хотя бы один набор символов")
    pool = ""
    if digits:
        pool += string.digits
    if letters:
        pool += string.ascii_letters
    if special:
        pool += string.punctuation
    if length < 1:
        raise ValueError("Длина пароля должна быть положительным числом")
    return ''.join(random.choices(pool, k=length))

def validate_params(length, digits, letters, special):
    errors = []
    if not isinstance(length, int) or length < MIN_LENGTH or length > MAX_LENGTH:
        errors.append(f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
    if not (digits or letters or special):
        errors.append("Выберите хотя бы один тип символов")
    return errors
