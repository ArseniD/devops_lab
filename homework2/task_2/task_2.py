import math


def quadratic_roots(A, B, C, min_root, max_root):
    """
    Solve the quadratic equation: Ax^2 + Bx + C = 0

    :param A: first polynomial coefficient
    :param B: second polynomial coefficient
    :param C: third polynomial coefficient
    :param min_root: min root value
    :param max_root: max root value
    :return: return quadratic roots in the range [min_root, max_root]
    """
    roots = []
    delta = B ** 2 - 4 * A * C

    if delta > 0:
        root_1 = 0
        root_2 = 0
        if A != 0:
            sgn = 1
            if B < 0:
                sgn = -1
            Q = -0.5 * (B + sgn * delta ** 2)
            # convert roots from float to integer
            root_1 += int(round(Q / A))
            root_2 += int(round(root_1))
            if Q != 0:
                root_2 = C / Q
        else:
            # convert roots from float to integer
            root_1 = int(round(-C / B))
            root_2 = root_1
        # order roots
        if root_1 > root_2:
            # convert roots from float to integer
            tmp = int(round(root_1))
            root_1 = root_2
            root_2 = tmp
        if min_root <= root_1 <= max_root:
            roots.append(root_1)
        if root_2 != root_1 and min_root <= root_2 <= max_root:
            roots.append(root_2)
    else:
        if A != 0:
            root_1 = -B / (2 * A)
            if min_root <= root_1 <= max_root:
                roots.append(root_1)
    return roots


def cubic_roots(A, B, C, D, min_root, max_root):
    """
    Solve the cubic equation: Ax^3 + Bx^2 + Cx + D = 0
    via the Vieta trigonometric formula

    :param A: first polynomial coefficient
    :param B: second polynomial coefficient
    :param C: third polynomial coefficient
    :param D: real number
    :param min_root: min root value
    :param max_root: max root value
    :return: sort and return cubic roots in the range [min_root, max_root]
    """
    if A != 0:

        roots = []

        a = B / A
        b = C / A
        c = D / A

        Q = (a * a - 3 * b) / 9.0
        R = (2 * a ** 3 - 9.0 * a * b + 27.0 * c) / 54.0

        Q_3 = Q ** 3
        R_2 = R ** 2
        S = R_2 - Q_3

        if S <= 0:
            ratio = R / Q_3 ** 0.5
            theta = math.acos(ratio)
            qr = -2.0 * Q ** 0.5
            a_3 = a / 3.0
            root_1 = round(qr * math.cos(theta / 3.0) - a_3)
            root_2 = round(qr * math.cos((theta + 2.0 * math.pi) / 3.0) - a_3)
            root_3 = round(qr * math.cos((theta - 2.0 * math.pi) / 3.0) - a_3)

            root_list = [root_1, root_2, root_3]

            for elem in sorted(root_list):
                if min_root <= elem <= max_root and elem not in roots:
                    roots.append(int(elem))
        else:
            big_a = 0
            if R > 0:
                big_a += -math.pow(R + S ** 0.5, 1.0 / 3.0)
            else:
                big_a += math.pow(-R + S ** 0.5, 1.0 / 3.0)
            big_b = 0.0
            if big_a != 0:
                big_b = Q / big_a
            root_1 = (big_a + big_b) - Q / 3.0
            if min_root <= root_1 <= max_root:
                roots.append(root_1)
        return roots
    else:
        # call quadratic_roots function if A variable is not presented
        return quadratic_roots(B, C, D, min_root, max_root)


if __name__ == '__main__':

    # Performed small tests
    assert quadratic_roots(1, 3, 2, -100, 100) == [-2, -1]
    assert cubic_roots(1, -3, 0, 0, -100, 100) == [0, 3]
    assert cubic_roots(3, -15, 18, 0, -100, 100) == [0, 2, 3]
    assert cubic_roots(1, -7, -33, 135, -100, 100) == [-5, 3, 9]

    # This construction will works only with Python 3.5 versions,
    # Python versions < 3.5 do not allow positional arguments after *expression
    # My previous method commented out and described below
    lines = [map(int, line.split()) for line in open('INPUT.TXT')]
    variable_list = lines[0]

    result = cubic_roots(*variable_list, -100, 100)

    # This construction will works with all Python versions
    # lines = [line.strip() for line in open('INPUT.TXT')]
    #
    # A = int(lines[0].split()[0])
    # B = int(lines[0].split()[1])
    # C = int(lines[0].split()[2])
    # D = int(lines[0].split()[3])
    #
    # result = cubic_roots(A, B, C, D, -100, 100)

    str_result = ' '.join(str(e) for e in result)

    with open('OUTPUT.TXT', 'w') as file:
        file.write(str_result)
