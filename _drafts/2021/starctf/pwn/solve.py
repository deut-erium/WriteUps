from z3 import *

a1 = BitVec('a1', 64)

def constraints(val):
    v1 = a1^(a1<<7)
    v3 = v1 ^ LShR(v1,0xb)
    v5 = v3 ^ (v3<<0x1f)
    return v5^LShR(v5,0xd)==val

def hash(n):
    # int64_t x8_1 = arg1 ^ (arg1 << 7)
    # int64_t x8_3 = x8_1 ^ (x8_1 u>> 0xb)
    # int64_t x8_5 = x8_3 ^ (x8_3 << 0x1f)
    # return x8_5 ^ (x8_5 u>> 0xd)
    mask = 0xffffffffffffffff
    a1 = n^((n<<7)&mask)
    a3 = a1 ^ ((a1>>0xb)&mask)
    a5 = a3 ^ ((a3<<0x1f)&mask)
    return a5^((a5>>0xd)&mask)

def reverse_hash(val):
    s = Solver()
    s.add(constraints(val))
    s.check()
    value = s.model()[a1].as_long()
    assert(hash(value)==val)
    return value

def get_models(constraints, num_models: int, var_list=None) -> list:
    models, results = [], []
    solver = Solver()
    solver.add(constraints)
    solver.push()
    while len(models) < num_models and solver.check() == sat:
        try:
            model = solver.model()
            if var_list:
                result = [model[var].as_long() for var in var_list]
                print(result)
                results.append(result)
            models.append(model)
            block = []
            for declaration in model:
                c = declaration()
                block.append(c != model[declaration])
            solver.add(Or(block))
            solver.push()
        except KeyboardInterrupt:
            print("interrupted")
            break
    if var_list:
        return results
    return models

def hash(n):
    # int64_t x8_1 = arg1 ^ (arg1 << 7)
    # int64_t x8_3 = x8_1 ^ (x8_1 u>> 0xb)
    # int64_t x8_5 = x8_3 ^ (x8_3 << 0x1f)
    # return x8_5 ^ (x8_5 u>> 0xd)
    mask = 0xffffffffffffffff
    a1 = n^((n<<7)&mask)
    a3 = a1 ^ ((a1>>0xb)&mask)
    a5 = a3 ^ ((a3<<0x1f)&mask)
    return a5^((a5>>0xd)&mask)

get_models(constraints(hash(100)),1000,[a1])

