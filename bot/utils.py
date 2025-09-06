def get_max_exp(level: int) -> int:
    return 50 * int(level ** 2.04)


def unitize(n: int) -> str:
    if n < 10000:
        return str(n)

    units = ['', '만', '억', '조', '경', '해', '자', '양', '구', '간', '정']
    result = []
    i = 0
    while n > 0:
        if n % 10000 > 0:
            result.append(f"{n % 10000}{units[i]}")
        n //= 10000
        i += 1
    return ' '.join(reversed(result))
