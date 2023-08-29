from django.db import models
from django.contrib.auth.models import User


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-updated_at', )


class ReferralCode(TimestampModel): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True, db_index=True)
    points = models.IntegerField(default=0)


class Referral(TimestampModel):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inviter")
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitee")
    code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.inviter}: {self.code.code}"


class PortfolioCoin(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_id = models.CharField(max_length=32)

