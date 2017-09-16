import json
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from .models import Todo
from django.core import serializers


def todolist(request):
    todolist = Todo.objects.filter(flag=1)
    finishtodos = Todo.objects.filter(flag=0)
    return render(request, 'todo/simpleTodo.html',
                  {'todolist': todolist,
                           'finishtodos': finishtodos})


def todolist_json(request):
    param_dict = request.GET if request.method=='GET' else request.POST
    todo_priority = param_dict.get('todo_priority', 0)
    task_number = param_dict.get('task_number', 'all')
    task_fetch_order = param_dict.get('task_fetch_order', 'latest')
    task_status = param_dict.get('task_status', None)
    if int(todo_priority) == 0:
        filter_dict = dict(priority__in=[1,2,3])
    else:
        filter_dict = dict(priority=int(todo_priority))
    if task_status:
        filter_dict.update({'flag': int(task_status)})
    if task_fetch_order == 'latest':
        order_by = '-pubtime'
    else:
        order_by = 'pubtime'
    if not task_number or task_number == 'all':
        task_number = None
    else:
        task_number = int(task_number)
    todolist = json.loads(
        serializers.serialize(
            'json', Todo.objects.filter(**filter_dict).all().order_by(order_by)[:task_number], fields=('todo', 'flag', 'priority', 'pubtime'
                                                                                    )
        ))
    # finishtodos = json.loads(
    #     serializers.serialize(
    #         'json', Todo.objects.filter(flag=0).all().order_by('-pubtime'), fields=('todo','flag', 'priority', 'pubtime'
    #             )
    #         ))
    # data =({"todolist": todolist, "finishtodos": finishtodos})
    print todolist
    return JsonResponse(todolist, safe=False)


def do_action(request):
    action = request.GET.get('task_action', None)
    if action:
        number = request.GET.getlist('number', [])
        if number:
            tasks = Todo.objects.all().order_by('-pubtime')
            number.sort(reverse=True)
            ids = []
            for i in number:
                ids.append(tasks[int(i)].id)
            if action == 'complete':
                Todo.objects.filter(id__in=ids).update(flag=0)
            elif action == 'incomplete':
                Todo.objects.filter(id__in=ids).update(flag=1)
            elif action == 'delete':
                Todo.objects.filter(id__in=ids).delete()
    return


def todofinish(request, id=''):
    todo = Todo.objects.get(id=id)
    if todo.flag == '1':
        todo.flag = '0'
        todo.save()
        return HttpResponseRedirect('/todos/')
    todolist = Todo.objects.filter(flag=1)
    return render(request, 'todo/simpleTodo.html',
                           {'todolist': todolist})


def todoback(request, id=''):
    todo = Todo.objects.get(id=id)
    if todo.flag == '0':
        todo.flag = '1'
        todo.save()
        return HttpResponseRedirect('/todos/')
    todolist = Todo.objects.filter(flag=1)
    return render(request, 'todo/simpleTodo.html', {'todolist': todolist})


def tododelete(request, id=''):
    try:
        todo = Todo.objects.get(id=id)
    except Exception:
        raise Http404
    if todo:
        todo.delete()
        return HttpResponseRedirect('/todos/')
    todolist = Todo.objects.filter(flag=1)
    return render(reqeust, 'todo/simpleTodo.html', {'todolist': todolist})


def addTodo(request):
    if request.method == 'POST':
        atodo = request.POST['todo']
        priority = request.POST['priority']
        user = User.objects.get(id='1')
        todo = Todo(user=user, todo=atodo, priority=priority, flag='1')
        todo.save()
        todolist = Todo.objects.filter(flag='1')
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/showtodo.html',
                      {'todolist': todolist,
                               'finishtodos': finishtodos})
    else:
        todolist = Todo.objects.filter(flag=1)
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/simpleTodo.html',
                      {'todolist': todolist,
                               'finishtodos': finishtodos})


def updatetodo(request, id=''):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=id)
        except Exception:
            return HttpResponseRedirect('/todos/')
        atodo = request.POST['todo']
        priority = request.POST['priority']
        todo.todo = atodo
        todo.priority = priority
        todo.save()
        return HttpResponseRedirect('/todos/')
    else:
        try:
            todo = Todo.objects.get(id=id)
        except Exception:
            raise Http404
        return render(request, 'todo/updatetodo.html', {'todo': todo})
