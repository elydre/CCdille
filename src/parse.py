from src.tools import fatal_error

def parse_func(asts):
    if len(asts) < 4:
        fatal_error(f"Unexpected end of asts {asts}")
    if isinstance(asts[0], list):
        fatal_error("Unexpected list in asts")
    if asts[0][0] != "name":
        fatal_error(f"Unexpected ast type: {asts[0][0]}")

    name = asts[0][1]

    if not isinstance(asts[1], list):
        fatal_error("Expected list after func name")

    params = []
    i = 0
    while i < len(asts[1]):
        arg = {"name": ""}
        e = asts[1][i]
        if isinstance(e, list):
            fatal_error("Unexpected list in asts")
        if e[0] != "name":
            fatal_error(f"Unexpected ast type: {e[0]}")
        arg["type"] = e[1]
        i += 1
        if i >= len(asts[1]):
            params.append(arg)
            break
        e = asts[1][i]
        if isinstance(e, list):
            fatal_error("Unexpected list in asts")
        if e[0] == "punct" and e[1] == ",":
            params.append(arg)
            i += 1
            continue
        if e[0] != "name":
            fatal_error(f"Unexpected ast type: {e[0]}")
        arg["name"] = e[1]
        params.append(arg)
        i += 1
        if i >= len(asts[1]):
            break
        e = asts[1][i]
        if isinstance(e, list):
            fatal_error("Unexpected list in asts")
        if e[0] != "punct" or e[1] != ",":
            fatal_error(f"Expected "," but got {e}")
        i += 1

    if isinstance(asts[2], list):
        fatal_error("Unexpected list in asts")
    if asts[2][0] != "name":
        fatal_error(f"Unexpected ast type: {asts[2][0]}")

    if isinstance(asts[3], list):
        fatal_error("Unexpected list in asts")
    if asts[3][0] == "punct":
        if asts[3][1] == ";":
            return {
                "type": "funcproto",
                "name": name,
                "params": params,
                "return": asts[2][1],
            }, 4
        elif asts[3][1] == "{":
            end = 4
            while end < len(asts):
                if isinstance(asts[end], list):
                    end += 1
                    continue
                if asts[end][0] == "punct" and asts[end][1] == "}":
                    return {
                        "type": "func",
                        "name": name,
                        "params": params,
                        "return": asts[2][1],
                        "body": parse(asts[4:end]),
                    }, end
                end += 1
            fatal_error("Unexpected end of asts")
        else:
            fatal_error(f"Unexpected punct: {asts[3][1]}")
    else:
        fatal_error(f"Unexpected ast: {asts[3]}")

def parse(asts):
    ret = []
    i = 0
    while i < len(asts):
        ast = asts[i]
        if isinstance(ast, list):
            fatal_error("Unexpected list in asts")
        if ast[0] != "name":
            i += 1
            continue
        if ast[1] == "func":
            tmp, a = parse_func(asts[i + 1:])
            ret.append(tmp)
            i += a
        else:
            fatal_error(f"Unexpected ast: {ast}")
        i += 1
    return ret
