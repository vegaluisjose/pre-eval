import argparse
import sys


def fmt(ident, num):
    return "{}{}".format(ident, num)


def expr(ident, ty):
    return "{}:{}".format(ident, ty)


def binop(dst, op, lhs, rhs):
    return "{} = {}({}, {});".format(dst, op, lhs, rhs)


def ins_mux(dst, cond, tru, fal):
    return "{} = mux({}, {}, {});".format(dst, cond, tru, fal)


def ins_id(dst, inp):
    return "{} = id({});".format(dst, inp)


def ins_reg(dst, lhs, rhs):
    return binop(dst, "reg[0]", lhs, rhs)


def ins_eq(dst, lhs, rhs):
    return binop(dst, "eq", lhs, rhs)


def ins_or(dst, lhs, rhs):
    return binop(dst, "or", lhs, rhs)


def ins_and(dst, lhs, rhs):
    return binop(dst, "and", lhs, rhs)


def ins_const(dst, value):
    return "{} = const[{}];".format(dst, value)


def gen_body(en, y, size):
    assert size >= 2
    ty = "i8"
    tmp = "t"
    body = []
    t = 0
    reg_inp = fmt(tmp, size * 6 - 1)
    reg_en = fmt(tmp, size * 6 - 2)
    cur = [i for i in range(size)]
    nxt = [i + 1 if i != size - 1 else 0 for i in range(size)]
    red = []
    for (c, n) in zip(cur, nxt):
        body.append(ins_const(expr(fmt(tmp, t), ty), c))
        body.append(ins_const(expr(fmt(tmp, t + 1), ty), n))
        body.append(ins_eq(expr(fmt(tmp, t + 2), "bool"), reg_inp, fmt(tmp, t)))
        body.append(ins_and(expr(fmt(tmp, t + 3), "bool"), en, fmt(tmp, t + 2)))
        red.append(fmt(tmp, t + 3))
        if c == 0:
            body.append(
                ins_mux(
                    expr(fmt(tmp, t + 4), ty),
                    fmt(tmp, t + 3),
                    fmt(tmp, t + 1),
                    reg_inp,
                )
            )
        else:
            body.append(
                ins_mux(
                    expr(fmt(tmp, t + 4), ty),
                    fmt(tmp, t + 3),
                    fmt(tmp, t + 1),
                    fmt(tmp, t - 1),
                )
            )
        t += 5
    for i in range(size - 1):
        if i == 0:
            body.append(ins_or(expr(fmt(tmp, t), "bool"), red[0], red[1]))
        else:
            body.append(
                ins_or(expr(fmt(tmp, t), "bool"), fmt(tmp, t - 1), red[i + 1])
            )
        t += 1
    body.append(ins_reg(expr(fmt(tmp, t), ty), fmt(tmp, t - size), reg_en))
    body.append(ins_id(expr(y, ty), fmt(tmp, t)))
    return body


def sig(name, en, y, ty):
    inp = expr(en, "bool")
    out = expr(y, ty)
    sig = "def {}({})->({})".format(name, inp, out)
    return sig


def prog(sig, body):
    body = "\n".join(body)
    prog = "{} {{\n{}\n}}".format(sig, body)
    return prog


def emit(name, size):
    ty = "i8"
    en = "en"
    y = "y"
    s = sig(name, en, y, ty)
    body = gen_body(en, y, size)
    return prog(s, body)


def parse_args():
    parser = argparse.ArgumentParser(description="generate fsm")
    parser.add_argument("-n", help="function name", type=str)
    parser.add_argument("-s", help="size of fsm", type=int)
    parser.add_argument("-o", help="output file", type=str)
    args = parser.parse_args()
    if not isinstance(args.n, str):
        print("Error: missing function name")
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not isinstance(args.s, int):
        print("Error: missing size parameter")
        parser.print_help(sys.stderr)
        sys.exit(1)
    return args.n, args.s, args.o


def fsm(name, length, output=None):
    if output:
        with open(output, "w") as file:
            file.write(emit(name, length))
    else:
        print(emit(name, length))


if __name__ == "__main__":
    name, size, output = parse_args()
    fsm(name, size, output)
