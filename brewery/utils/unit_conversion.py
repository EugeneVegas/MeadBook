def sg_to_brix(value: float) -> float:
    bx = (((182.4601 * value - 775.6821) *
          value + 1262.7794) * value - 669.5622)
    return round(bx, 3)


def brix_to_sg(value: float) -> float:
    sg = value / (258.6 - (value / 258.2
                  * 227.1)) + 1
    return round(sg, 3)


def brix_to_sg_corrected(og_brix: float, current_brix: float,
                         wcf: float = 1.0) -> float:
    # Peter Novotný
    fg = -0.002349 * (og_brix / wcf) + 0.006276 * (current_brix / wcf) + 1
    return round(fg, 3)


def fahrenheit_to_celcius(value: float) -> float:
    return (value - 32) * (5 / 9)


def celcius_to_fahrenheit(value: float) -> float:
    return (value * (9 / 5)) + 32
