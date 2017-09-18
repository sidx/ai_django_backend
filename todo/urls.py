from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.todolist, name='todo'),
    url(r'^addtodo/$', views.addTodo, name='add'),
    url(r'^addtodojson/$', views.addTodoJson, name='addjson'),
    url(r'^todofinish/(?P<id>\d+)/$', views.todofinish, name='finish'),
    url(r'^todobackout/(?P<id>\d+)/$', views.todoback,  name='backout'),
    url(r'^updatetodo/(?P<id>\d+)/$', views.updatetodo, name='update'),
    url(r'^tododelete/(?P<id>\d+)/$', views.tododelete, name='delete'),
    url(r'^listjson/$', views.todolist_json, name='listjson'),
    url(r'^do_action/$', views.do_action, name='do_action'),
    url(r'^web_hook_test/$', views.web_hook_test, name='web_hook'),
]
