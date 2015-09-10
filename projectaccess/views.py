
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from models import PAUser, PAProject, PAUserProjectAccess, PAGroup, PAGroupProjectAccess, UserProfile

from P4Connection import P4ConnectionAsServiceUser

import logging
logger = logging.getLogger(__name__)

def login_user(request):

    def create_user_profile(user):
        print str(user.ldap_user.attrs)

        try:
            user_profile = UserProfile.objects.get(user=user)
        except:
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
        return user_profile

    def initialize_user_p4_name(user_profile, ldap_attrs, ldap_attr_name):
#            if not user_profile.p4_name:
                if ldap_attr_name in ldap_attrs:
                    user_profile.p4_username = ldap_attrs[ldap_attr_name][0]
                    user_profile.save()

    def p4_user_exists(user):
        with P4ConnectionAsServiceUser() as p4:
            try:
                print user
                p4.get_user(user.name)
                return True
            except:
                return False

    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            logger.info("user is not None")
            if user.is_active:
                login(request, user)
                user_profile = create_user_profile(user)
                initialize_user_p4_name(user_profile, user.ldap_user.attrs, 'homeDirectory')
                if not p4_user_exists(user):
                    return HttpResponseRedirect('/projectaccess/user/')
                else:
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
def user(request):

    template = loader.get_template('user.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

@login_required
def my_projects(request):

    template = loader.get_template('projects.html')

    pa_user = PAUser.objects.get(name=request.user.username)

    pa_user_project_accesses = PAUserProjectAccess.objects.filter(user=pa_user)
    pa_projects_for_user = PAProject.objects.filter(pauserprojectaccess__in=pa_user_project_accesses)

    pa_group_project_access = PAGroupProjectAccess.objects.filter(group__in=pa_user.pagroup_set.all())
    pa_projects_for_groups = PAProject.objects.filter(pagroupprojectaccess__in=pa_group_project_access)

    pa_projects = pa_projects_for_user | pa_projects_for_groups

    context = RequestContext(request, {
        'projects': pa_projects,
    })

    return HttpResponse(template.render(context))

@login_required
def projects(request):

    if request.method == 'POST':

        from project_actions import add_user_to_project, remove_user_from_project
        from project_actions import add_group_to_project, remove_group_from_project

        if request.POST['action'] == 'add':
            project_id = request.POST['project_id']
            name = request.POST['name']
            pa_project = PAProject.objects.get(id=project_id)
#            try:
            pa_user = PAUser.objects.get(name=name)
            add_user_to_project(pa_project, pa_user)
#            except:
#                pa_group = PAGroup.objects.get(name=name)
#                add_group_to_project(pa_project, pa_group)

        elif request.POST['action'] == 'remove_user':
            project_access_id = request.POST['user_with_access_id']
            pa_project_access = PAUserProjectAccess.objects.get(id=project_access_id)
            remove_user_from_project(pa_project_access)
        elif request.POST['action'] == 'remove_group':
            project_access_id = request.POST['group_with_access_id']
            pa_project_access = PAGroupProjectAccess.objects.get(id=project_access_id)
            remove_group_from_project(pa_project_access)
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

@login_required
def groups(request):

    if request.method == 'POST':

        from group_actions import add_user_to_group, remove_user_from_group

        if request.POST['action'] == 'add':
            group_id = request.POST['group_id']
            user_name = request.POST['user_name']
            pa_user = PAUser.objects.get(name=user_name)
            pa_group = PAGroup.objects.get(id=group_id)
            add_user_to_group(pa_group, pa_user)
        elif request.POST['action'] == 'remove':
            group_id = request.POST['group_id']
            user_id = request.POST['user_id']
            pa_user = PAUser.objects.get(id=user_id)
            pa_group = PAGroup.objects.get(id=group_id)
            remove_user_from_group(pa_group, pa_user)
        else:
            raise Exception("Unsupported POST action")

    template = loader.get_template('groups.html')
    context = RequestContext(request, {
        'groups': PAGroup.objects.all(),
    })

    return HttpResponse(template.render(context))

@login_required
def create_new_group(request):

    template = loader.get_template('create_new_group.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

@login_required
def create_new_group_submit(request):

    name = request.POST['name']

    from group_actions import create_new_group
    create_new_group(name)

    return HttpResponse("New group creation done.")

@login_required
def delete_group(request, id):

    from group_actions import delete_group
    delete_group(PAGroup.objects.get(id=id))

    return groups(request)

