from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    points = models.IntegerField(default=0)
    lottery = models.IntegerField(default=0)
    STM = models.IntegerField(default=0)                                #意法
    Yahoo = models.IntegerField(default=0)
    ASML = models.IntegerField(default=0)
    NXP = models.IntegerField(default=0)
    Hsinchu = models.IntegerField(default=0)                           #中華電信
    Kronos = models.IntegerField(default=0)
    Cathay = models.IntegerField(default=0)                             #國泰
    CTBC = models.IntegerField(default=0)                               #中信金控
    Line = models.IntegerField(default=0)
    tsmc = models.IntegerField(default=0)
    a104 = models.IntegerField(default=0)
    Pixart = models.IntegerField(default=0)

    def __str__(self):
        return self.uid

import random
# random_string = str(random.randint(100000, 999999))
class TSMC(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class CTBC(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class STM(models.Model):
    password = models.CharField(max_length=10,null=False,default='')
   
class ASML(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class NXP(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class PixArt(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class Kronos(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class Cathay(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class LINE(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class Yahoo(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class onezerofour(models.Model):
    password = models.CharField(max_length=10,null=False,default='')

class Hsinchu(models.Model):
    password = models.CharField(max_length=10,null=False,default='')