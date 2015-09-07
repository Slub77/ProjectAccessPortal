
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from models import PAUser, PAProject, PAUserProjectAccess

import logging
logger = logging.getLogger(__name__)

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/projectaccess/')
    return render_to_response('login.html', context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/projectaccess/login')

@login_required
def index(request):

    template = loader.get_template('index.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

@login_required
def users(request):

    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': PAUser.objects.all(),
    })

    return HttpResponse(template.render(context))

@login_required
def projects(request):

    if request.method == 'POST':

        from project_actions import add_user_to_project, remove_user_from_project

        if request.POST['action'] == 'add':
            project_id = request.POST['project_id']
            user_name = request.POST['user_name']
            pa_user = PAUser.objects.get(name=user_name)
            pa_project = PAProject.objects.get(id=project_id)
            add_user_to_project(pa_project, pa_user)
        elif request.POST['action'] == 'remove':
            project_access_id = request.POST['user_with_access_id']
            pa_project_access = PAUserProjectAccess.objects.get(id=project_access_id)
            remove_user_from_project(pa_project_access)
        else:
            raise Exception("Unsupported POST action")

    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects': PAProject.objects.all(),
    })

    return HttpResponse(template.render(context))

@login_required
def import_p4_users(request):

    from p4_import import import_p4_to_django
    import_p4_to_django()

    return users(request)

@login_required
def create_new_project(request):

    template = loader.get_template('create_new_project.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

@login_required
def create_new_project_submit(request):

    name = request.POST['name']

    from project_actions import create_new_project
    create_new_project(name)

    return HttpResponse("New project creation done.")

@login_required
def delete_project(request, id):

    from project_actions import delete_project
    delete_project(PAProject.objects.get(id=id))

    return projects(request)

