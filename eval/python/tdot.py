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


def index_ports(ports, length, ty):
    res = []
    for i in range(length):
        for p in ports:
            res.append(expr(name(p, i), ty))
    return res


def ports(ports, ty):
    res = []
    for p in ports:
        res.append(expr(p, ty))
    return res


def sig(name, en, lhs, rhs, val, res, length, ty):
    inp = []
    inp += index_ports(lhs, length, ty)
    inp += index_ports(rhs, length, ty)
    inp += ports(val, ty)
    inp.append(expr(en, "bool"))
    out = ports(res, ty)
    i = ", ".join(inp)
    o = ", ".join(out)
    sig = "def {}({})->({})".format(name, i, o)
    return sig


def prog(sig, body):
    body = "\n".join(body)
    prog = "{} {{\n{}\n}}".format(sig, body)
    return prog


def emit(name, length):
    ty = "i8"
    t = 0
    body = []
    lhs = ["a", "c", "e", "g"]
    rhs = ["b", "d", "f", "h"]
    val = ["m", "n", "o", "p"]
    res = ["w", "x", "y", "z"]
    en = "en"
    s = sig(name, en, lhs, rhs, val, res, length, ty)
    for i in range(4):
        t, tb = dot(lhs[i], rhs[i], val[i], en, res[i], t, length)
        body += tb
    return prog(s, body)


if __name__ == "__main__":
    print(emit("main", 2))
