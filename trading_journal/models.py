from django.db import models
from account.models import User

class TradingJournal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.DateField()
    content_1M = models.TextField(null=True, blank=True)
    content_1W = models.TextField(null=True, blank=True)
    content_1D = models.TextField(null=True, blank=True)
    content_4H = models.TextField(null=True, blank=True)
    content_1H = models.TextField(null=True, blank=True)
    content_15m = models.TextField(null=True, blank=True)

    img_1M = models.ImageField(upload_to='image/',null=True, blank=True)
    img_1W = models.ImageField(upload_to='image/',null=True, blank=True)
    img_1D = models.ImageField(upload_to='image/',null=True, blank=True)
    img_4H = models.ImageField(upload_to='image/',null=True, blank=True)
    img_1H = models.ImageField(upload_to='image/',null=True, blank=True)
    img_15m = models.ImageField(upload_to='image/',null=True, blank=True)

    transaction_content = models.TextField(null=True,blank=True)
    tp = models.TextField(null=True,blank=True)
    sl = models.TextField(null=True,blank=True)
    amount = models.TextField(null=True,blank=True)

    create_date = models.DateTimeField()

