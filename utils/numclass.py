def one_many(val: int):
    return 0 if val == 1 else 1

def one_two_five(val: int):
    val = val % 100
    d, r = divmod(val, 10)
    if d == 1 or not (1 <= r <= 4):
        return 2  # = 5
    return 0 if r == 1 else 1  # = 1 or = 2
