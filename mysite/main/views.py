import json
import datetime

import pandas as pd
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Func, F
import csv

from .forms import *
from .models import *


# Create your views here.
def homepage(request):
    return render(request=request, template_name="main/group_trans.html", context={"frlist": MyUser.objects.all})


def userpage(request):
    user = MyUser.objects.get(username=request.user)
    return render(request=request, template_name="main/user.html",
                  context={"friendtrans": FriendT.objects.filter(urname=user.username).values('fdname').annotate(
                      netmoney=Sum('money')), "users": MyUser.objects.all})


def friendspage(request):
    user = MyUser.objects.get(username=request.user)
    return render(request=request, template_name="main/friends.html",
                  context={"friendtrans": FriendT.objects.filter(urname=user.username).values('fdname').annotate(
                      netmoney=Sum('money')), "users": MyUser.objects.all})


def flist(request):
    user = MyUser.objects.get(username=request.user)
    return render(request=request, template_name="main/FTlist.html",
                  context={"ftrans": FriendT.objects.filter(urname=user.username).order_by('time'),
                           "users": MyUser.objects.all})


def thokka(request, name):
    user = MyUser.objects.get(username=request.user)
    return render(request=request, template_name="main/FTlist.html",
                  context={"ftrans": FriendT.objects.filter(urname=user.username, fdname=name).order_by('time'),
                           "users": MyUser.objects.all})


def register(request):
    if request.method == "POST":
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created : {username}")
            # login(request,user)
            # messages.info(request,f"You are logged in as : {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = MyForm
    return render(request,
                  "main/input.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as : {username}")
                return redirect("main:userpage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})


def account(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = PasswordChangeForm(request.user)
    return render(request,
                  "main/account.html",
                  context={"form": form})


def get_user_profile(request):
    return render(request, 'main/user_profile.html')


def friends_form(request):
    if request.method == "POST":
        form = FriendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                friend = MyUser.objects.get(username=name)
                FriendT.add_friend(request.user, friend)
                return redirect("main:userpage")
            except MyUser.DoesNotExist:
                messages.error(request, "User doesn't exist")
        else:
            messages.error(request, "Invalid username")
    form = FriendForm()
    return render(request,
                  "main/add_friend.html",
                  {"form": form})


def transaction_form(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            friend = form.cleaned_data.get('friend')
            money = form.cleaned_data.get('money')
            notes = form.cleaned_data.get('notes')
            tag = form.cleaned_data.get('tag')
            display_type = request.POST['paid']
            split_type = form.cleaned_data.get('split')
            ys = form.cleaned_data.get('ys')
            fs = form.cleaned_data.get('fs')
            if display_type == "You paid":
                if split_type:
                    if form.data['fs'] and form.data['ys']:
                        money = fs
                    else:
                        messages.error(request, "Specify the amounts")
                else:
                    if form.data['ys'] or form.data['fs']:
                        messages.error(request, "Please select Split by amounts if you want to specify amounts")
                    else:
                        money = money / 2
            elif display_type == "Paid by friend":
                if split_type:
                    if form.data['fs'] and form.data['ys']:
                        money = -ys
                    else:
                        messages.error(request, "Specify the amounts")
                else:
                    if form.data['ys'] or form.data['fs']:
                        messages.error(request, "Please select Split by amounts if you want to specify amounts")
                    else:
                        money = -money / 2
            FriendT.add_transaction(request.user, friend, money, notes, tag)
            return redirect("main:userpage")
        else:
            messages.error(request, "Invalid Friend")
    form = TransactionForm()
    return render(request,
                  "main/trans.html",
                  {"form": form})


def insight(request):
    if request.method == "POST":
        start = datetime.strptime(request.POST['start'], '%Y-%m-%d').strftime('%x')
        end = datetime.strptime(request.POST['end'], '%Y-%m-%d').strftime('%x')
        user = MyUser.objects.get(username=request.user)
        kavali = FriendT.objects.filter(time__lte=end, time__gte=start, urname=user.username).exclude(tag="friend_creation")
        mydata = {}
        piedata = {}
        tdata = {}
        ddata = {}
        tot = 0
        taken = 0

        for entry in kavali:
            if entry.money > 0:
                if entry.fdname in mydata:
                    mydata[entry.fdname][0] += entry.money
                    tot += entry.money
                else:
                    mydata[entry.fdname] = [entry.money, 0]
                    tot += entry.money
            elif entry.money < 0:
                if entry.fdname in mydata:
                    mydata[entry.fdname][1] -= entry.money
                    tot -= entry.money
                    taken -= entry.money 
                else:
                    mydata[entry.fdname] = [0, -entry.money]
                    tot -= entry.money
                    taken -= entry.money

        for entry in kavali:
            if entry.fdname in piedata:
                piedata[entry.fdname] += abs(entry.money)
            else:
                piedata[entry.fdname] = abs(entry.money)

        for entry in kavali:
            if entry.tag in tdata:
                if not (entry.tag == "friend_creation"):
                    tdata[entry.tag] += abs(entry.money)
            else:
                if not (entry.tag == "friend_creation"):
                    tdata[entry.tag] = abs(entry.money)

        for entry in kavali:
            if entry.tag in ddata:
                if not (entry.tag == "friend_creation"):
                    if entry.time in ddata[entry.tag]:
                        ddata[entry.tag][entry.time] += entry.money
                    else:
                        ddata[entry.tag][entry.time] = entry.money
            else:
                if not (entry.tag == "friend_creation"):
                    ddata[entry.tag] = {entry.time: entry.money}

        categories = list()
        categories1 = list()
        categories2 = list()
        survived_series_data = list()
        not_survived_series_data = list()
        friends = list()
        tags = list()
        timedata = {}
        timedata1 = {}
        time_list = list()

        def get_model_fields(model):
            return FriendT._meta.fields

        with open('history.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([ 'Transaction_id' , 'username' , 'friendname' ,'money' , 'description' ,'tag','date'])
            # write your header first
            for obj in kavali:
                writer.writerow(getattr(obj, field.name) for field in get_model_fields(FriendT))

        data = pd.read_csv('history.csv')
        data_html = data.to_html()

        for entry, mon in mydata.items():
            categories.append(entry)
            survived_series_data.append(mon[0])
            not_survived_series_data.append(mon[1])

        for entry, mon in piedata.items():
            categories1.append(entry)
            friends.append(mon)

        for entry, mon in tdata.items():
            categories2.append(entry)
            tags.append(mon)

        for entry, mon in ddata.items():
            for pi, val in ddata[entry].items():
                if entry in timedata:
                    time_list.append(pi)
                    timedata1[entry].append(val)
                else:
                    time_list.append(pi)
                    timedata1[entry] = [val]

        if not ("Restaurant" in timedata1):
            timedata1["Restaurant"] = [0]
        if not ("Cinema" in timedata1):
            timedata1["Cinema"] = [0]
        if not ("Travel" in timedata1):
            timedata1["Travel"] = [0]
        if not ("Others" in timedata1):
            timedata1["Others"] = [0]

        survived_series = {
            'name': 'Lent',
            'data': survived_series_data,
            'color': 'green'
        }

        not_survived_series = {
            'name': 'Borrowed',
            'data': not_survived_series_data,
            'color': 'red'
        }

        chart = {
            'chart': {'type': 'bar'},
            'plotOptions': {
                'series': {
                    'stacking': 'normal'
                }
            },
            'title': {'text': 'Lent and Borrowed amounts friends wise'},
            'xAxis': {'categories': categories},
            'series': [survived_series, not_survived_series]
        }

        chart1 = {
            'chart': {'type': 'pie'},
            'title': {'text': 'Pie chart for expenditure among friends'},
            'series': [{
                'name': 'Total Transaction Amount',
                'data': list(map(lambda row1, row2: {'name': row1, 'y': row2}, categories1, friends))
            }]
        }

        chart2 = {
            'chart': {'type': 'area'},
            'title': {'text': 'Pie chart for expenditure with tags'},
            'xAxis': {
                'categories': time_list
            },
            'series': [{
                'name': 'Money spent on Restaurants',
                'data': timedata1["Restaurant"]
            }, {
                'name': 'Money spent on Cinemas',
                'data': timedata1["Cinema"]
            }, {
                'name': 'Money spent on Travels',
                'data': timedata1["Travel"]
            }, {
                'name': 'Miscellaneous Transactions',
                'data': timedata1["Others"]
            }]
        }

        chart3 = {
            'chart': {'type': 'pie'},
            'title': {'text': 'Pie chart for expenditure in different areas'},
            'series': [{
                'name': 'Total Transaction Amount',
                'data': list(map(lambda row1, row2: {'name': row1, 'y': row2}, categories2, tags))
            }]
        }

        perc = taken*100//tot
        dump = json.dumps(chart)
        dump1 = json.dumps(chart1)
        dump2 = json.dumps(chart2)
        dump3 = json.dumps(chart3)

        response = render(request=request,
                          template_name="main/insight.html",
                          context={"chart1": dump1, "chart2": dump2, "chart": dump, "chart3": dump3,'loaded_data': data_html,
                                    "chart4": perc})

    return response
    # return "%s?%s?%s" % (redirect('insight', args=(start, end,)))

# @login_required(login_url='login_request')
# def insight(request, start, end):
#     # start = datetime.strptime(request.POST['start'], '%Y-%m-%d').strftime('%m/%d/%y')
#     # end = datetime.strptime(request.POST['end'], '%Y-%m-%d').strftime('%m/%d/%y')
#     user = MyUser.objects.get(username=request.user)
#     data = FriendT.objects.filter(urname=user.username)
#     mydata = {}
#     for entry in data:
#         if entry.money > 0:
#             if entry.fdname in mydata:
#                 mydata[entry.fdname][0] += entry.money
#             else:
#                 mydata[entry.fdname] = [entry.money, 0]
#         elif entry.money < 0:
#             if entry.fdname in mydata:
#                 mydata[entry.fdname][1] -= entry.money
#             else:
#                 mydata[entry.fdname] = [0, -entry.money]
#
#     print(mydata)
#
#     categories = list()
#     survived_series_data = list()
#     not_survived_series_data = list()
#
#     for entry, mon in mydata.items():
#         categories.append(entry)
#         survived_series_data.append(mon[0])
#         not_survived_series_data.append(mon[1])
#
#     survived_series = {
#         'name': 'Lent',
#         'data': survived_series_data,
#         'color': 'green'
#     }
#
#     not_survived_series = {
#         'name': 'Borrowed',
#         'data': not_survived_series_data,
#         'color': 'red'
#     }
#
#     chart = {
#         'chart': {'type': 'column'},
#         'title': {'text': 'Lent and Borrowed amounts friends wise'},
#         'xAxis': {'categories': categories},
#         'series': [survived_series, not_survived_series]
#     }
#
#     dump = json.dumps(chart)
#
#     return render(request,
#                   "main/insight.html",
#                   context={"chart": dump})



def groupslistpage(request):
    user = MyUser.objects.get(username=request.user)
    return render(request=request, template_name="main/groups.html",
                  context={"grouptrans": GroupTrans.objects.filter(username=user.username).values().annotate(
                      netmoney_owed=Sum('money_gave'),netmoney_owes=Sum('money_took')),
                           "current_user": MyUser.objects.get(username=user.username)})


#check grouppage once
def grouppage(request,group_name):
    user = MyUser.objects.get(username=request.user)
    group_members=set()
    query1=GroupTable.objects.filter(gpname=group_name,username=user.username)
    for members in query1:
        # print(1)
        group_members.add(members.frname)
    # print(group_members)
    return render(request=request,template_name="main/GTlist.html",
                  context={"gtrans": GroupTrans.objects.filter(gpname=group_name,username=user.username).order_by('time'),
                           "group_members":group_members,
                           "groupname":group_name,
                           "gtable": GroupTable.objects.filter(gpname=group_name,username=user.username).annotate(netmoney=Sum('money')).order_by('time')})


def group_form(request):
    if request.method == "POST":
        form=GroupForm(request.POST)
        if form.is_valid():
            group_name=form.cleaned_data.get('group')
            members=form.cleaned_data.get('friends')
            members_list=members.split(',')
            # print(members_list)
            user=request.user
            GroupTrans.add_group(user.username,group_name,members_list)
            members_list.append(user.username)
            # print(type(members_list[len(members_list)-1]))
            for member1 in members_list:
                # member1a=MyUser.objects.get(username=member1)
                for member2 in members_list:
                    if member1!=member2:
                        # member2a=MyUser.objects.get(username=member2)
                        # print('tug time')
                        # print(member1a.username)
                        GroupTable.add_group(group_name,member1,member2)
            return redirect("main:userpage")
        else:
            messages.error(request,"Fill the form properly")
    form=GroupForm()
    return render(request,"main/add_group.html",{"form": form})



def group_transaction_form(request,thisgroup_name):
    if request.method=="POST":
        form=ActivityTransactionForm(request.POST)
        if form.is_valid():
            # saveform=form.save()
            print("possible")
            # activity_name = form.cleaned_data.get('activity')
            # few_users=form.cleaned_data.get('users')
            #
            # money = form.cleaned_data.get('money')
            # amount_paid=form.cleaned_data.get('friends_and_money_paid_by_each')
            # split_choice=form.cleaned_data.get('split')
            # l1 = amount_paid.split(";")
            # l2 = []
            # if split_choice=="Split Equally":
            #     splitting_money=[]
            #
            #     # for ele in l1:
            #     #     dummy1 = ele.split(",")
            #     #     dummy1[1] = int(dummy1[1])
            #     #     l2.append(dummy1)
            # # all_users=form.cleaned_data.get('users')
            # else:
            #     amount_split=cleaned_data.get('amount_string')
            #     splitting_money=splitunequally(user.username,amount_split,money)#current_user amount entered in the end
            #     for entry in splitting_money:
            #         key,value=entry[0],entry[1]
            #
            # all_users=[]
            # for lis in splitting_money:
            #     all_users.append(lis[0])
            # tag=form.cleaned_data.get('tag')
            # # description=form.cleaned_data.get('Description')
            #
            # for user1 in all_users:
            #     GroupTrans.add_activity_and_user(thisgroup_name,activity_name,user1,tag,money_dict[user1][0],money_dict[user1][1])
            # return redirect("main:userpage")
        else:
            return render(request,"main/add_activity_form.html",{"form":form})

def sorting_who_to_give(list1,list2):
    list3=[]#In this list list3[i][0] should get list3[i][2] money from list3[i][1]
    size1=len(list1)
    size2=len(list2)
    p=0
    for i in range(0, size1):
        if list1[i][1] != 0:
            for j in range(p, size2):
                if list1[i][0] != list2[j][0]:
                    m=list1[i][1]-list2[j][1]
                    if m>=0:
                        list[i][1] = m
                        p = p+1
                        list3.append([list1[i][0],list1[i][1],m])
                        break
                    # else if m==0:
                    #     list[i][1]=0
                    #     p++
                    #     break
                    else:
                        list2[i][j]=-m
                        list1[i][1]=0
                        list3.append([list1[i][0], list1[i][1], -m])
                        break
        # else:
    return list3


def splitunequally(user,amount_split,money):
    n1=amount_split(';')
    l2=[]
    sum_others=0
    for ele in n1:
        dummy1 = ele.split(",")
        dummy1[1] = int(dummy1[1])
        sum_others=sum_others+dummy1[1]
        l2.append(dummy1)

    l2.append([user,money-sum_others])
    # amount_split.append([user.username,money-sum_others])
    return l2
    # n1 = self.all_friends_in_activity
    # a = self.amount_list
    # l1 = []
    # if len(a) - len(n1) == 1:
    #     sum = 0
    #     for num in a:
    #         sum = sum + num
    #     if sum == self.money:
    #         l1.append([currentuser, a[0]])
    #         for i in range(1, len(a)):
    #             l1.append([n1[i], amount_list[i]])
    #             return l1
    #     else:
    #         raise forms.ValidationError("Split the money properly")
    # else:
    #     raise forms.ValidationError("Give money spent for each person")


def settleup_ingroup(request,group_name):
    if request.method=="POST":
        form = SettleUpGroup(request.POST)
        if form.is_valid():
            user=request.user
            saveform=form.save()
            users = form.cleaned_data.get('users')
            users_list = users.split(",")
            for member in users_list:
                l1=GroupTable.objects.filter(gpname=group_name,username=user.username,frname=member).aggregate(money_give_take=Sum(money))
                if l1[money_give_take] != 0:
                    GroupTable.add_rows(group_name,user.username,member,-(money_give_take))
                    GroupTable.add_rows(group_name,member,user.username,money_give_take)
                    return redirect("main/settl")#check once here
                elif l1[money_give_take]== 0:
                    return redirect("main/settleupgroup.html")  # check once here
        else:
            return(request,"main/settleupgroup.html",{"form":form})






def leave_delete_group(request,group_name):
    user=request.user
    query1=GroupTable.objects.filter(gpname=group_name,username=user.username).annotate(netmoney=Sum(money))
    query2=GroupTable.objects.filter(gpname=group_name,frname=user.username).annotate(netmoney=Sum(money))








