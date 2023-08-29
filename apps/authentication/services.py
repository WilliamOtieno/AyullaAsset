from .selectors import get_referral_code


def award_referee(code):
    ref_obj = get_referral_code(code)
    if ref_obj is not None:
        ref_obj.points += 5
        ref_obj.save()
