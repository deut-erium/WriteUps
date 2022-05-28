from flag import flag


def rotate(point: list[int], rx: int, ry: int, n: int) -> None:
    if ry != 0:
        return
    if rx == 1:
        point[0] = n - 1 - point[0]
        point[1] = n - 1 - point[1]
    point[0] = point[0] + point[1]
    point[1] = point[0] - point[1]
    point[0] = point[0] - point[1]


def point_to_index(point: list[int], order: int) -> int:
    n = pow(2, order)
    index = 0
    s = n // 2
    while s:
        rx = 1 if point[0] & s else 0
        ry = 1 if point[1] & s else 0
        index += s * s * ((3 * rx) ^ ry)
        rotate(point, rx, ry, n)
        s = s // 2
    return index


def mesmerize(chars: list[str], rows: int) -> list[str]:
    assert len(chars) == len(chars[0])
    assert all([ len(row) == len(chars[0]) for row in chars ])
    assert len(chars) and (len(chars) & (len(chars) - 1)) == 0

    order = len(chars)
    mesmerized = [
        [ [''] for _ in range(order ** 2 // rows) ] for _ in range(rows)
    ]

    for i in range(order):
        for j in range(order):
            index = point_to_index([i, j], order)
            k = index % rows
            l = index // rows
            mesmerized[k][l] = chars[j][i]

    return mesmerized


if __name__ == "__main__":
    with open('chall.txt', 'w') as file:
        file.writelines([
            ''.join(c) + '\n' for c in mesmerize(flag, 32)
        ])
