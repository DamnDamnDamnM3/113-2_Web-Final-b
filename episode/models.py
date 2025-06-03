from django.db import models
from django.db.models import IntegerField
from django.db.models.functions import Cast

# Create your models here.
  
class Season(models.Model):
    season_number = models.IntegerField() # 第幾季
    description = models.TextField(max_length=1500) # 該季主要劇情描述
    img = models.ImageField(upload_to='uploaded_img', null=True)

    def __str__(self):
      #  d = self.description[0,20]
      return f"Season {self.season_number}: {self.description}"         

class Episode(models.Model):

    season = models.ForeignKey(Season, models.CASCADE) # 所連接的季
    ep_number = models.IntegerField() # 第幾集
    ep_title = models.CharField(max_length=255) # 集標題
    eng_plot = models.TextField(null=True, max_length=2000) # 該集英文描述
    tw_plot = models.TextField(null=True, max_length=2000) # 該集中文描述


    def next(self):
        # Find next episode in the same season
        try:
            next_ep_number = self.ep_number + 1
            return Episode.objects.get(season=self.season, ep_number=next_ep_number)
        except Episode.DoesNotExist:
            pass
        
        try:
            next_season = Season.objects.get(pk=self.season.pk + 1)
            return Episode.objects.filter(season=next_season).order_by('ep_number').first()
        except Season.DoesNotExist:
            return None

    def prev(self):
        # Find previous episode in the same season
        try:
            prev_ep_number = self.ep_number - 1
            return Episode.objects.get(season=self.season, ep_number=prev_ep_number)
        except Episode.DoesNotExist:
            pass

        # Find last episode of the previous season
        try:
            prev_season = Season.objects.get(pk=self.season.pk - 1)
            count = Episode.objects.filter(season=prev_season).count()
            return Episode.objects.get(season=prev_season, ep_number=count)
        except Season.DoesNotExist:
            return None
        
    def __str__(self):
      # 例如：EP1-1: Pilot
      return f"EP{self.season.season_number}-{self.ep_number}: {self.ep_title}"  

class Cast (models.Model):
    GENDER_TYPE = [
        ('M', 'Male'), 
        ('F', 'Female')
    ]
    name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=250)
    introduction = models.TextField(max_length=2000)
    gender = models.CharField(null=True, choices=GENDER_TYPE, 
                              max_length=10)
    born_year = models.IntegerField(null=True)

    def __str__(self):
      return (self.name)