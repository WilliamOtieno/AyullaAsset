from django.contrib.auth.models import User
from django.db.models import QuerySet
from .models import PortfolioCoin, Referral, ReferralCode
from .services import get_coin_info


def get_user_referrals(user: User) -> QuerySet[Referral]:
    return Referral.objects.select_related(
        "inviter", "invitee", "code"
    ).filter(inviter=user)


def get_user_coins(user: User) -> list:
    coin_ids = PortfolioCoin.objects.filter(
        user=user
    ).values_list("coin_id", flat=True)
    if len(coin_ids) < 1:
        return []
    coins = [get_coin_info(id) for id in coin_ids]
    return coins


def get_total_referral_bonus(user: User) -> int:
    points = 0
    objs = ReferralCode.objects.filter(user=user)
    for i in objs:
        points += i.points
    return points

