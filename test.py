'''
import random

times=1000

up2600=0
up2800=0
up2500=0
up2000=0
up2400=0
up1900=0


while times > 0:
    init = 0
    company = 12
    while company>0:
        x=random.randrange(100,301,100)
        init = init + x
        company = company -1
    print(init)
    if init >= 2600:
        up2600=up2600+1
    if init >= 2800:
        up2800=up2800+1
    if init >= 2500:
        up2500=up2500+1
    if init >= 2000:
        up2000=up2000+1
    if init >= 2400:
        up2400=up2400+1
    if init >= 1900:
        up1900=up1900+1
    #print("\n")
    times = times - 1

print("2600=")
print(up2600)
print("2800=")
print(up2800)
print("2500=")
print(up2500)
print("2000=")
print(up2000)
print("2400=")
print(up2400)
print("1900=")
print(up1900)
'''
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
    #a = input()
    anyToDecimal(a,36)
    print(anyToDecimal(a,36) % 2022)
    return anyToDecimal(a,36) % 2022 #這裡可以拿到最後要的mod出來的值 2022要記得改掉


bb=input()
x = bb.split(":")
print(x[1])
seaftermod = secretnum(x[1])
info = 'aftermod=%s'%(seaftermod)
print(info)

