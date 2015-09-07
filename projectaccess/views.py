
from django.http import HttpResponse
from django.template import RequestContext, loader

from models import PAUser, PAProject

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

#    if request.method == 'POST':
#
#        if request.POST['action'] == 'add':
#            project_id = request.POST['project_id']
#            user_name = request.POST['user_name']
#            ldap_user = LDAPUser.objects.get(uid=user_name)
#            meta_user = MetaUser.objects.get(ldap_user=ldap_user)
#            meta_project = MetaProject.objects.get(id=project_id)
#            add_user_to_project(meta_project, meta_user)
#        elif request.POST['action'] == 'remove':
#            project_id = request.POST['project_id']
#            user_id = request.POST['user_id']
#            meta_user = MetaUser.objects.get(id=user_id)
#            meta_project = MetaProject.objects.get(id=project_id)
#            remove_user_from_project(meta_project, meta_user)
#        else:
#            raise Exception("Unsupported POST action")

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

