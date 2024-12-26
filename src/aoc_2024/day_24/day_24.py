from common.input import get_data_file, get_lines

EXAMPLE_SHORT = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

EXAMPLE_LONG = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

EXAMPLE_AND = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""

FUNCTIONS = {"OR": lambda a, b: a | b, "AND": lambda a, b: a & b, "XOR": lambda a, b: a ^ b}

GateInput = tuple[str, str, str]
Gates = dict[str, GateInput]


def gate_input(left: str, operation: str, right: str) -> GateInput:
    inputs = sorted([left, right])
    return inputs[0], operation, inputs[1]


def load_input(data: str) -> tuple[dict[str, int], Gates]:
    lines = get_lines(data)
    wires = {}
    gates = {}
    for line in lines:
        if ":" in line:
            wire, value = line.split(":")
            wires[wire] = int(value)
        elif "->" in line:
            left, operation, right, _, output = line.split(" ")
            gates[output] = gate_input(left, operation, right)
    return wires, gates


def do_calculation(wires: dict[str, int], gates: Gates) -> int:
    z = 0
    done = False
    while not done:
        done = True
        for output, calculation in gates.items():
            left, operation, right = calculation
            if left in wires and right in wires and output not in wires:
                op = FUNCTIONS[operation]
                wires[output] = op(wires[left], wires[right])
                done = False
                if wires[output] and output[0] == "z":
                    bit = int(output[1:])
                    z += 2 ** bit

    return z


def simulate_system(data: str) -> int:
    wires, gates = load_input(data)
    return do_calculation(wires, gates)


"""
Full Adder with Ripple Carry
(Half Adder at bit0)

x00  ----,--,  (SumXor)
         |  |--> XOR ----------------------------------------> z00
y00  -,--|--'
      |  |
      |  '--,  (CarryOut)
      |     |--> AND ----,--, 
      '-----'            |  |
                         |  '---,  (ZOut)
x01  ---,-,  (SumXor)    |      |----> XOR ------------------> z01
        | |--> XOR ---,--|------'
y01  -,-|-'           |  |
      | '-, (SumAnd)  |  '------,  (CarryAnd)
      |   |--> AND -, |         |----> AND -,
      '---'         | '---------'           | (CarryOut)
                    |                       |--> OR --,
                    '-----------------------'         |
                         ,--,-------------------------'
                         |  '---,  (ZOut)
x02  ---,-,  (SumXor)    |      |----> XOR ------------------> z02
        | |--> XOR ---,--|------'
y02  -,-|-'           |  |
      | '-, (SumAnd)  |  '------,  (CarryAnd)
      |   |--> AND -, |         |----> AND -,
      '---'         | '---------'           | (CarryOut)
                    |                       |--> OR --,
                    '-----------------------'         |
                                                     ...
                         ,--,-------------------------'
                         |  '---,  (ZOut)
xnn  ---,-,  (SumXor)    |      |----> XOR ------------------> znn
        | |--> XOR ---,--|------'
ynn  -,-|-'           |  |
      | '-, (SumAnd)  |  '------,  (CarryAnd)
      |   |--> AND -, |         |----> AND -,
      '---'         | '---------'           | (CarryOut)
                    |                       |--> OR ---------> znn+1
                    '-----------------------'         
"""


def get_bit_ids(ids: str | tuple, bit: int) -> tuple | str:
    result = []
    ids = [ids] if isinstance(ids, str) else ids
    for id in ids:
        result.append(f"{id}{bit:02}")
    return result[0] if len(result) == 1 else tuple(result)


def build_simple_and(input_bits: int):
    result = {}
    for bit in range(input_bits):
        x, y, z = get_bit_ids(("x", "y", "z"), bit)
        result[z] = gate_input(x, "AND", y)
    return result


def build_full_adder_with_ripple(input_bits: int):
    result = {}
    for bit in range(input_bits):
        carry_id = get_bit_ids("co", bit - 1)
        bit_ids = get_bit_ids(("x", "y", "z", "sx", "sa", "ca", "co"), bit)
        x, y, z, sxor, sand, cand, cout = bit_ids

        sum_xor = gate_input(x, "XOR", y)
        sum_and = gate_input(x, "AND", y)

        car_xor = gate_input(sxor, "XOR", carry_id)
        car_and = gate_input(sxor, "AND", carry_id)
        car_or = gate_input(sand, "OR", cand)

        if bit == 0:
            result[z] = sum_xor
            result[cout] = sum_and
        else:
            result[sxor] = sum_xor
            result[z] = car_xor
            result[cand] = car_and
            result[sand] = sum_and
            if bit + 1 == input_bits:
                cout = get_bit_ids("z", bit + 1)
            result[cout] = car_or
    return result


def swap_outputs(mapping: dict[str, str], gates: Gates, swapped: set, key_a: str, key_b: str):
    input_a = gates[key_a]
    gates[key_a] = gates[key_b]
    gates[key_b] = input_a
    swapped.add(key_a)
    swapped.add(key_b)

    a_mapping = [k for k, v in mapping.items() if v == key_a]
    b_mapping = [k for k, v in mapping.items() if v == key_b]
    if a_mapping:
        mapping[a_mapping[0]] = key_b
    if b_mapping:
        mapping[b_mapping[0]] = key_a


def find_swaps(correct: Gates, incorrect: Gates, mapping: dict[str, str], swapped: set):
    done = False
    while not done:
        done = True
        for output, input in correct.items():
            if output in mapping:
                continue
            a_in, op, b_in = input
            if a_in not in mapping or b_in not in mapping:
                continue

            a = mapping.get(a_in)
            b = mapping.get(b_in)
            search = gate_input(a, op, b)
            match = [o for o, g in incorrect.items() if g == search]
            if match and (output[0] != "z" or output == match[0]):
                mapping[output] = match[0]
                done = False
            elif match:
                swap_outputs(mapping, incorrect, swapped, output, match[0])
                done = False
            else:
                match_a = [o for o, g in incorrect.items() if g[1] == op and a in {g[0], g[2]}]
                match_b = [o for o, g in incorrect.items() if g[1] == op and b in {g[0], g[2]}]
                wrong = None
                right = None
                if match_a and not match_b:
                    candidate = incorrect[match_a[0]]
                    wrong = b
                    ca, cop, cb = candidate
                    right = ca if cb == a else cb
                elif match_b and not match_a:
                    candidate = incorrect[match_b[0]]
                    wrong = a
                    ca, cop, cb = candidate
                    right = ca if cb == b else cb
                if wrong and right:
                    swap_outputs(mapping, incorrect, swapped, wrong, right)
                    done = False


def find_swapped_outputs(data: str, adder: bool = True) -> str:
    wires, gates = load_input(data)

    input_bits = sum(1 for wire in wires if wire[0] == "x")
    adder_gates = build_full_adder_with_ripple(input_bits) if adder else build_simple_and(input_bits)

    swapped = set()
    input_map = ({f"x{b:02}": f"x{b:02}" for b in range(input_bits)} |
                 {f"y{b:02}": f"y{b:02}" for b in range(input_bits)})
    find_swaps(adder_gates, gates, input_map, swapped)
    return ",".join(sorted(list(swapped)))


def main(year: int, day: int, example: bool, part_b: bool) -> any:
    if example:
        if not part_b:
            short = simulate_system(EXAMPLE_SHORT)
            long = simulate_system(EXAMPLE_LONG)
            return short, long
        else:
            return find_swapped_outputs(EXAMPLE_AND, False)
    else:
        source = get_data_file(year, day)
        return find_swapped_outputs(source) if part_b else simulate_system(source)
