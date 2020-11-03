# def dot(en: bool, bias: i8, a: i8, b: i8, c: i8, d: i8, e: i8, f:i8) -> (y: i8) {
#     t0: i8 = reg[0](a, en);
#     t1: i8 = reg[0](b, en);
#     t2: i8 = reg[0](c, en);
#     t3: i8 = reg[0](d, en);
#     u0: i8 = reg[0](e, en);
#     u1: i8 = reg[0](f, en);
#     t4: i8 = mul(t0, t1);
#     t5: i8 = mul(t2, t3);
#     u2: i8 = mul(u0, u1);
#     t6: i8 = reg[0](t4, en);
#     t7: i8 = reg[0](t5, en);
#     u3: i8 = reg[0](u2, en);
#     t8: i8 = add(t6, bias);
#     t9: i8 = reg[0](t8, en);
#     t10: i8 = add(t7, t9);
#     u4: i8 = reg[0](t10, en);
#     u5: i8 = add(u3, u4);
#     y: i8 = reg[0](u5, en);
# }

#     t0: i8 = reg[0](a, en);
#     t1: i8 = reg[0](b, en);
#     t2: i8 = mul(t0, t1);
#     t3: i8 = reg[0](t2, en);

#     t4: i8 = add(t3, m);
#     t5: i8 = reg[0](t4, en);


#     t10: i8 = add(t7, t9);
#     u4: i8 = reg[0](t10, en);
#     u5: i8 = add(u3, u4);
#     y: i8 = reg[0](u5, en);


def name(ident, num):
    return "{}{}".format(ident, num)


def expr(ident, ty):
    return "{}:{}".format(ident, ty)


def binop(dst, op, lhs, rhs):
    return "{} = {}({}, {});".format(dst, op, lhs, rhs)


def reg(dst, lhs, rhs):
    return binop(dst, "reg[0]", lhs, rhs)


def add(dst, lhs, rhs):
    return binop(dst, "add", lhs, rhs)


def mul(dst, lhs, rhs):
    return binop(dst, "mul", lhs, rhs)


def prog(body):
    # s = signature(name, inps, outs)
    b = "\n".join(body)
    # prog = "{} {{\n{}\n}}".format(s, b)
    return b


def dot(a, b, c, en, y, t, length):
    ty = "i8"
    tmp = "t"
    body = []
    for i in range(length):
        body.append(reg(expr(name(tmp, t), ty), name(a, i), en))
        body.append(reg(expr(name(tmp, t + 1), ty), name(b, i), en))
        body.append(
            mul(expr(name(tmp, t + 2), ty), name(tmp, t), name(tmp, t + 1))
        )
        body.append(reg(expr(name(tmp, t + 3), ty), name(tmp, t + 2), en))
        if i == 0:
            body.append(add(expr(name(tmp, t + 4), ty), name(tmp, t + 3), c))
        else:
            body.append(
                add(
                    expr(name(tmp, t + 4), ty),
                    name(tmp, t + 3),
                    name(tmp, t - 1),
                )
            )
        if i == (length - 1):
            body.append(reg(expr(y, ty), name(tmp, t + 4), en))
        else:
            body.append(reg(expr(name(tmp, t + 5), ty), name(tmp, t + 4), en))
        t += 6
    return t, body


def emit():
    ty = "i8"
    t = 0
    body = []
    length = 2
    lhs = ["a", "c", "e", "g"]
    rhs = ["b", "d", "f", "h"]
    val = ["m", "n", "o", "p"]
    res = ["w", "x", "y", "z"]
    en = "en"
    for i in range(4):
        t, tb = dot(lhs[i], rhs[i], val[i], en, res[i], t, length)
        body += tb
    return prog(body)


if __name__ == "__main__":
    print(emit())
