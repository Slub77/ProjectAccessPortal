
from django.conf import settings

from P4Connection import P4ConnectionAsServiceUser
from models import PAUser, PAProject, PAUserProjectAccess, PAGroupProjectAccess

import logging
logger = logging.getLogger(__name__)

def construct_protection_line(p4_path, p4_access_group_name):
    return 'write group %s * %s/...' % (p4_access_group_name, p4_path)

def add_p4_protection_line(p4, p4_protection_line):

    protections = p4.read_protect()

    if p4_protection_line in protections:
        logger.warning('Attempted to add P4 protection line "%s" which already existed in protect table; operation ignored', p4_protection_line)
    else:
        protections.append(str(p4_protection_line))

    p4.write_protect(protections)

def remove_p4_protection_line(p4, p4_protection_line):

    protections = p4.read_protect()

    try:
        protections.remove(p4_protection_line)
    except:
        logger.warning('Attempted to remove P4 protection line "%s" which did not exist in protect table; operation ignored', p4_protection_line)

    p4.write_protect(protections)

def create_project_standard_files_in_p4(p4, project_root):

    file_name = 'readme.txt'
    local_root = 'WorkspaceTemplates/NewProject'
    local_file = '%s/%s' % (local_root, file_name)
    depot_file = '%s/%s' % (project_root, file_name)

    p4.import_local_file(local_file, depot_file, 'Setting up project-area in %s' % project_root)

def delete_project_standard_files_in_p4(p4, p4_path):
    # TODO implement
    pass

def create_new_project(project_name):

    p4_path = '%s/%s' % (settings.PERFORCE_PROJECT_DEPOT_LOCATION, project_name)
    p4_access_group_name = '%s-%s-ReadWrite' % (settings.PERFORCE_PROJECT_GROUP_PREFIX, project_name)

    project = PAProject.objects.create(name=project_name, p4_path=p4_path, p4_access_group_name=p4_access_group_name)

    with P4ConnectionAsServiceUser() as p4:

        add_p4_protection_line(p4, construct_protection_line(p4_path, p4_access_group_name))
        create_project_standard_files_in_p4(p4, p4_path)

    return project

def delete_project(project):

    with P4ConnectionAsServiceUser() as p4:

        remove_p4_protection_line(p4, construct_protection_line(project.p4_path, project.p4_access_group_name))

        # Delete group in P4
        # TODO: perhaps check for group existence before deleting? That will allow for ignoring a narrower range of exceptions
        try:
            p4.delete_group(project.p4_access_group_name)
        except:
            pass

        delete_project_standard_files_in_p4(p4, project.p4_path)

    project.delete()

    pass

def add_user_to_project(project, user):

    with P4ConnectionAsServiceUser() as p4:

        project_access = PAUserProjectAccess.objects.create(project=project, user=user)
        project_access.save()
        p4.add_user_to_group(project.p4_access_group_name, str(user.p4_user_name))
        return project_access

def remove_user_from_project(project_access):

    with P4ConnectionAsServiceUser() as p4:

        p4.remove_user_from_group(project_access.project.p4_access_group_name, project_access.user.p4_user_name)
        project_access.delete()

def add_group_to_project(project, group):

    with P4ConnectionAsServiceUser() as p4:

        project_access = PAGroupProjectAccess.objects.create(project=project, group=group)
        project_access.save()
        p4.add_subgroup_to_group(project.p4_access_group_name, str(group.name))
        return project_access

def remove_group_from_project(project_access):

    with P4ConnectionAsServiceUser() as p4:

        p4.remove_subgroup_from_group(project_access.project.p4_access_group_name, project_access.group.name)
        project_access.delete()
