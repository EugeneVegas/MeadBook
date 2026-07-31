from django.test import SimpleTestCase
from brewery.utils.unit_conversion import (
    sg_to_brix, brix_to_sg, brix_to_sg_corrected
)


class UnitConversionTestCase(SimpleTestCase):

    def test_sg_to_brix_matrix(self):
        """Test multiple Specific Gravity to Brix."""
        test_cases = [
            (1.000, 0.0),
            (1.040, 9.98),
            (1.101, 23.96),
        ]
        for sg_val, expected_brix in test_cases:
            with self.subTest(sg=sg_val):
                self.assertAlmostEqual(sg_to_brix(sg_val), expected_brix, 1)

    def test_brix_to_sg_matrix(self):
        """Test multiple Brix to Specific Gravity."""
        test_cases = [
            (0.0, 1.000),
            (10.0, 1.040),
            (24.0, 1.101),
        ]
        for brix_val, expected_sg in test_cases:
            with self.subTest(brix=brix_val):
                self.assertAlmostEqual(brix_to_sg(brix_val), expected_sg, 3)

    def test_corrected_refractometer_matrix(self):
        """Test the calculation for refractometer correction."""
        test_cases = [
            # format: (og_brix, current_brix, expected_corrected_sg)
            (24, 18, 1.057),
            (24, 10, 1.006),
            (24, 24, 1.094),
        ]
        for og, curr, expected in test_cases:
            with self.subTest(og=og, curr=curr):
                self.assertAlmostEqual(
                    brix_to_sg_corrected(og, curr), expected)

    def test_corrected_refractometer_with_wcf_matrix(self):
        """Test the calculation for refractometer correction with the wort
            correction factor."""
        test_cases = [
            # format: (og_brix, current_brix, wcf, expected_corrected_sg)
            (24, 18, 1.1, 1.051),
            (24, 18, 1.5, 1.038),
            (24, 10, 1.1, 1.006),
            (24, 10, 1.5, 1.004),
            (24, 24, 1.1, 1.086),
            (24, 24, 1.5, 1.063),
        ]
        for og, curr, wcf, expected in test_cases:
            with self.subTest(og=og, curr=curr, wcf=wcf):
                self.assertAlmostEqual(
                    brix_to_sg_corrected(og, curr, wcf), expected)
