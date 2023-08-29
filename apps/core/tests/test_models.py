from django.test import TestCase
from django.utils.crypto import get_random_string
from ..models import PortfolioCoin, ReferralCode, User, Referral


class TestReferralCode(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test.user",
            password=get_random_string(12)
        )
        self.referral_code = ReferralCode.objects.create(
            user=self.user, 
            code='qwerty'
        )
        self.user1 = User.objects.create_user(
            username="test.user.1",
            password=get_random_string(12)
        )

    def test_referral_code_creation(self):
        self.assertIsInstance(self.referral_code.points, int)
        self.assertEqual(self.referral_code.points, 0)

    def test_referral_code_unique(self):
        with self.assertRaises(Exception):
            ReferralCode.objects.create(user=self.user1, code='qwerty')


class TestReferral(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test.user",
            password=get_random_string(12)
        )
        self.user1 = User.objects.create_user(
            username="test.user.1",
            password=get_random_string(12)
        )
        self.referral_code = ReferralCode.objects.create(user=self.user, code='qwerty')


    def test_referral_creation(self):
        referral = Referral.objects.create(inviter=self.user, invitee=self.user1, code=self.referral_code)
        self.assertEqual(referral.__str__(), f"{self.user}: qwerty")


class TestPortfolioCoin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test.user', password=get_random_string(12))

    def test_portfolio_coin_creation(self):
        portfolio_coin = PortfolioCoin.objects.create(user=self.user, coin_id='bitcoin')
        self.assertEqual(portfolio_coin.user, self.user)
        self.assertEqual(portfolio_coin.coin_id, 'bitcoin')
        self.assertIsInstance(portfolio_coin.coin_id, str)

    def test_cascade_delete(self):
        PortfolioCoin.objects.create(user=self.user, coin_id='bitcoin')
        self.user.delete()
        with self.assertRaises(PortfolioCoin.DoesNotExist):
            PortfolioCoin.objects.get(user=self.user)

