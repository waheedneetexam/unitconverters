import math

def fmt(num):
    if math.isnan(num) or math.isinf(num): return "N/A"
    if num == 0: return "0"
    abs_n = abs(num)
    if abs_n > 0:
        sig = 10
        magnitude = math.floor(math.log10(abs_n))
        rounded = round(num, -int(magnitude) + sig - 1)
    else:
        rounded = num
    abs_r = abs(rounded)
    if abs_r < 0.000001 and abs_r > 0:
        decimals = max(0, -int(math.floor(math.log10(abs_r))) + 5)
        decimals = min(decimals, 20)
        return f"{rounded:.{decimals}f}".rstrip('0').rstrip('.')
    if abs_r >= 1000:
        if rounded == int(rounded):
            return f"{int(rounded):,}"
        decimals = max(0, sig - 1 - int(math.floor(math.log10(abs_r))))
        return f"{rounded:,.{decimals}f}".rstrip('0').rstrip('.')
    return f"{rounded:.10g}"

tests = [
    (1*1/1e-9,    "1,000,000,000"),
    (2*1/1e-9,    "2,000,000,000"),
    (5*1/1e-9,    "5,000,000,000"),
    (500*1/1e-9,  "500,000,000,000"),
    (1000*1/1e-9, "1,000,000,000,000"),
    (1e-9,        "0.000000001"),
    (1e-12,       "0.000000000001"),
    (3.78541,     "3.78541"),
    (1609.344,    "1,609.344"),
    (0.0254,      "0.0254"),
    (1609344,     "1,609,344"),
    (0.000001,    "0.000001"),
    (0.0000001,   "0.0000001"),
]

all_ok = True
for val, expected in tests:
    result = fmt(val)
    ok = result == expected
    if not ok:
        all_ok = False
    status = "OK" if ok else f"FAIL (expected: {expected})"
    print(f"{val} -> {result}  {status}")

print(f"\nAll OK: {all_ok}")
