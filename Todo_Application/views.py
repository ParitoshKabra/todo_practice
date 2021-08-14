from django.forms.fields import DateTimeField
from django.shortcuts import redirect, render, HttpResponse
from .models import TodoList, TodoItem
from django import forms
from Todo_Application.forms import DTForms
from datetime import datetime

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret




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
    lst = TodoList.objects.get(id=list_id)
    items = TodoItem.objects.filter(todo_list=lst)
    context = {
        'list':lst,
        'items': items,
    }
    return render(request, "update.html",context)

def update_item(request, id):
    t = TodoItem.objects.get(id=id)
    forms = DTForms()
    forms.fields['title'].initial = t.title
    forms.fields['date_time_input'].initial = t.due_date
    if request.method == "GET":
        context={
            'form':forms,
            'item': t,
            'list': t.todo_list
        }
        return render(request, "updateitem.html",context)
    title = request.POST['title']
    date = request.POST['date_time_input_0']
    date = date.replace('-','/')
    time = request.POST['date_time_input_1']
    datetime_str = date+" "+time
    datetime_object = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
    t.title=title 
    t.checked=False
    if request.POST.get('checked', False):
        t.checked=True
    t.due_date=datetime_object
    t.save()
    return redirect("/")

def create(request):
    if request.method == "GET":
        return render(request, "createlist.html")
    name = request.POST["listname"]
    TodoList.objects.create(list_name=name)
    list_items = TodoList.objects.all()
    items = TodoItem.objects.all()
    context = {
        'todolists': list_items,
        'items': items,
        
    }
    return redirect('/')

def delete(request, list_id):
    TodoList.objects.filter(id=list_id).delete()
    return redirect('/')

def add_item(request, list_id):
    form = DTForms()
    form.fields['checked'].widget = forms.HiddenInput()
    if request.method == "GET": 
        return render(request, "additem.html",{'form':form})
    title = request.POST['title']
    date = request.POST['date_time_input_0']
    date = date.replace('-','/')
    time = request.POST['date_time_input_1']
    datetime_str = date+" "+time
    datetime_object = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
    # datetime_object = get_aware_datetime(datetime_str)
    a2 = TodoItem(title=title, checked=request.POST['checked'], due_date=datetime_object, todo_list=TodoList.objects.get(id=list_id))
    a2.save()
    return redirect('/')

def delete_item(request, id):
    t = TodoItem.objects.get(id=id)
    print(t)
    list_id = t.todo_list.id
    t.delete()
    return redirect(f'/update/{list_id}')



# Create your views here.



