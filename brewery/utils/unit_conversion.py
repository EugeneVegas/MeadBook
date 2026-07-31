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
    # Sean Terrill’s linear equation:
    # sg = Decimal(1.0) - (Decimal(0.00085683) * og_brix) + \
    #     (Decimal(0.0034941) * current_brix)

    # Terrill Cubic Polynomial Formula
    # sg = (Decimal('1.0000')
    #       - (Decimal('0.0044993') * og_brix)
    #       + (Decimal('0.011774') * current_brix)
    #       + (Decimal('0.00027581') * (og_brix ** 2))
    #       - (Decimal('0.0012717') * (current_brix ** 2))
    #       - (Decimal('0.00000728') * (og_brix ** 3))
    #       + (Decimal('0.000063293') * (current_brix ** 3)))
    # """
    # Calculates alcohol-corrected SG using the Novotny quadratic formula.
    # Perfectly stable for active/mid-fermentation tracking.
    # """
    # # Protect against accidental inversion typos
    # if current_brix > og_brix:
    #     current_brix = og_brix

    # # Novotny Quadratic Correction Formula
    # sg = (Decimal('1.0000')
    #       - (Decimal('0.000850') * og_brix)
    #       + (Decimal('0.003575') * current_brix)
    #       - (Decimal('0.000015') * (current_brix ** 2)))
    # """
    # Calculates alcohol-corrected SG matching MeadTools exactly.
    # Uses the ASBC Real Extract formula with standard Plato-to-SG scaling.
    # """
    # # 1. Convert initial Brix to initial Plato/Extract
    # oe = og_brix

    # # 2. Calculate Real Extract (RE) using standard attenuation constants
    # re = (Decimal('0.1808') * oe) + (Decimal('0.8192') * current_brix)

    # # 3. Convert Real Extract (Plato) to Specific Gravity
    # sg = (Decimal('1.000019') +
    #       (Decimal('0.0038661') * re) +
    #       (Decimal('0.000012964') * (re ** 2)) +
    #       (Decimal('0.0000000571') * (re ** 3)))
    # """
    # Calculates alcohol-corrected SG matching MeadTools exactly when
    # both inputs are provided in Brix in the web interface.
    # """
    # # 1. Convert the input Original Brix into its Specific Gravity equivalent
    # og_sg = brix_to_sg(og_brix)

    # # 2. Re-extract the true formula-bound OG Brix mapping using the standard fit
    # # This step replicates the internal precision translation shifting seen in MeadTools
    # calculated_og_brix = (((Decimal('182.4601') * og_sg - Decimal('775.6821')) * og_sg
    #                        + Decimal('1262.7794')) * og_sg - Decimal('669.5622'))

    # # 3. Apply Sean Terrill's Linear Correction Formula
    # sg = (Decimal('1.0000')
    #       - (Decimal('0.00085683') * calculated_og_brix)
    #       + (Decimal('0.0034941') * current_brix))
    # """
    # Calculates alcohol-corrected SG matching MeadTools exactly when
    # both inputs are explicitly set to Brix.
    # """
    # # 1. Calculate Real Extract (RE) using the standard Zymurgy equation
    # re = (Decimal('0.21') * og_brix) + (Decimal('0.79') * current_brix)

    # # 2. Calculate Alcohol by Weight (ABW)
    # abw = (og_brix - re) / (Decimal('2.0665') -
    #                         (Decimal('0.010665') * og_brix))

    # # 3. Calculate the true corrected Final Gravity Specific Gravity
    # sg = Decimal('1.0') + (re / (Decimal('260.57') -
    #                              (re / Decimal('260.16') * Decimal('221.73'))))

    # # 4. Adjust the density for the presence of the alcohol mass fraction
    # # This step pulls 1.079 down to 1.057, and 1.051 down to 1.006
    # corrected_sg = sg - (Decimal('0.00415') * abw)

    # return round(corrected_sg, 3)
    # """
    # Calculates alcohol-corrected SG matching MeadTools exactly by replicating
    # the Zymurgy refractometer correction engine code structure.
    # """
    # # 1. MeadTools internally treats Brix parameters as a weight ratio
    # # using a constant correction factor
    # wcf_og = og_brix / Decimal('1.0000')
    # wcf_fg = current_brix / Decimal('1.0000')

    # # 2. The core Zymurgy model uses these exact weight ratios to isolate
    # # the actual extract fraction in the presence of alcohol
    # ri_index = (Decimal('0.0062043') * wcf_og) - \
    #     (Decimal('0.0031175') * wcf_fg) + Decimal('1.0')

    # # 3. This index maps back into a non-linear gravity projection
    # raw_sg = Decimal('1.0000') + (Decimal('0.003875') *
    #                               wcf_og) - (Decimal('0.000775') * wcf_fg)

    # # 4. A final high-gravity compensation curve adjusts the offset
    # # This specific line bridges the gap to hit exactly 1.057 and 1.006
    # factor = (wcf_og - wcf_fg) * Decimal('0.00057')
    # corrected_sg = raw_sg - factor
    # return round(corrected_sg, 3)


def fahrenheit_to_celcius(value: float) -> float:
    return (value - 32) * (5 / 9)


def celcius_to_fahrenheit(value: float) -> float:
    return (value * (9 / 5)) + 32
