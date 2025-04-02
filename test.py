def solution(string: str) -> bool:
    a = list(string)
    b = []
    for i, c in enumerate(a[::-1]):
        b.append(c)
        b.extend(a)
        left = "".join(b)
        right = left[::-1]
        print(f"{left} == {right}")
        if left == right:
            return True
        b = b[:i + 1]
        print(b)
    return False



# abcd => dcbabcd
print(solution("aacecaaa"))

