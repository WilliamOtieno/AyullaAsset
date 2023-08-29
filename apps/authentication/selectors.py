from ..core.models import ReferralCode


def get_referral_code(code: str) -> ReferralCode | None:
    try:
        ref = ReferralCode.objects.get(code=code)
        return ref
    except ReferralCode.DoesNotExist:
        return None

