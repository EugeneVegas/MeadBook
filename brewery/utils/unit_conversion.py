def sg_to_brix(value):
    bx = 263.663 - 263.806 / value
    return round(bx, 3)


def brix_to_sg(value):
    sg = value / (258.6 - (value / 258.2 * 227.1)) + 1
    return round(sg, 3)


def fahrenheit_to_celcius(value):
    return (value - 32) * (5 / 9)


def celcius_to_fahrenheit(value):
    return (value * (9 / 5)) + 32
