import sys

BUILDINGS = {
    "T": {"build_time": 5, "earning": 1500},
    "P": {"build_time": 4, "earning": 1000},
    "C": {"build_time": 10, "earning": 2000},
}
NAMES = ["T", "P", "C"]


def max_profit(n):
    """Find the most money that can be earned in n units of time.

    Properties are built one at a time. A finished property earns its
    rate for every unit of time left until n.

    Returns a pair: the max earnings, and a list of every (T, P, C)
    count that reaches it, largest first.
    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("Time units cannot be negative")

    best = [0] * (n + 1)
    mixes = [[(0, 0, 0)] for _ in range(n + 1)]


    for t in range(1, n + 1):
        for index, name in enumerate(NAMES):
            build_time = BUILDINGS[name]["build_time"]
            earning = BUILDINGS[name]["earning"]

            if build_time >= t:
                continue

            time_left = t - build_time
            total = earning * time_left + best[time_left]

            if total > best[t]:
                best[t] = total
                mixes[t] = []

            if total == best[t]:
                for mix in mixes[time_left]:
                    new_mix = list(mix)
                    new_mix[index] += 1
                    new_mix = tuple(new_mix)
                    if new_mix not in mixes[t]:
                        mixes[t].append(new_mix)


    return best[n], sorted(mixes[n], reverse=True)


def format_result(n, earnings, mixes):
    """Turn the result into the text printed by the program.

    Example for n = 7:
        Time Unit: 7
        Earnings: $3000
        Solutions
        1. T: 1 P: 0 C: 0
        2. T: 0 P: 1 C: 0
    """
    lines = [f"Time Unit: {n}", f"Earnings: ${earnings}", "Solutions"]
    for number, (t, p, c) in enumerate(mixes, start=1):
        lines.append(f"{number}. T: {t} P: {p} C: {c}")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python3 max_profit.py <time_units>")
        sys.exit(1)

    n = int(sys.argv[1])
    earnings, mixes = max_profit(n)
    print(format_result(n, earnings, mixes))


if __name__ == "__main__":
    main()
