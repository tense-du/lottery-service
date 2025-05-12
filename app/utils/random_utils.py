import string
import random


def generate_random_alphanumeric(length: int = 12) -> str:
    return "".join(
        random.choices(population=string.ascii_lowercase + string.digits, k=length)
    )
