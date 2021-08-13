from django.forms.fields import DateTimeField
from django.shortcuts import redirect, render, HttpResponse
from .models import TodoList, TodoItem
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms import SplitDateTimeField
from datetime import datetime

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret

class DTForms(forms.Form):
    title = forms.CharField(max_length=64)
    date_time_input = SplitDateTimeField(widget=AdminSplitDateTime())


def index(request):

    # return HttpResponse("this is our home page")
    lists = TodoList.objects.all()
    items = TodoItem.objects.all()
    
    for lt in lists:
        for item in items:
            if item.todo_list == lt:
                print(f"{item} {lt}")
    
    context={
        'todolists': lists,
        'items': items
    }
    return render(request, "index.html", context)

def update(request, list_id):
    return HttpResponse("this is our update page")

def create(request):
    if request.method == "GET":
        return render(request, "createlist.html")
    name = request.POST["listname"]
    TodoList.objects.create(list_name=name)
    list_items = TodoList.objects.all()
    items = TodoItem.objects.all()
    context = {
        'todolists': list_items,
        'items': items
    }
    return redirect('/')

def delete(request, list_id):
    TodoList.objects.filter(id=list_id).delete()
    return redirect('/')

def add_item(request, list_id):
    form = DTForms()
    if request.method == "GET": 
        return render(request, "additem.html",{'form':form})
    title = request.POST['title']
    date = request.POST['date_time_input_0']
    date = date.replace('-','/')
    time = request.POST['date_time_input_1']
    datetime_str = date+" "+time
    datetime_object = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
    # datetime_object = get_aware_datetime(datetime_str)
    print(datetime_object.date())
    a2 = TodoItem(title=title, checked=False, due_date=datetime_object, todo_list=TodoList.objects.get(id=list_id))
    a2.save()
    print(a2.due_date)
    print(title, datetime_object)
    return redirect('/')
# Create your views here.


