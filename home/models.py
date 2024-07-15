from django.db import models

class EconomicCalendar(models.Model):
    scheduled_time = models.DateTimeField()
    contents = models.CharField(max_length=100)

    def __str__(self):
        return self.subject

class News(models.Model):
    post_date = models.DateTimeField()
    news_link = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100)
    img_link = models.CharField(max_length=100)

    def __str__(self):
        return self.subject
