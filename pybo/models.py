from django.db import models
#from account.models import Crypto

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

#class TradeHistory(models.Model):
#    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
#    symbol = models.CharField(max_length=100)
#    open_time = models.DateTimeField()
#    open_timestamp = models.PositiveBigIntegerField()
#    close_time = models.DateTimeField()
#    close_timestamp = models.PositiveBigIntegerField()
#    side = models.CharField(max_length=10)
#    leverage = models.IntegerField(null=True,blank=True)
#    open_amount = models.FloatField()
#    close_amount = models.FloatField()
#    open_price = models.FloatField()
#    close_price = models.FloatField()
#    open_cost = models.FloatField()
#    close_cost = models.FloatField()
#    tp = models.FloatField(null=True,blank=True)
#    sl = models.FloatField(null=True,blank=True)
#    open_commission_fee = models.FloatField()
#    close_commission_fee = models.FloatField()
#    funding_fee = models.FloatField()
#    insurance_clear = models.FloatField()
#    realized_pnl = models.FloatField()
#    pnl = models.FloatField()
#    pnl_percentage = models.FloatField()
#    open_balance = models.FloatField()
#    close_balance = models.FloatField()
