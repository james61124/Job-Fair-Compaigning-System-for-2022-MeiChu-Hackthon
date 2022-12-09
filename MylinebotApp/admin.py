from django.contrib import admin

# Register your models here.
from MylinebotApp.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','name','pic_url','mtext','mdt','lottery','points','STM','Yahoo','ASML','NXP','Hsinchu','Kronos','Cathay','CTBC','Line','tsmc','a104','Pixart')
    #list_display = ('uid','name','pic_url','mtext','mdt','points','lottery')
admin.site.register(User_Info,User_Info_Admin)

class TSMC_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(TSMC,TSMC_Admin)

class CTBC_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(CTBC,CTBC_Admin)

class STM_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(STM,STM_Admin)

class ASML_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(ASML,ASML_Admin)

class NXP_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(NXP,NXP_Admin)

class PixArt_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(PixArt,PixArt_Admin)

class Kronos_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(Kronos,Kronos_Admin)

class Cathay_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(Cathay,Cathay_Admin)

class LINE_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(LINE,LINE_Admin)

class Yahoo_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(Yahoo,Yahoo_Admin)

class onezerofour_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(onezerofour,onezerofour_Admin)

class Hsinchu_Admin(admin.ModelAdmin):
    list_display = ['password']
admin.site.register(Hsinchu,Hsinchu_Admin)