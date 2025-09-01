def get_max_exp(level: int) -> int:
    return 50 * int(level ** 2.04)


def unitize(n: int) -> str:
    if n < 10000:
        return str(n)

    units = ['', '만', '억', '조', '경', '해', '자', '양', '구', '간', '정']
    result = []
    while n > 0:
        result.append(f"{n % 10000}{units[len(result)]}")
        n //= 10000
    return ' '.join(reversed(result))
