
from django.http import HttpResponse
from django.template import RequestContext, loader

from models import PAUser, PAProject, PAUserProjectAccess

import logging
logger = logging.getLogger(__name__)

def index(request):

    template = loader.get_template('index.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def users(request):

    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': PAUser.objects.all(),
    })

    return HttpResponse(template.render(context))

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

def import_p4_users(request):

    from p4_import import import_p4_to_django
    import_p4_to_django()

    return users(request)

def create_new_project(request):

    template = loader.get_template('create_new_project.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def create_new_project_submit(request):

    name = request.POST['name']

    from project_actions import create_new_project
    create_new_project(name)

    return HttpResponse("New project creation done.")

def delete_project(request, id):

    from project_actions import delete_project
    delete_project(PAProject.objects.get(id=id))

    return projects(request)

