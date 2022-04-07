from django.db import models
from datetime import date
# Create your models here.

class ITBoard(models.Model):
    TeaserID = models.IntegerField(verbose_name="번호", primary_key=True)
    Title = models.CharField(max_length=50, verbose_name="제목")
    AccID = models.CharField(max_length=15, verbose_name="작성자")
    Date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    Clicked = models.IntegerField(verbose_name="조회수")

    class Meta:
        db_table = 'brainTeaser'

    def __str__(self):
        return '{} : {} :: {} : {} : {}'.format(self.TeaserID,self.Title,self.AccID,self.Date.date(),self.Clicked)

