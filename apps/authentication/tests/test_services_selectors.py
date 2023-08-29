from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from ..selectors import get_referral_code
from ..services import award_referee
from ...core.models import ReferralCode


class ServicesTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test.user', password=get_random_string(12))
        self.referral_code = ReferralCode.objects.create(user=self.user, code="TESTCODE")

    def test_get_referral_code_exists(self):
        code = "TESTCODE"
        referral = get_referral_code(code)
        self.assertIsNotNone(referral)
        self.assertEqual(referral.code, code)

    def test_get_referral_code_not_exists(self):
        code = "NONEXISTENTCODE"
        referral = get_referral_code(code)
        self.assertIsNone(referral)

    def test_award_referee_with_valid_code(self):
        initial_points = self.referral_code.points
        code = self.referral_code.code

        award_referee(code)
        self.referral_code.refresh_from_db()

        self.assertEqual(self.referral_code.points, initial_points + 5)

    def test_award_referee_with_invalid_code(self):
        code = "INVALIDCODE"

        award_referee(code)  # This should not raise an error since the code is invalid

