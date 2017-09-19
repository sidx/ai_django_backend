import json
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from .models import Todo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from urllib2 import urlopen, Request
from urllib import urlencode

# from urllib.error import HTTPError


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


@csrf_exempt
def addTodoJson(request):
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


@csrf_exempt
def web_hook_test(request, **kwargs):
    print('Request:')
    print(json.dumps(request.POST, indent=4))
    print(json.dumps(kwargs, indent=4))
    res = processRequest(request.POST)

    res = json.dumps(res, indent=4)
    return JsonResponse(res, safe=False)


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


