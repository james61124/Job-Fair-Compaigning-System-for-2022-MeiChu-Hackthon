from django.shortcuts import render
from MylinebotApp.models import *

#我自己加的
import random

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage #原本的
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


#解密碼函式
def anyToDecimal(num,n):
    baseStr = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
               "A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,
               "K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,
               "U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35}
    new_num = 0
    nNum = len(num) - 1
    for i in num:         
        new_num = new_num  + baseStr[i]*pow(n,nNum)
        nNum = nNum -1 
    return new_num
def secretnum(a):
    anyToDecimal(a,36)
    return (anyToDecimal(a,36) % 2022) #這裡可以拿到最後要的mod出來的值 2022要記得改掉

@csrf_exempt
def callback(request):
    print(request)
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                points=0

                message=[]
                #if event.message.text=='開始遊戲':
                if User_Info.objects.filter(uid=uid).exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,points=points)
                    #message.append(TextSendMessage(text='註冊成功'))
                    #else:
                        #message.append(TextSendMessage(text='已註冊'))
                elif event.message.text=='查看黑客松幣總額':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                    for user in user_info:
                        info = '\U0001F385你的黑客松幣=%s'%(user.points)
                        message.append(TextSendMessage(text=info))

                elif event.message.text=='確定兌換 Level 1 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    original_point=0
                    new_points=0
                    less_point=1200
                    for user in user_info:
                        new_points = user.points - less_point
                        original_point = user.points
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = '兌換完抽獎卷後，你的黑客松幣=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    flag = 0
                    for user in user_info:
                        if user.lottery==1:
                            flag=1
                            break
                    if flag==1:
                        info = '您已兌換過抽獎卷'
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=original_point) #修改回原本的
                        message.append(TextSendMessage(text=info)) #輸出
                    elif new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = '剩餘黑客松幣數=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(lottery=1) 
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311260763_104695532438140_8784150806900176898_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=730e14&_nc_ohc=OjkIHkMC6CcAX8XJTXM&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9-ieCIdJZU9v8Dn5ugfgFdUzZvV73KgBXvnh4bQH2ZOw&oe=63558337',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311260763_104695532438140_8784150806900176898_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=730e14&_nc_ohc=OjkIHkMC6CcAX8XJTXM&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9-ieCIdJZU9v8Dn5ugfgFdUzZvV73KgBXvnh4bQH2ZOw&oe=63558337'
                        )
                        message.append(image_message) #輸出抽獎卷 
                elif event.message.text=='確定兌換 Level 2 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    original_point=0
                    new_points=0
                    less_point=1900
                    for user in user_info:
                        new_points = user.points - less_point
                        original_point = user.points
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = '兌換完抽獎卷後，你的黑客松幣=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    flag = 0
                    for user in user_info:
                        if user.lottery==1:
                            flag=1
                            break
                    if flag==1:
                        info = '您已兌換過抽獎卷'
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=original_point) #修改回原本的
                        message.append(TextSendMessage(text=info)) #輸出
                    elif new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = '剩餘黑客松幣數=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(lottery=1) 
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311833481_104696019104758_5795713764810911910_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=730e14&_nc_ohc=GqQiiHt_WdQAX_jP7YF&tn=FKUeTQCsg2KYCGQ3&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9Z6mfTysnSXCrYiOK9DqABLG0UvKoNFLNB0ExbJ_e8pg&oe=6354D555',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311833481_104696019104758_5795713764810911910_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=730e14&_nc_ohc=GqQiiHt_WdQAX_jP7YF&tn=FKUeTQCsg2KYCGQ3&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9Z6mfTysnSXCrYiOK9DqABLG0UvKoNFLNB0ExbJ_e8pg&oe=6354D555'
                        )
                        message.append(image_message) #輸出抽獎卷
                elif event.message.text=='確定兌換 Level 3 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    original_point = 0
                    new_points=0
                    less_point=2500
                    for user in user_info:
                        new_points = user.points - less_point
                        original_point = user.points
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = '兌換完抽獎卷後，你的黑客松幣=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    flag = 0
                    for user in user_info:
                        if user.lottery==1:
                            flag=1
                            break
                    if flag==1:
                        info = '您已兌換過抽獎卷'
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=original_point) #修改回原本的
                        message.append(TextSendMessage(text=info)) #輸出
                    elif new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = '剩餘黑客松幣數=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(lottery=1) 
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311605785_104696382438055_2392417563507812056_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=730e14&_nc_ohc=kJvz63HCxEgAX-6LxvL&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9D3GR2ZPLGX_2AsDsUv1S4DShWn4PB9_aiTPB1taJ_JQ&oe=6355FB28',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/311605785_104696382438055_2392417563507812056_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=730e14&_nc_ohc=kJvz63HCxEgAX-6LxvL&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9D3GR2ZPLGX_2AsDsUv1S4DShWn4PB9_aiTPB1taJ_JQ&oe=6355FB28'
                        )
                        message.append(image_message) #輸出抽獎卷
                elif event.message.text=='輸出會員資料':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                    for user in user_info:
                        info = 'UID=%s\nNAME=%s\n大頭貼=%s\npoints=%s\n'%(user.uid,user.name,user.pic_url,user.points)
                        message.append(TextSendMessage(text=info))
                elif event.message.text=='增加點數':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    add_point=random.randrange(100,301,100)
                    for user in user_info:
                        new_points = user.points + add_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info))
                elif event.message.text=='刪除會員資料':
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).delete() #刪除
                elif ('LINE:'in event.message.text or 'line:'in event.message.text or 'Line:'in event.message.text or 'LINE：'in event.message.text or 'line：'in event.message.text or 'Line：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了LINE的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==36):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        line_info = LINE.objects.all()
                        for user in user_info:
                            flag = 0
                            for line in line_info:
                                if(x[1]==line.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Line==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                LINE.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Line=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('TSMC:'in event.message.text or 'tsmc:'in event.message.text or 'Tsmc:'in event.message.text or 'TSMC：'in event.message.text or 'tsmc：'in event.message.text or 'Tsmc：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了TSMC台積電的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==25):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        tsmc_info = TSMC.objects.all()
                        for user in user_info:
                            flag = 0
                            for tsmc in tsmc_info:
                                if(x[1]==tsmc.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.tsmc==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                TSMC.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(tsmc=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('STM:'in event.message.text or 'stm:'in event.message.text or 'Stm:'in event.message.text or 'STM：'in event.message.text or 'stm：'in event.message.text or 'Stm：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了意法半導體的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==34):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        stm_info = STM.objects.all()
                        for user in user_info:
                            flag = 0
                            for stm in stm_info:
                                if(x[1]==stm.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.STM==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                STM.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(STM=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))                    
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Yahoo:'in event.message.text or 'YAHOO:'in event.message.text or 'yahoo:'in event.message.text or 'Yahoo：'in event.message.text or 'YAHOO：'in event.message.text or 'yahoo：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了Yahoo的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==32):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        yahoo_info = Yahoo.objects.all()
                        for user in user_info:
                            flag = 0
                            for yahoo in yahoo_info:
                                if(x[1]==yahoo.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Yahoo==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                Yahoo.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Yahoo=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('ASML:'in event.message.text or 'asml:'in event.message.text or 'Asml:'in event.message.text or 'ASML：'in event.message.text or 'asml：'in event.message.text or 'Asml：'in event.message.text ):
                    message.append(TextSendMessage(text='輸入了ASML艾司摩爾的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==30):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        asml_info = ASML.objects.all()
                        for user in user_info:
                            flag = 0
                            for asml in asml_info:
                                if(x[1]==asml.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.ASML==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                ASML.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(ASML=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('NXP:'in event.message.text or 'nxp:'in event.message.text or 'Nxp:'in event.message.text or 'NXP：'in event.message.text or 'nxp：'in event.message.text or 'Nxp：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了恩智浦半導體的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==28):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        nxp_info = NXP.objects.all()
                        for user in user_info:
                            flag = 0
                            for nxp in nxp_info:
                                if(x[1]==nxp.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.NXP==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                NXP.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(NXP=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Hsinchu:'in event.message.text or 'HSINCHU:'in event.message.text or 'hsinchu:'in event.message.text or 'Hsinchu：'in event.message.text or 'HSINCHU：'in event.message.text or 'hsinchu：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了新竹市政府的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==26):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        hsinchu_info = Hsinchu.objects.all()
                        for user in user_info:
                            flag = 0
                            for hsinchu in hsinchu_info:
                                if(x[1]==hsinchu.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Hsinchu==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                Hsinchu.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Hsinchu=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Kronos:'in event.message.text or 'KRONOS:'in event.message.text or 'kronos:'in event.message.text or 'Kronos：'in event.message.text or 'KRONOS：'in event.message.text or 'kronos：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了Kronos Research麒點科技的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==24):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        kronos_info = Kronos.objects.all()
                        for user in user_info:
                            flag = 0
                            for kronos in kronos_info:
                                if(x[1]==kronos.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Kronos==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                Kronos.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Kronos=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Cathay:'in event.message.text or 'CATHAY:'in event.message.text or 'cathay:'in event.message.text or 'Cathay：'in event.message.text or 'CATHAY：'in event.message.text or 'cathay：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了國泰金控的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==22):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        cathay_info = Cathay.objects.all()
                        for user in user_info:
                            flag = 0
                            for cathay in cathay_info:
                                if(x[1]==cathay.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Cathay==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                Cathay.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Cathay=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('CTBC:'in event.message.text or 'ctbc:'in event.message.text or 'Ctbc:'in event.message.text or 'CTBC：'in event.message.text or 'ctbc：'in event.message.text or 'Ctbc：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了中國信託的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==20):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        ctbc_info = CTBC.objects.all()
                        for user in user_info:
                            flag = 0
                            for ctbc in ctbc_info:
                                if(x[1]==ctbc.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.CTBC==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                CTBC.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(CTBC=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('104:'in event.message.text or '104：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了一零四資訊科技的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==16):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                        onezerofour_info = onezerofour.objects.all() 
                        for user in user_info:
                            flag = 0
                            for onezerofour_ in onezerofour_info:
                                if(x[1]==onezerofour_.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.a104==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                onezerofour.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(a104=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('PixArt:'in event.message.text or 'PIXART:'in event.message.text or 'pixart:'in event.message.text or 'PixArt：'in event.message.text or 'PIXART：'in event.message.text or 'pixart：'in event.message.text):
                    message.append(TextSendMessage(text='輸入了原相科技的密碼'))
                    x = []
                    if ':' in event.message.text:
                        x = event.message.text.split(":")
                    elif '：' in event.message.text:
                        x = event.message.text.split("：")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==19):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        pixart_info = PixArt.objects.all() 
                        for user in user_info:
                            flag = 0
                            for pixart in pixart_info:
                                if(x[1]==pixart.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Pixart==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                PixArt.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Pixart=1) #修改
                                for user in user_info:
                                    info = '現在你的黑客松幣=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('企業位置圖' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('購買抽獎卷' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('企業任務總覽' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('活動規則' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('查看Level 1獎品清單' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('查看Level 2獎品清單' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif ('查看Level 3獎品清單' in event.message.text):
                    message.append(TextSendMessage(text=''))
                elif event.message.text=='查看企業任務完成進度':
                    f_l=['尚未完成','已完成']
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                    for user in user_info:
                        info = '中國信託：%s\n台積電：%s\n意法半導體：%s\nASML 艾司摩爾：%s\n恩智浦半導體：%s\n原相科技：%s\nKronos Research 麒點科技：%s\n國泰金控：%s\nLINE：%s\nYahoo：%s\n一零四資訊科技：%s\n新竹市政府：%s'%(f_l[user.CTBC],f_l[user.tsmc],f_l[user.STM],f_l[user.ASML],f_l[user.NXP],f_l[user.Pixart],f_l[user.Kronos],f_l[user.Cathay],f_l[user.Line],f_l[user.Yahoo],f_l[user.a104],f_l[user.Hsinchu])
                        message.append(TextSendMessage(text=info))                
                else:
                    message.append(TextSendMessage(text='輸入格式錯誤'))
                line_bot_api.reply_message(event.reply_token,message)

                return HttpResponse()
            else:
                return HttpResponseBadRequest()
