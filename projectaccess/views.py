
from django.http import HttpResponse
from django.template import RequestContext, loader

from models import LDAPUser, MetaUser, MetaProject
from meta_actions import add_user_to_project, remove_user_from_project


def index(request):

    template = loader.get_template('index.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def users(request):

    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': MetaUser.objects.all(),
    })

    return HttpResponse(template.render(context))

def projects(request):

    if request.method == 'POST':

        if request.POST['action'] == 'add':
            project_id = request.POST['project_id']
            user_name = request.POST['user_name']
            ldap_user = LDAPUser.objects.get(uid=user_name)
            meta_user = MetaUser.objects.get(ldap_user=ldap_user)
            meta_project = MetaProject.objects.get(id=project_id)
            add_user_to_project(meta_project, meta_user)
        elif request.POST['action'] == 'remove':
            project_id = request.POST['project_id']
            user_id = request.POST['user_id']
            meta_user = MetaUser.objects.get(id=user_id)
            meta_project = MetaProject.objects.get(id=project_id)
            remove_user_from_project(meta_project, meta_user)
        else:
            raise Exception("Unsupported POST action")

    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects': MetaProject.objects.all(),
    })

    return HttpResponse(template.render(context))

def import_users_and_projects(request):

    from ldap_import import import_ldap_users_to_django
    import_ldap_users_to_django()

    from p4_import import import_p4_to_django
    import_p4_to_django()

    from meta_update import update_all_meta_users_and_projects
    update_all_meta_users_and_projects()

    return index(request)

def update_p4(request):

    from p4_modify import create_default_project_user
    create_default_project_user()

    from p4_modify import create_missing_p4_users
    create_missing_p4_users()

    from p4_modify import update_p4_protect_for_users
    update_p4_protect_for_users()

    return index(request)

def create_new_project(request):

    template = loader.get_template('create_new_project.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def create_new_project_submit(request):

    block = request.POST['block']
    name = request.POST['name']

    from meta_actions import create_new_project
    create_new_project(block, name)

    return HttpResponse("New project creation done.")

def delete_project(request, id):

    from meta_actions import delete_project
    delete_project(MetaProject.objects.get(id=id))

    return projects(request)

