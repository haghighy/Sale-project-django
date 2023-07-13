from asyncio.windows_events import NULL
from datetime import datetime
from email import message
from unicodedata import name
from unittest import result
from django.shortcuts import render , get_object_or_404
from collections import namedtuple
from jalali_date import datetime2jalali, date2jalali
# from django.utils.timezone import datetime

from app.models import *

# Create your views here.
# def home_view(request):
#     return render(request, "vorood.html")

def sabte_name(request):
    sbtmessage = []
    finishmessage = ""
    if request.method == "GET":
        return render(request, "sabtenam.html",{'msg': sbtmessage})
    if request.method == "POST":
        data = request.POST
        if User.objects.filter(userName = data['userName']).exists():
            sbtmessage.append("این نام کاربری قبلا در سامانه ثبت شده")
            # return render(request, "sabtenam.html",{'msg': sbtmessage})
        if User.objects.filter(telephone_sabet = data['telephone_sabet']).exists():
            sbtmessage.append("این تلفن ثابت قبلا در سامانه ثبت شده")
            # return render(request, "sabtenam.html",{'msg': sbtmessage})
        if User.objects.filter(phoneNumber = data['phoneNumber']).exists():
            sbtmessage.append("این شماره تلفن همراه قبلا در سامانه ثبت شده")
            # return render(request, "sabtenam.html",{'msg': sbtmessage})
        if User.objects.filter(codeMelli = data['codeMelli']).exists():
            sbtmessage.append("این کد ملی قبلا در سامانه ثبت شده")
            # return render(request, "sabtenam.html",{'msg': sbtmessage})
        # if User.objects.filter(email = data['email']).exists():
        #     sbtmessage = "این ایمیل قبلا در سامانه ثبت شده"
        #     return render(request, "sabtenam.html",{'msg': sbtmessage})
        if len(sbtmessage) != 0:
            return render(request, "sabtenam.html",{'msg': sbtmessage, 'data':data})
        try:
            lastID = User.objects.order_by('-userID')[0]
            maxID = lastID.userID
        except IndexError:
            maxID = 0
        a = User.objects.create(name=data['name'],phoneNumber=data['phoneNumber'] ,codeMelli=data['codeMelli'] , userName=data['userName'] , password=data['password'] , address=data['address'] , email=data['email'] ,telephone_sabet=data['telephone_sabet'], U_Type="user", Register_Status = "not register yet")
        a.save()
        # sol = User.objects.all()
        finishmessage = "ثبت نام با موفقیت انجام شد"
        return render(request, "sabtenam.html",{'finishmsg': finishmessage})

def log_in(request):
    mymessage = ""
    if request.method == "GET":
        return render(request, "vorood.html",{'msg': mymessage})
    if request.method == "POST":
        data = request.POST
        try:
            g = User.objects.get(userName = data['userName'])
        except User.DoesNotExist:
            mymessage = "نام کاربری اشتباه وارد شده. لطفا مجدد تلاش کنید"
            return render(request, "vorood.html",{'msg': mymessage})
        if (g.password == data['password'] and g.U_Type == "user"):
            jalali_join = datetime2jalali(datetime.now()).strftime('%y/%m/%d _ %H:%M:%S')
            return render(request, "userpanel.html" ,{'User': g, 'mydate':jalali_join})
            # return ordering(request)
        else:
            mymessage = "رمز ورود اشتباه وارد شده. لطفا مجدد تلاش کنید"
            return render(request, "vorood.html",{'msg': mymessage})


def forgot_pass(request):
    if request.method == "GET":
        return render(request, "forgotpass.html")
    if request.method == "POST":
        data = request.POST
        try:
            g = User.objects.get(phoneNumber = data['phoneNumber'])
        except User.DoesNotExist:
            mymessage = "این شماره تلفن در سامانه موجود نمیباشد. دقت کنید شماره را به درستی وارد کرده باشید!"
            return render(request, "forgotpass.html",{'msg': mymessage})
        if (g.codeMelli == data['codeMelli']):
            g.password = data['password']
            g.save()
            mymessage = " رمز جدید با موفقیت برای شما ثبت شد. (نام کاربری شما " + g.userName + " است.)"
            return render(request, "forgotpass.html",{'msg': mymessage})
        else:
            mymessage = "کدملی اشتباه وارد شده. لطفا مجدد تلاش کنید!"
            return render(request, "forgotpass.html",{'msg': mymessage})

context = {}
def ordering(request):
    msg = ""
    O_ID1 = "" 
    O_ID2 = ""
    O_ID3 = ""
    O_ID4 = ""
    O_ID5 = ""
    goodoptions = Good.objects.all()
    designoptions = Design.objects.all()
    coloroptions = Color.objects.all()
    if request.method == "GET":
        system = request.GET.get('User', None)
        context['goodoptions'] = goodoptions
        context['designoptions'] = designoptions
        context['coloroptions'] = coloroptions
        context['userID'] = system
        try:
            u = User.objects.get(userID = context['userID'])
        except User.DoesNotExist:
            return render(request, "sale1.html", context)
        context['name'] = u.name
        context['phoneNumber'] = u.phoneNumber
        context['userName'] = u.userName
        context['address'] = u.address
        context['telephone_sabet'] = u.telephone_sabet
        context['codeMelli'] =u.codeMelli
        context['password'] = u.password
        context['email'] = u.email
        context['U_Type'] = u.U_Type
        context['Register_Status'] =u.Register_Status
        print(u.Register_Status)
        if (u.Register_Status == "not register yet" or u.Register_Status == "non-register"):
            context['msg'] = "شما هنوز توسط ادمین تایید نشدید. فقط کاربرانی که تایید شوند قادر به سفارش دادن هستند."
        else:
            context['msg'] = ""
        # context['mymessage'] = mymessage
        return render(request, "sale1.html", context)
    if request.method == "POST":
        data = request.POST
        # DD2 = datetime.now()
        # print(DD2)
        DD = datetime2jalali(datetime.now()).strftime('14%y-%m-%d %H:%M:%S')
        orderCount = 0
        try:
            lastOrder = customer_order.objects.order_by('-orderID')[0]
            maxID = lastOrder.orderID
        except IndexError:
            maxID = 0

        try:
            lastOrderNum = customer_order.objects.order_by('-orderNumber')[0]
            maxNum = lastOrderNum.orderNumber
        except IndexError:
            maxNum = 0

        try:
            u = User.objects.get(userID = context['userID'])
        except User.DoesNotExist:
            return render(request, "sale1.html", {'goodoptions':goodoptions, 'designoptions':designoptions, 'coloroptions':coloroptions, 'msg': msg})
        # if (u.Register_Status == "registered"):
        tozihat5 = data['tozihat_5orders']
        ordersCount = 0
        if (data['good_description1'] != 'non' and data['count1'] != ''):
            cc1=data['color_description1']
            dc1 = data['design_description1']
            w1=data['width1']
            l1=data['length1']
            t1 =data['thickness1']
            tozihat1_1 = data['tozihat_1order1']
            if cc1=='': cc1=0
            if dc1=='': dc1=0
            if w1=='': w1=0
            if l1=='': l1=0
            if t1=='': t1=0
            O_ID1 = str(maxID+1)
            ordersCount += 1
            newOrder1 = customer_order.objects.create(U_userID = u.userID, good_description=data['good_description1'],color_description=cc1 ,design_description=dc1 , width=w1 , length=l1 , thickness=t1 , count=data['count1'] ,registration_date=DD,Order_Status = "sabt shode" , orderNumber=maxNum+1, tozihat_1order = tozihat1_1, tozihat_5orders = tozihat5)
            newOrder1.save()
            orderCount += 1
        if (data['good_description2'] != 'non' and data['count2'] != ''):
            cc2=data['color_description2']
            dc2 = data['design_description2']
            w2=data['width2']
            l2=data['length2']
            t2 =data['thickness2']
            tozihat1_2 = data['tozihat_1order2']
            if cc2=='': cc2=0
            if dc2=='': dc2=0
            if w2=='': w2=0
            if l2=='': l2=0
            if t2=='': t2=0
            O_ID2 = str(maxID+2)
            ordersCount += 1
            newOrder2 = customer_order.objects.create(U_userID = u.userID, good_description=data['good_description2'],color_description=cc2 ,design_description=dc2 , width=w2 , length=l2 , thickness=t2 , count=data['count2'] ,registration_date=DD,Order_Status = "sabt shode", orderNumber=maxNum+1, tozihat_1order = tozihat1_2, tozihat_5orders = tozihat5)
            newOrder2.save()
            orderCount += 1
        if (data['good_description3'] != 'non' and data['count3'] != ''):
            cc3=data['color_description3']
            dc3 = data['design_description3']
            w3=data['width3']
            l3=data['length3']
            t3 =data['thickness3']
            tozihat1_3 = data['tozihat_1order3']
            if cc3=='': cc3=0
            if dc3=='': dc3=0
            if w3=='': w3=0
            if l3=='': l3=0
            if t3=='': t3=0
            O_ID3 = str(maxID+3)
            ordersCount += 1
            newOrder3 = customer_order.objects.create(U_userID = u.userID, good_description=data['good_description3'],color_description=cc3 ,design_description=dc3 , width=w3 , length=l3 , thickness=t3 , count=data['count3'] ,registration_date=DD,Order_Status = "sabt shode", orderNumber=maxNum+1, tozihat_1order = tozihat1_3, tozihat_5orders = tozihat5)
            newOrder3.save()
            orderCount += 1
        if (data['good_description4'] != 'non' and data['count4'] != ''):
            cc4=data['color_description4']
            dc4 = data['design_description4']
            w4=data['width4']
            l4=data['length4']
            t4 =data['thickness4']
            tozihat1_4 = data['tozihat_1order4']
            if cc4=='': cc4=0
            if dc4=='': dc4=0
            if w4=='': w4=0
            if l4=='': l4=0
            if t4=='': t4=0
            O_ID4 = str(maxID+4)
            ordersCount += 1
            newOrder4 = customer_order.objects.create(U_userID = u.userID, good_description=data['good_description4'],color_description=cc4 ,design_description=dc4 , width=w4 , length=l4 , thickness=t4 , count=data['count4'] ,registration_date=DD,Order_Status = "sabt shode", orderNumber=maxNum+1, tozihat_1order = tozihat1_4, tozihat_5orders = tozihat5)
            newOrder4.save()
            orderCount += 1
        if (data['good_description5'] != 'non' and data['count5'] != ''):
            cc5=data['color_description5']
            dc5 = data['design_description5']
            w5=data['width5']
            l5=data['length5']
            t5 =data['thickness5']
            tozihat1_5 = data['tozihat_1order5']
            if cc5=='': cc5=0
            if dc5=='': dc5=0
            if w5=='': w5=0
            if l5=='': l5=0
            if t5=='': t5=0
            O_ID5 = str(maxID+5)
            newOrder5 = customer_order.objects.create(U_userID = u.userID, good_description=data['good_description5'],color_description=cc5 ,design_description=dc5 , width=w5 , length=l5, thickness=t5 , count=data['count5'] ,registration_date=DD,Order_Status = "sabt shode", orderNumber=maxNum+1, tozihat_1order = tozihat1_5, tozihat_5orders = tozihat5)
            newOrder5.save()
            orderCount += 1
        # IDs = [O_ID1, O_ID2, O_ID3, O_ID4, O_ID5]
        # msg = "سفارش شما با موفقیت ثبت شد، کدهای سفارشات شما:  " + OrdersIDs
        if orderCount != 0: 
            msg = "سفارش شما با موفقیت ثبت شد، شماره دسته سفارش شما:  " + str(maxNum+1)  + " - تاریخ ثبت سفارش: " + DD
        else:
            msg = ""
        context['msg'] = msg
        return render(request, "sale1.html", context)
        # else:
        #     msg = "فقط کاربرانی که توسط ادمین تایید شوند، قادر به ثبت سفارش خواهند بود. لطفا بعدا مجدد امتحان کنید."
        #     context['msg'] = msg
        #     return render(request, "sale1.html", context)

admin_infos2 = {}
def panel_admin(request):
    if request.method == "GET":
        adminID = request.GET.get('User', None)
        try:
            g = User.objects.get(userID = int(adminID))
        except User.DoesNotExist:
            mymessage = ""
            return render(request, "paneladmin.html",{'msg': mymessage})
        return render(request, "paneladmin.html", {'adminID': g.userID, 'admin_username':g.userName})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if (data['action'] == "add-good"):
            return render(request, "addnewgdc.html", {'adminID':adminID})
        if (data['action']== "delete-good"):
            sucess_msg = ""
            result = Good.objects.all()
            return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"no select" , 'adminID':adminID})
        if (data['action']== "all-users"):
            newUsers = User.objects.filter(U_Type = "user").filter(Register_Status = "not register yet")
            resultCount = len(newUsers)
            return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'adminID':adminID})
        if (data['action']== "all-orders"):
            result = customer_order.objects.order_by('orderNumber')
            uniq_result = {}
            for r in result:
                if not r.orderNumber in uniq_result.keys():
                    uniq_result[r.orderNumber] = r
            result2 = uniq_result.values()
            resultCount = len(result2)
            Point = namedtuple("Point", ["x", "y"])
            allPoints = []
            for r in result2:
                u = User.objects.get(userID = r.U_userID)
                allPoints.append(Point(r,u.userName))

            allUsers = User.objects.all()
            # queryset = User.objects.prefetch_related('userID2')
            # print(queryset)
            return render(request, "seeAllOrders.html",{'result': allPoints , 'resultCount' : resultCount, 'allUsers':allUsers, 'adminID':adminID})
        if (data['action']== "new-admin"):
            return render(request, "newadmin.html", {'adminID':adminID})
        ac = data['action'].split('&')
        if (ac[0] == "editInfo"):
            mymessage = ""
            admin_infos2['userID'] = int(ac[1])
            admin_infos2['adminID'] = adminID
            try:
                u = User.objects.get(userID = admin_infos2['userID'])
            except User.DoesNotExist:
                return render(request, "editadmin.html", admin_infos2)
            admin_infos2['mymessage'] = mymessage
            admin_infos2['name'] = u.name
            admin_infos2['phoneNumber'] = u.phoneNumber
            admin_infos2['userName'] = u.userName
            admin_infos2['address'] = u.address
            admin_infos2['telephone_sabet'] = u.telephone_sabet
            admin_infos2['codeMelli'] =u.codeMelli
            admin_infos2['password'] = u.password
            admin_infos2['email'] = u.email
            admin_infos2['U_Type'] = u.U_Type
            admin_infos2['Register_Status'] =u.Register_Status
            return render(request, "editadmin.html", admin_infos2 )

        return render(request, "paneladmin.html", {'adminID':adminID})

res_public2 = None
def all_orders(request):
    # res_public = res_public
    global res_public2
    Point = namedtuple("Point", ["x", "y"])
    # res_public = customer_order.objects.order_by('orderNumber')
    # uniq_result = {}
    # for r in res_public:
    #     if not r.orderNumber in uniq_result.keys():
    #         uniq_result[r.orderNumber] = r
    # result2 = uniq_result.values()
    # resultCount = len(result2)
    # Point = namedtuple("Point", ["x", "y"])
    # allPoints = []
    # for r in result2:
    #     u = User.objects.get(userID = r.U_userID)
    #     allPoints.append(Point(r,u.userName))
    if request.method == "GET":
        res_public = customer_order.objects.order_by('orderNumber')
        res_public2 = customer_order.objects.order_by('orderNumber')
        uniq_result = {}
        for r in res_public:
            if not r.orderNumber in uniq_result.keys():
                uniq_result[r.orderNumber] = r
        result2 = uniq_result.values()
        resultCount = len(result2)
        Point = namedtuple("Point", ["x", "y"])
        allPoints = []
        for r in result2:
            u = User.objects.get(userID = r.U_userID)
            allPoints.append(Point(r,u.userName))
        resultCount = len(uniq_result.values())
        allUsers = User.objects.all()
        username_toShow = "-"
        return render(request, "seeAllOrders.html" ,{'result': allPoints, 'resultCount' : resultCount ,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if 'resultCount' in data:
            dataCount = data['resultCount']
            for i in range(1,int(dataCount)+1):
                order_num = "orderNumber" + str(i)
                order_Status = "orderStatus" + str(i)
                text_admin_user = "text_adminTouser" + str(i)
                text_admin_admin = "text_adminToadmin" + str(i)
                try:
                    g = customer_order.objects.filter(orderNumber = data[order_num])
                except customer_order.DoesNotExist:
                    break
                if (data[order_Status] == "sabt"):
                    for o in g:
                        o.Order_Status = "sabt shode"
                        o.save()
                if (data[order_Status] == "taeed"):
                    for o in g:
                        o.Order_Status = "taeed shode"
                        o.save()
                if (data[order_Status] == "rad"):
                    for o in g:
                        o.Order_Status = "rad shode"
                        o.save()
                if (data[order_Status] == "ersal"):
                    for o in g:
                        o.Order_Status = "ersal baraye tolid"
                        o.save()
                if (data[order_Status] == "tahvil"):
                    for o in g:
                        o.Order_Status = "tahvil dade shode"
                        o.save()
                for o in g:
                    o.text_adminTouser = data[text_admin_user]
                    o.text_adminToadmin = data[text_admin_admin]
                    o.save()
            myMSG = "تغییرات با موفقیت اعمال شد"
            res_public = customer_order.objects.order_by('orderNumber')
            uniq_result = {}
            for r in res_public:
                if not r.orderNumber in uniq_result.keys():
                    uniq_result[r.orderNumber] = r
            result2 = uniq_result.values()
            resultCount = len(result2)
            allPoints = []
            for r in result2:
                u = User.objects.get(userID = r.U_userID)
                allPoints.append(Point(r,u.userName))
            allUsers = User.objects.all()
            username_toShow = "-"
            return render(request, "seeAllOrders.html", {'result': allPoints, 'resultCount' : dataCount ,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
        else:
            if data['show-with-user'] == "nothing":
                res_public = customer_order.objects.order_by('orderNumber')
                res_public2 = customer_order.objects.order_by('orderNumber')
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                Point = namedtuple("Point", ["x", "y"])
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                resultCount = len(uniq_result.values())
                allUsers = User.objects.all()
                myMSG = ""
                username_toShow = "-"
                # return render(request, "seeAllOrders.html" ,{'result': allPoints, 'resultCount' : resultCount ,'myMSG':myMSG, 'allUsers':allUsers})
            else:
                user_ID = int(data['show-with-user'])
                us = User.objects.get(userID = user_ID)
                username_toShow = us.userName
                res_public2 = customer_order.objects.filter(U_userID = user_ID)
                uniq_result = {}
                for r in res_public2:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات ثبت شده (در حال بررسی)"
                allUsers = User.objects.all()
                # return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers})





            if data['show-res'] == "by-Num":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.order_by('orderNumber')
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات بر اساس شماره دسته سفارش:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "by-date":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public =res_public2.order_by('-registration_date')
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG= "سفارشات بر اساس تاریخ جدید به قدیم:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "by-date-old":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.order_by('registration_date')
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات بر اساس تاریخ قدیمی به جدید:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "waits":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.filter(Order_Status = "sabt shode")
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات ثبت شده (در حال بررسی)"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "oks":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.filter(Order_Status = "taeed shode")
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات تایید شده  :"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "not-oks":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.filter(Order_Status = "rad shode")
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات رد شده:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "sent-for-make":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.filter(Order_Status = "ersal baraye tolid")
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = " سفارشات ارسال شده برای تولید:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})
            if data['show-res'] == "finishes":
                if res_public2 == None:
                    res_public2 = customer_order.objects.all()
                res_public = res_public2.filter(Order_Status = "tahvil dade shode")
                uniq_result = {}
                for r in res_public:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                resultCount = len(result2)
                allPoints = []
                for r in result2:
                    u = User.objects.get(userID = r.U_userID)
                    allPoints.append(Point(r,u.userName))
                myMSG = "سفارشات تحویل داده شده به کاربر:"
                allUsers = User.objects.all()
                return render(request, "seeAllOrders.html",{'result': allPoints, 'resultCount' : resultCount,'myMSG':myMSG, 'allUsers':allUsers, 'username_toShow' :username_toShow, 'adminID':adminID})

def add_good(request):
    sucess_msg = ""
    if request.method == "GET":
        return render(request, "paneladmin.html", {'sucess_msg':sucess_msg})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if (data['good_design_color']=="good"):
            if Good.objects.filter(g_description = data['description']).exists():
                sucess_msg = "این کالا قبلا در سامانه ثبت شده"
            else:
                g = Good.objects.create( g_description=data['description'])
                g.save()
                sucess_msg = "کالا با موفقیت افزوده شد"
        elif (data['good_design_color']=="design"):
            if Design.objects.filter(d_description = data['description']).exists():
                sucess_msg = "این طرح قبلا در سامانه ثبت شده"
            else:
                d = Design.objects.create( d_description=data['description'])
                d.save()
                sucess_msg = "طرح با موفقیت افزوده شد"
        elif (data['good_design_color']=="color"):
            if Color.objects.filter(c_description = data['description']).exists():
                sucess_msg = "این رنگ قبلا در سامانه ثبت شده"
            else:
                c = Color.objects.create(c_description=data['description'])
                c.save()
                sucess_msg = "رنگ با موفقیت افزوده شد"
        else:
            sucess_msg ="دوباره تلاش کنید"
    return render(request, "addnewgdc.html", {'sucess_msg':sucess_msg , 'adminID':adminID})

def delete_good(request):
    sucess_msg = ""
    result = Good.objects.all()
    if request.method == "GET":
        return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"no select"})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if 'good_design_color' in data:
            if (data['good_design_color']=="good"):
                result = Good.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "good", 'adminID':adminID})
            elif (data['good_design_color']=="design"):
                result = Design.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "design", 'adminID':adminID})
            elif (data['good_design_color']=="color"):
                result = Color.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "color", 'adminID':adminID})
        if 'delete-obj' in data:
            if data['obj'] == "good":
                if (not customer_order.objects.filter(good_description = data['delete-obj']).exists()) or (not customer_order.objects.filter(good_description = data['delete-obj'],Order_Status="sabt shode").exists() and not customer_order.objects.filter(good_description = data['delete-obj'],Order_Status="taeed shode").exists() and not customer_order.objects.filter(good_description = data['delete-obj'],Order_Status="ersal baraye tolid").exists() and not customer_order.objects.filter(good_description = data['delete-obj'],Order_Status="tahvil dade shode").exists()):
                    if Good.objects.filter(g_description = data['delete-obj']).exists():
                        c = Good.objects.get(g_description = data['delete-obj'])
                        c.delete()
                        sucess_msg = "کالا با موفقیت حذف شد"
                    else:
                        sucess_msg = "این کالا در سامانه موجود نمیباشد"
                else:
                    sucess_msg = "سفارشاتی رد نشده با این کالا وجود دارد، قادر به حذف این کالا نیستید."
                result = Good.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "good", 'adminID':adminID})
            elif data['obj'] == "design":
                if (not customer_order.objects.filter(design_description = data['delete-obj']).exists()) or (not customer_order.objects.filter(design_description = data['delete-obj'],Order_Status="sabt shode").exists() and not customer_order.objects.filter(design_description = data['delete-obj'],Order_Status="taeed shode").exists() and not customer_order.objects.filter(design_description = data['delete-obj'],Order_Status="ersal baraye tolid").exists() and not customer_order.objects.filter(design_description = data['delete-obj'],Order_Status="tahvil dade shode").exists()):
                    if Design.objects.filter(d_description = data['delete-obj']).exists():
                        c = Design.objects.get(d_description = data['delete-obj'])
                        c.delete()
                        sucess_msg = "طرح با موفقیت حذف شد"
                    else:
                        sucess_msg = "این طرح در سامانه موجود نمیباشد"
                else:
                    sucess_msg = "سفارشاتی رد نشده با این طرح وجود دارد، قادر به حذف این طرح نیستید."
                result = Design.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "design", 'adminID':adminID})
            elif data['obj'] == "color":
                if (not customer_order.objects.filter(color_description = data['delete-obj']).exists()) or (not customer_order.objects.filter(color_description = data['delete-obj'],Order_Status="sabt shode").exists() and not customer_order.objects.filter(color_description = data['delete-obj'],Order_Status="taeed shode").exists() and not customer_order.objects.filter(color_description = data['delete-obj'],Order_Status="ersal baraye tolid").exists() and not customer_order.objects.filter(color_description = data['delete-obj'],Order_Status="tahvil dade shode").exists()):
                    if Color.objects.filter(c_description = data['delete-obj']).exists():
                        c = Color.objects.get(c_description = data['delete-obj'])
                        c.delete()
                        sucess_msg = "رنگ با موفقیت حذف شد"
                    else:
                        sucess_msg = "این رنگ در سامانه موجود نمیباشد"
                else:
                    sucess_msg = "سفارشاتی رد نشده با این رنگ وجود دارد، قادر به حذف این رنگ نیستید."
                result = Color.objects.all()
                return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'result':result, 'selected':"done", 'obj' : "color", 'adminID':adminID})

    return render(request, "delgdc.html", {'sucess_msg':sucess_msg, 'adminID':adminID})


def Registering_Users(request):
    myMSG = ""
    if request.method == "GET":
        return render(request, "registerUser.html", {'myMSG':myMSG})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if 'resultCount' in data:
            dataCount = data['resultCount']
            for i in range(1,int(dataCount)+1):
                user_Name = "userName" + str(i)
                register_Status = "registerStatus" + str(i)
                try:
                    g = User.objects.get(userName = data[user_Name])
                except User.DoesNotExist:
                    break
                if (data[register_Status] == "register"):
                    g.Register_Status = "registered"
                    g.save()
                if (data[register_Status] == "non-register"):
                    g.Register_Status = "non-register"
                    g.save()
                if (data[register_Status] == "not-register-yet"):
                    g.Register_Status = "not register yet"
                    g.save()
            myMSG = "تغییرات با موفقیت اعمال شد"
            newUsers = User.objects.filter(U_Type = "user").filter(Register_Status = "not register yet")
            resultCount = len(newUsers)
            return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'myMSG':myMSG, 'adminID':adminID})
        else:
            if data['show-res'] == "all":
                newUsers = User.objects.filter(U_Type = "user")
                resultCount = len(newUsers)
                myMSG = 'همه کاربران:'
                return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'myMSG':myMSG, 'adminID':adminID})
            if data['show-res'] == "yes":
                newUsers = User.objects.filter(U_Type = "user").filter(Register_Status = "registered")
                resultCount = len(newUsers)
                myMSG = "تایید شده ها:"
                return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'myMSG':myMSG, 'adminID':adminID})
            if data['show-res'] == "no":
                newUsers = User.objects.filter(U_Type = "user").filter(Register_Status = "non-register")
                resultCount = len(newUsers)
                myMSG = "کاربران رد شده:"
                return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'myMSG':myMSG, 'adminID':adminID})
            if data['show-res'] == "not-yet":
                newUsers = User.objects.filter(U_Type = "user").filter(Register_Status = "not register yet")
                resultCount = len(newUsers)
                myMSG = "کاربران تازه وارد شده ( در حال بررسی ها):"
                return render(request, "registerUser.html", {'result':newUsers, 'resultCount' : resultCount, 'myMSG':myMSG, 'adminID':adminID})

def log_in_admin(request):
    mymessage = ""
    if request.method == "GET":
        return render(request, "voroodAdmin.html",{'msg': mymessage})
    if request.method == "POST":
        data = request.POST
        try:
            g = User.objects.get(userName = data['userName'])
        except User.DoesNotExist:
            mymessage = "نام کاربری اشتباه وارد شده. لطفا مجدد تلاش کنید"
            return render(request, "voroodAdmin.html",{'msg': mymessage})
        if (g.password == data['password'] and g.U_Type == "admin"):
            return render(request, "paneladmin.html", {'adminID': g.userID, 'admin_username': g.userName})
            # return ordering(request)
        else:
            mymessage = "رمز ورود اشتباه وارد شده. لطفا مجدد تلاش کنید"
            return render(request, "voroodAdmin.html",{'msg': mymessage})

user_infos2 = {}
def edit_info(request):
    mymessage = ""
    if request.method == "GET":
        system = request.GET.get('User', None)
        user_infos2['userID'] = system
        try:
            u = User.objects.get(userID = user_infos2['userID'])
        except User.DoesNotExist:
            return render(request, "editinfos.html", user_infos2)
        user_infos2['mymessage'] = mymessage
        user_infos2['name'] = u.name
        user_infos2['phoneNumber'] = u.phoneNumber
        user_infos2['userName'] = u.userName
        user_infos2['address'] = u.address
        user_infos2['telephone_sabet'] = u.telephone_sabet
        user_infos2['codeMelli'] =u.codeMelli
        user_infos2['password'] = u.password
        user_infos2['email'] = u.email
        user_infos2['U_Type'] = u.U_Type
        user_infos2['Register_Status'] =u.Register_Status
        return render(request, "editinfos.html", user_infos2 )
    if request.method == "POST":
        data = request.POST
        try:
            u = User.objects.get(userID = user_infos2['userID'])
        except User.DoesNotExist:
            return render(request, "editinfos.html", user_infos2)        
        try:
            g = User.objects.get(userName = u.userName)
        except User.DoesNotExist:
            mymessage = "نام کاربری اشتباه وارد شده. لطفا مجدد تلاش کنید"
            user_infos2['mymessage'] = mymessage
            return render(request, "editinfos.html", user_infos2)


        if (User.objects.filter(phoneNumber = data['phoneNumber']).exists() and int(User.objects.get(phoneNumber = data['phoneNumber']).userID) != int(user_infos2['userID'])):
            sbtmessage = "این شماره تلفن قبلا در سامانه ثبت شده"
            user_infos2['mymessage'] = ""
            user_infos2['msg'] = sbtmessage
            return render(request, "editinfos.html",user_infos2)
        if (User.objects.filter(codeMelli = data['codeMelli']).exists() and int(User.objects.get(codeMelli = data['codeMelli']).userID) != int(user_infos2['userID'])):
            sbtmessage = "این کد ملی قبلا در سامانه ثبت شده"
            user_infos2['mymessage'] = ""
            user_infos2['msg'] = sbtmessage
            return render(request, "editinfos.html",user_infos2)
        if (User.objects.filter(userName = data['userName']).exists() and int(User.objects.get(userName = data['userName']).userID) != int(user_infos2['userID'])):
            sbtmessage = "این نام کاربری قبلا در سامانه ثبت شده"
            user_infos2['mymessage'] = ""
            user_infos2['msg'] = sbtmessage
            return render(request, "editinfos.html",user_infos2)
        # if User.objects.filter(email = data['email']).exists():
        #     sbtmessage = "این ایمیل قبلا در سامانه ثبت شده"
        #     return render(request, "sabtenam.html",{'msg': sbtmessage})
        if (User.objects.filter(telephone_sabet = data['telephone_sabet']).exists() and int(User.objects.get(telephone_sabet = data['telephone_sabet']).userID) != int(user_infos2['userID'])):
            sbtmessage = "این تلفن قبلا در سامانه ثبت شده"
            user_infos2['mymessage'] = ""
            user_infos2['msg'] = sbtmessage
            return render(request, "editinfos.html",user_infos2)
        g.name = data['name']
        g.phoneNumber = data['phoneNumber']
        g.codeMelli = data['codeMelli']
        g.userName = data['userName']
        g.password = data['password']
        g.address = data['address']
        g.email = data['email']
        g.telephone_sabet = data['telephone_sabet']
        g.save()
        user_infos2['msg'] = ""
        mymessage = "ویرایش اطلاعات با موفقیت انجام شد"
        user_infos2['mymessage'] = mymessage

        user_infos2['name'] = data['name']
        user_infos2['phoneNumber'] = data['phoneNumber']
        user_infos2['codeMelli'] = data['codeMelli']
        user_infos2['userName'] = data['userName']
        user_infos2['password'] = data['password']
        user_infos2['address'] = data['address']
        user_infos2['email'] = data['email']
        user_infos2['telephone_sabet'] = data['telephone_sabet']
        return render(request, "editinfos.html", user_infos2)


def new_admin(request):
    sbtmessage = []    
    finishmessage = ""
    if request.method == "GET":
        return render(request, "newadmin.html",{'msg': sbtmessage})
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        if User.objects.filter(userName = data['userName']).exists():
            sbtmessage.append("این نام کاربری قبلا در سامانه ثبت شده")
        if User.objects.filter(telephone_sabet = data['telephone_sabet']).exists():
            sbtmessage.append("این تلفن قبلا در سامانه ثبت شده")
        if User.objects.filter(phoneNumber = data['phoneNumber']).exists():
            sbtmessage.append("این شماره تلفن همراه قبلا در سامانه ثبت شده")
        if User.objects.filter(codeMelli = data['codeMelli']).exists():
            sbtmessage.append("این کد ملی قبلا در سامانه ثبت شده")
        if len(sbtmessage) != 0:
            return render(request, "newadmin.html",{'msg': sbtmessage, 'adminID':adminID, 'data':data})
        try:
            lastID = User.objects.order_by('-userID')[0]
            maxID = lastID.userID
        except IndexError:
            maxID = 0
        a = User.objects.create(name=data['name'],phoneNumber=data['phoneNumber'] ,codeMelli=data['codeMelli'] , userName=data['userName'] , password=data['password'] , address=data['address'] , email=data['email'] ,telephone_sabet=data['telephone_sabet'], U_Type="admin", Register_Status = "registered")
        a.save()
        # sol = User.objects.all()
        finishmessage = "ثبت نام با موفقیت انجام شد"
        return render(request, "newadmin.html",{'finishmsg': finishmessage, 'adminID':adminID})


user_id = {}
def last_orders(request):
    result = customer_order.objects.order_by('orderNumber')
    uniq_result = {}
    for r in result:
        if not r.orderNumber in uniq_result.keys():
            uniq_result[r.orderNumber] = r
    result2 = uniq_result.values()
    if request.method == "GET":
        user_id['u_id'] = request.GET.get('User', None)
        user_order_nums = customer_order.objects.filter(U_userID = user_id['u_id'])
        uniq_nums2 = {}
        for r in user_order_nums:
            if not r.orderNumber in uniq_nums2.keys():
                uniq_nums2[r.orderNumber] = r
        user_order_nums = uniq_nums2.values()
        result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('orderNumber')
        uniq_result = {}
        for r in result:
            if not r.orderNumber in uniq_result.keys():
                uniq_result[r.orderNumber] = r
        result2 = uniq_result.values()
        m_message = "تمام سفارشات:"
        return render(request, "lastorders.html" ,{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
    if request.method == "POST":
        data = request.POST
        user_order_nums = customer_order.objects.filter(U_userID = user_id['u_id'])
        uniq_nums2 = {}
        for r in user_order_nums:
            if not r.orderNumber in uniq_nums2.keys():
                uniq_nums2[r.orderNumber] = r
        user_order_nums = uniq_nums2.values()



        



        numOFOrder = data['show-one-order']
        if numOFOrder == "nothing":
            # user_order_nums = customer_order.objects.filter(U_userID = user_id['u_id'])
            # uniq_nums2 = {}
            # for r in user_order_nums:
            #     if not r.orderNumber in uniq_nums2.keys():
            #         uniq_nums2[r.orderNumber] = r
            # user_order_nums = uniq_nums2.values()
            # result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('orderNumber')
            # uniq_result = {}
            # for r in result:
            #     if not r.orderNumber in uniq_result.keys():
            #         uniq_result[r.orderNumber] = r
            # result2 = uniq_result.values()
            # return render(request, "lastorders.html" ,{'result': result2, 'user_order_nums': user_order_nums})





            if data['show-res'] == "by-ID":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('orderID')
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات به ترتیب کد سفارش:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "by-Num":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('orderNumber')
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات به ترتیب شماره سفارش:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "by-date":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('-registration_date')
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات به ترتیب زمان(جدید به قدیم):"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "by-date-old":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).order_by('registration_date')
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message ="سفارشات به ترتیب زمان (قدیمی به جدید):"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})

            if data['show-res'] == "waits":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).filter(Order_Status = "sabt shode")
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات در حال بررسی(ثبت شده):"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "oks":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).filter(Order_Status = "taeed shode")
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات تایید شده:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "not-oks":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).filter(Order_Status = "rad shode")
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message="سفارشات رد شده:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "sent-for-make":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).filter(Order_Status = "ersal baraye tolid")
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message="سفارشات ارسال شده برای تولید:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})
            if data['show-res'] == "finishes":
                result = customer_order.objects.filter(U_userID = user_id['u_id']).filter(Order_Status = "tahvil dade shode")
                uniq_result = {}
                for r in result:
                    if not r.orderNumber in uniq_result.keys():
                        uniq_result[r.orderNumber] = r
                result2 = uniq_result.values()
                m_message = "سفارشات مختومه:"
                return render(request, "lastorders.html",{'result': result2, 'user_order_nums': user_order_nums, 'm_message':m_message})





        else:
            try:
                result = customer_order.objects.filter(orderNumber = int(numOFOrder))
            except customer_order.DoesNotExist:
                result = None
            uniq_result = None
            for r in result:
                uniq_result = r
                break
            result2 = uniq_result
            res = []
            res.append(result2)
            m_message = "سفارش شماره ی : " + numOFOrder + " ام"
            return render(request, "lastorders.html",{'result': res, 'user_order_nums': user_order_nums, 'm_message':m_message})


def edit_info_admin(request):
    mymessage = ""
    # if request.method == "GET":
    #     system = request.GET.get('User', None)
    #     user_infos2['userID'] = system
    #     try:
    #         u = User.objects.get(userID = user_infos2['userID'])
    #     except User.DoesNotExist:
    #         return render(request, "editinfos.html", user_infos2)
    #     user_infos2['mymessage'] = mymessage
    #     user_infos2['name'] = u.name
    #     user_infos2['phoneNumber'] = u.phoneNumber
    #     user_infos2['userName'] = u.userName
    #     user_infos2['address'] = u.address
    #     user_infos2['telephone_sabet'] = u.telephone_sabet
    #     user_infos2['codeMelli'] =u.codeMelli
    #     user_infos2['password'] = u.password
    #     user_infos2['email'] = u.email
    #     user_infos2['U_Type'] = u.U_Type
    #     user_infos2['Register_Status'] =u.Register_Status
    #     return render(request, "editinfos.html", user_infos2 )
    if request.method == "POST":
        data = request.POST
        adminID = data['adminID']
        try:
            # u = User.objects.get(userID = admin_infos2['userID'])
            u = User.objects.get(userID = adminID)
        except User.DoesNotExist:
            return render(request, "editadmin.html", admin_infos2)        
        try:
            g = User.objects.get(userName = u.userName)
        except User.DoesNotExist:
            mymessage = "نام کاربری اشتباه وارد شده. لطفا مجدد تلاش کنید"
            admin_infos2['mymessage'] = mymessage
            return render(request, "editadmin.html", admin_infos2)


        if (User.objects.filter(phoneNumber = data['phoneNumber']).exists() and int(User.objects.get(phoneNumber = data['phoneNumber']).userID) != int(admin_infos2['userID'])):
            sbtmessage = "این شماره تلفن قبلا در سامانه ثبت شده"
            admin_infos2['mymessage'] = ""
            admin_infos2['msg'] = sbtmessage
            return render(request, "editadmin.html",admin_infos2)
        if (User.objects.filter(codeMelli = data['codeMelli']).exists() and int(User.objects.get(codeMelli = data['codeMelli']).userID) != int(admin_infos2['userID'])):
            sbtmessage = "این کد ملی قبلا در سامانه ثبت شده"
            admin_infos2['mymessage'] = ""
            admin_infos2['msg'] = sbtmessage
            return render(request, "editadmin.html",admin_infos2)
        if (User.objects.filter(userName = data['userName']).exists() and int(User.objects.get(userName = data['userName']).userID) != int(admin_infos2['userID'])):
            sbtmessage = "این نام کاربری قبلا در سامانه ثبت شده"
            admin_infos2['mymessage'] = ""
            admin_infos2['msg'] = sbtmessage
            return render(request, "editadmin.html",admin_infos2)
        # if User.objects.filter(email = data['email']).exists():
        #     sbtmessage = "این ایمیل قبلا در سامانه ثبت شده"
        #     return render(request, "sabtenam.html",{'msg': sbtmessage})
        if (User.objects.filter(telephone_sabet = data['telephone_sabet']).exists() and int(User.objects.get(telephone_sabet = data['telephone_sabet']).userID) != int(admin_infos2['userID'])):
            sbtmessage = "این تلفن قبلا در سامانه ثبت شده"
            admin_infos2['mymessage'] = ""
            admin_infos2['msg'] = sbtmessage
            return render(request, "editadmin.html",admin_infos2)
        g.name = data['name']
        g.phoneNumber = data['phoneNumber']
        g.codeMelli = data['codeMelli']
        g.userName = data['userName']
        g.password = data['password']
        g.address = data['address']
        g.email = data['email']
        g.telephone_sabet = data['telephone_sabet']
        g.save()
        admin_infos2['msg'] = ""
        mymessage = "ویرایش اطلاعات با موفقیت انجام شد"
        admin_infos2['mymessage'] = mymessage

        admin_infos2['name'] = data['name']
        admin_infos2['phoneNumber'] = data['phoneNumber']
        admin_infos2['codeMelli'] = data['codeMelli']
        admin_infos2['userName'] = data['userName']
        admin_infos2['password'] = data['password']
        admin_infos2['address'] = data['address']
        admin_infos2['email'] = data['email']
        admin_infos2['telephone_sabet'] = data['telephone_sabet']
        return render(request, "editadmin.html", admin_infos2)


# order_infos2 = {}
# def edit_order(request):
#     mymessage = ""
#     if request.method == "GET":
#         # orderEditID = request.GET.get('editID', None)
#         # order_infos2['orderID'] = orderEditID
#         # try:
#         #     o = customer_order.objects.get(orderID = order_infos2['orderID'])
#         # except customer_order.DoesNotExist:
#         #     return render(request, "editinfos.html", order_infos2)
#         # order_infos2['mymessage'] = mymessage
#         # order_infos2['U_userID'] = o.U_userID
#         # order_infos2['good_description'] = o.good_description
#         # order_infos2['color_description'] = o.color_description
#         # order_infos2['design_description'] = o.design_description
#         # order_infos2['width'] = o.width
#         # order_infos2['length'] =o.length
#         # order_infos2['thickness'] = o.thickness
#         # order_infos2['count'] = o.count
#         # order_infos2['registration_date'] = o.registration_date
#         # order_infos2['orderID'] =o.orderID
#         # order_infos2['orderNumber'] =o.orderNumber
#         # order_infos2['Order_Status'] =o.Order_Status
#         # order_infos2['text_adminToadmin'] =o.text_adminToadmin
#         # order_infos2['text_adminTouser'] =o.text_adminTouser
#         # order_infos2['tozihat_1order'] =o.tozihat_1order
#         # order_infos2['tozihat_5orders'] =o.tozihat_5orders
#         # return render(request, "editinfos.html", order_infos2 )

#         U_id = request.GET.get('userID', None)
#         order_infos2['userID'] = U_id
#         user_orders = customer_order.objects.filter(U_userID = int(U_id))
#         numOfOrders = []
#         for order in user_orders:
#             if not order.orderNumber  in numOfOrders:
#                 numOfOrders.append(order.orderNumber)
#         order_infos2['numOfOrders'] = numOfOrders
#         return render(request, "editOrder2.html", order_infos2)
#     if request.method == "POST":
#         data = request.POST
#         try:
#             u = User.objects.get(userID = user_infos2['userID'])
#         except User.DoesNotExist:
#             return render(request, "editinfos.html", user_infos2)        
#         try:
#             g = User.objects.get(userName = u.userName)
#         except User.DoesNotExist:
#             mymessage = "نام کاربری اشتباه وارد شده. لطفا مجدد تلاش کنید"
#             user_infos2['mymessage'] = mymessage
#             return render(request, "editinfos.html", user_infos2)


#         if (User.objects.filter(phoneNumber = data['phoneNumber']).exists() and int(User.objects.get(phoneNumber = data['phoneNumber']).userID) != int(user_infos2['userID'])):
#             sbtmessage = "این شماره تلفن قبلا در سامانه ثبت شده"
#             user_infos2['mymessage'] = ""
#             user_infos2['msg'] = sbtmessage
#             return render(request, "editinfos.html",user_infos2)
#         if (User.objects.filter(codeMelli = data['codeMelli']).exists() and int(User.objects.get(codeMelli = data['codeMelli']).userID) != int(user_infos2['userID'])):
#             sbtmessage = "این کد ملی قبلا در سامانه ثبت شده"
#             user_infos2['mymessage'] = ""
#             user_infos2['msg'] = sbtmessage
#             return render(request, "editinfos.html",user_infos2)
#         if (User.objects.filter(userName = data['userName']).exists() and int(User.objects.get(userName = data['userName']).userID) != int(user_infos2['userID'])):
#             sbtmessage = "این نام کاربری قبلا در سامانه ثبت شده"
#             user_infos2['mymessage'] = ""
#             user_infos2['msg'] = sbtmessage
#             return render(request, "editinfos.html",user_infos2)
#         # if User.objects.filter(email = data['email']).exists():
#         #     sbtmessage = "این ایمیل قبلا در سامانه ثبت شده"
#         #     return render(request, "sabtenam.html",{'msg': sbtmessage})
#         if (User.objects.filter(telephone_sabet = data['telephone_sabet']).exists() and int(User.objects.get(telephone_sabet = data['telephone_sabet']).userID) != int(user_infos2['userID'])):
#             sbtmessage = "این تلفن قبلا در سامانه ثبت شده"
#             user_infos2['mymessage'] = ""
#             user_infos2['msg'] = sbtmessage
#             return render(request, "editinfos.html",user_infos2)
#         g.name = data['name']
#         g.phoneNumber = data['phoneNumber']
#         g.codeMelli = data['codeMelli']
#         g.userName = data['userName']
#         g.password = data['password']
#         g.address = data['address']
#         g.email = data['email']
#         g.telephone_sabet = data['telephone_sabet']
#         g.save()
#         user_infos2['msg'] = ""
#         mymessage = "ویرایش اطلاعات با موفقیت انجام شد"
#         user_infos2['mymessage'] = mymessage

#         user_infos2['name'] = data['name']
#         user_infos2['phoneNumber'] = data['phoneNumber']
#         user_infos2['codeMelli'] = data['codeMelli']
#         user_infos2['userName'] = data['userName']
#         user_infos2['password'] = data['password']
#         user_infos2['address'] = data['address']
#         user_infos2['email'] = data['email']
#         user_infos2['telephone_sabet'] = data['telephone_sabet']
#         return render(request, "editinfos.html", user_infos2)


def show_details_order(request):
    if request.method=='GET':
        sku = request.GET.get('sku')
        if not sku:
            return render(request,  "showDetail.html")
        else:
            result = customer_order.objects.filter(orderNumber = sku).order_by('orderID')
            for r in result:
                tozih_kol = r.tozihat_5orders
                adminToUser = r.text_adminTouser
                note = r.text_adminToadmin
                break
            return render(request, "showDetail.html" ,{'result': result, 'tozih_kol': tozih_kol, 'adminToUser': adminToUser, 'note': note})
    if request.method == "POST":
        data = request.POST


def show_details_order2_user(request):
    if request.method=='GET':
        sku = request.GET.get('sku')
        if not sku:
            return render(request,  "showEditDetails.html")
        else:
            result = customer_order.objects.filter(orderNumber = sku).order_by('orderID')
            resultcount = len(result)
            tozih_kol = ""
            adminToUser = ""
            tarikh = ""
            vaziat =""
            orderNum = 0
            for r in result:
                tozih_kol = r.tozihat_5orders
                adminToUser = r.text_adminTouser
                tarikh = r.registration_date
                vaziat = r.Order_Status
                orderNum = r.orderNumber
                break
            goodoptions = Good.objects.all()
            designoptions = Design.objects.all()
            coloroptions = Color.objects.all()
            myContext = {}
            myContext['result'] = result
            myContext['tozih_kol'] = tozih_kol
            myContext['adminToUser'] = adminToUser
            myContext['tarikh'] = tarikh
            myContext['vaziat'] = vaziat
            myContext['goodoptions'] = goodoptions
            myContext['designoptions'] = designoptions
            myContext['coloroptions'] = coloroptions
            myContext['resultcount'] = resultcount
            myContext['orderNum'] = orderNum
            myContext['mmsg'] = ""
            # myContext['userID'] = user_id['u_id']
            # try:
            #     u = User.objects.get(userID = myContext['userID'])
            # except User.DoesNotExist:
            #     return render(request, "showEditDetails.html", myContext) 
            # myContext['userID'] = user_id['u_id']
            return render(request, "showEditDetails.html" ,myContext)
    if request.method == "POST":
        data = request.POST
        DD = datetime2jalali(datetime.now()).strftime('14%y-%m-%d %H:%M:%S')
        resultcount = data['resultcount']
        orderNum = data['orderNum']
        O_status = ""
        for i in range (1, int(resultcount)+1):
            order_id = "orderID" + str(i)
            good_desc = "good_description" + str(i)
            color_desc = "color_description" + str(i)
            design_desc = "design_description" + str(i)
            width = "width" + str(i)
            length = "length" + str(i)
            thickness = "thickness" + str(i)
            count = "count" + str(i)
            tozihat_1order = "tozihat_1order" + str(i)

            try:
                o = customer_order.objects.get(orderID = data[order_id])
            except customer_order.DoesNotExist:
                break
            cc = data[count]
            if cc == "" or cc == "0" or int(cc) == 0:
                o.delete()
            else:
                o.good_description = data[good_desc]
                o.color_description = data[color_desc]
                o.design_description = data[design_desc]
                ww = data[width]
                if ww == "":
                    ww = 0
                o.width = ww
                ll = data[length]
                if ll == "":
                    ll = 0
                o.length = ll
                tt = data[thickness]
                if tt == "":
                    tt = 0
                o.thickness = tt
                o.count = cc
                O_status = o.Order_Status
                if (O_status == "sabt shode" or O_status == "rad shode"):
                    o.Order_Status = "sabt shode"
                    o.registration_date = DD
                o.tozihat_1order = data[tozihat_1order]
                o.tozihat_5orders = data['tozihat_5orders']
                o.save()
        result = customer_order.objects.filter(orderNumber = orderNum).order_by('orderID')
        resultcount = len(result)
        tozih_kol = ""
        adminToUser = ""
        tarikh = ""
        vaziat =""
        for r in result:
            tozih_kol = r.tozihat_5orders
            adminToUser = r.text_adminTouser
            tarikh = r.registration_date
            vaziat = r.Order_Status
            break
        goodoptions = Good.objects.all()
        designoptions = Design.objects.all()
        coloroptions = Color.objects.all()
        myContext = {}
        myContext['result'] = result
        myContext['tozih_kol'] = tozih_kol
        myContext['adminToUser'] = adminToUser
        myContext['tarikh'] = tarikh
        myContext['vaziat'] = vaziat
        myContext['goodoptions'] = goodoptions
        myContext['designoptions'] = designoptions
        myContext['coloroptions'] = coloroptions
        myContext['resultcount'] = resultcount
        myContext['orderNum'] = orderNum
        if (O_status == "sabt shode" or O_status == "rad shode" or O_status == ""):
            myContext['mmsg'] = "ویرایش با موفقیت انجام شد"
        else:
            myContext['mmsg'] = "ویرایش انجام نشد. فقط سفارشات در حال بررسی و یا رد شده قابل ویرایش هستند"
        return render(request, "showEditDetails.html" ,myContext)


def new_row_order(request):
    if request.method=='GET':
        orderNum = request.GET.get('orderNum', None)
        if orderNum == None:
            return render(request,  "newRowOrder.html")
        else:
            result = customer_order.objects.filter(orderNumber = orderNum).order_by('orderID')
            resultcount = len(result) +1
            try:
                lastOrder = customer_order.objects.order_by('-orderID')[0]
                maxID = lastOrder.orderID
            except IndexError:
                maxID = 0

            o_new_ID = maxID+1
            tozih_kol = ""
            adminToUser = ""
            tarikh = ""
            vaziat =""
            orderNum = 0
            userID=0
            for r in result:
                tozih_kol = r.tozihat_5orders
                adminToUser = r.text_adminTouser
                tarikh = r.registration_date
                vaziat = r.Order_Status
                orderNum = r.orderNumber
                userID = r.U_userID
                break
            goodoptions = Good.objects.all()
            designoptions = Design.objects.all()
            coloroptions = Color.objects.all()
            myContext = {}
            myContext['result'] = result
            myContext['o_new_ID'] = o_new_ID
            myContext['tozih_kol'] = tozih_kol
            myContext['adminToUser'] = adminToUser
            myContext['tarikh'] = tarikh
            myContext['vaziat'] = vaziat
            myContext['goodoptions'] = goodoptions
            myContext['designoptions'] = designoptions
            myContext['coloroptions'] = coloroptions
            myContext['resultcount'] = resultcount
            myContext['orderNum'] = orderNum
            myContext['userID'] = userID
            myContext['mmsg'] = ""
            # myContext['userID'] = user_id['u_id']
            # try:
            #     u = User.objects.get(userID = myContext['userID'])
            # except User.DoesNotExist:
            #     return render(request, "showEditDetails.html", myContext) 
            # myContext['userID'] = user_id['u_id']
            return render(request, "newRowOrder.html" ,myContext)
    if request.method == "POST":
        data = request.POST
        DD = datetime2jalali(datetime.now()).strftime('14%y-%m-%d %H:%M:%S')
        resultcount = data['resultcount']
        orderNum = data['orderNum']
        O_status = ""
        for i in range (1, int(resultcount)):
            order_id = "orderID" + str(i)
            good_desc = "good_description" + str(i)
            color_desc = "color_description" + str(i)
            design_desc = "design_description" + str(i)
            width = "width" + str(i)
            length = "length" + str(i)
            thickness = "thickness" + str(i)
            count = "count" + str(i)
            tozihat_1order = "tozihat_1order" + str(i)

            try:
                o = customer_order.objects.get(orderID = data[order_id])
            except customer_order.DoesNotExist:
                break
            cc = data[count]
            if cc == "" or cc == "0":
                o.delete()
            else:
                o.good_description = data[good_desc]
                o.color_description = data[color_desc]
                o.design_description = data[design_desc]
                ww = data[width]
                if ww == "":
                    ww = 0
                o.width = ww
                ll = data[length]
                if ll == "":
                    ll = 0
                o.length = ll
                tt = data[thickness]
                if tt == "":
                    tt = 0
                o.thickness = tt
                o.count = cc
                O_status = o.Order_Status
            if (O_status == "sabt shode" or O_status == "rad shode" or O_status == ""):
                o.Order_Status = "sabt shode"
                o.registration_date = DD
            o.tozihat_1order = data[tozihat_1order]
            o.tozihat_5orders = data['tozihat_5orders']
            o.save()


        order_id = "orderID" + str(resultcount)
        good_desc = "good_description" + str(resultcount)
        color_desc = "color_description" + str(resultcount)
        design_desc = "design_description" + str(resultcount)
        width = "width" + str(resultcount)
        length = "length" + str(resultcount)
        thickness = "thickness" + str(resultcount)
        count = "count" + str(resultcount)
        tozihat_1order = "tozihat_1order" + str(resultcount)
        ww = data[width]
        if (data[width] == ""):
            ww=0
        ll = data[width]
        if (data[length] == ""):
            ll=0
        tt = data[thickness]
        if (data[thickness] == ""):
            tt=0
        if (data[count] != "" and data[count] != 0 and data[count] != "0" and int(data[count]) != 0):
            newOrderRow = customer_order.objects.create(U_userID = data['userID'], good_description=data[good_desc],color_description=data[color_desc] ,design_description=data[design_desc] , width=ww , length=ll , thickness=tt , count=data[count] ,registration_date=DD,Order_Status = "sabt shode" , orderNumber=orderNum, tozihat_1order = data[tozihat_1order], tozihat_5orders = data['tozihat_5orders'])
            newOrderRow.save()

        result = customer_order.objects.filter(orderNumber = orderNum).order_by('orderID')
        resultcount = len(result)
        for r in result:
            tozih_kol = r.tozihat_5orders
            adminToUser = r.text_adminTouser
            tarikh = r.registration_date
            vaziat = r.Order_Status
            break
        goodoptions = Good.objects.all()
        designoptions = Design.objects.all()
        coloroptions = Color.objects.all()
        myContext = {}
        myContext['result'] = result
        myContext['tozih_kol'] = tozih_kol
        myContext['adminToUser'] = adminToUser
        myContext['tarikh'] = tarikh
        myContext['vaziat'] = vaziat
        myContext['goodoptions'] = goodoptions
        myContext['designoptions'] = designoptions
        myContext['coloroptions'] = coloroptions
        myContext['resultcount'] = resultcount
        myContext['orderNum'] = orderNum
        if (O_status == "sabt shode" or O_status == "rad shode"):
            myContext['mmsg'] = "ویرایش با موفقیت انجام شد"
        else:
            myContext['mmsg'] = "ویرایش انجام نشد. فقط سفارشات در حال بررسی و یا رد شده قابل ویرایش هستند"
        return render(request, "showEditDetails.html" ,myContext)

