from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from ..models import Referral, PortfolioCoin, ReferralCode
from ..selectors import get_user_referrals, get_user_coins, get_total_referral_bonus

class CoreSelectorsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test.user', password=get_random_string(12))
        self.user1 = User.objects.create_user(username='test.user.1', password=get_random_string(12))
        self.user2 = User.objects.create_user(username='test.user.2', password=get_random_string(12))
        self.referral_code = ReferralCode.objects.create(user=self.user, code="qwerty")

    def test_get_user_referrals(self):
        # Create test referrals for the user
        Referral.objects.create(inviter=self.user, invitee=self.user1, code=self.referral_code)
        Referral.objects.create(inviter=self.user, invitee=self.user2, code=self.referral_code)

        referrals = get_user_referrals(self.user)

        self.assertEqual(len(referrals), 2)
        self.assertEqual(referrals[0].inviter, self.user)
        self.assertEqual(referrals[1].invitee, self.user1)

    def test_get_user_coins(self):
        # Create a test portfolio coin for the user
        PortfolioCoin.objects.create(user=self.user, coin_id="bitcoin")

        coins = get_user_coins(self.user)

        self.assertEqual(len(coins), 1)
        self.assertEqual(coins[0]['id'], "bitcoin")

    def test_get_total_referral_bonus(self):
        # Create test referral codes for the user
        ReferralCode.objects.create(user=self.user, points=50, code="sudo")
        ReferralCode.objects.create(user=self.user, points=100, code="uiop")
        
        total_bonus = get_total_referral_bonus(self.user)

        self.assertEqual(total_bonus, 150)

