
from P4Connection import P4Connection
from models import PAUser, PAProject, PAUserProjectAccess

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

def create_new_project(project_name):

    p4_path = '//Projects2/%s' % project_name
    p4_access_group_name = 'Projects2-%s-ReadWrite' % project_name

    project = PAProject.objects.create(name=project_name, p4_path=p4_path, p4_access_group_name=p4_access_group_name)

    with P4Connection('localhost', '1666', 'kalms') as p4:

        add_p4_protection_line(p4, construct_protection_line(p4_path, p4_access_group_name))

    return project

def delete_project(project):

    with P4Connection('localhost', '1666', 'kalms') as p4:

        remove_p4_protection_line(p4, construct_protection_line(project.p4_path, project.p4_access_group_name))

        # Delete group in P4
        # TODO: perhaps check for group existence before deleting? That will allow for ignoring a narrower range of exceptions
        try:
            p4.delete_group(project.p4_access_group_name)
        except:
            pass

    project.delete()

    pass

def add_user_to_project(project, user):

    with P4Connection('localhost', '1666', 'kalms') as p4:

        project_access = PAUserProjectAccess.objects.create(project=project, user=user)
        project_access.save()
        p4.add_user_to_group(project.p4_access_group_name, str(user.name))
        return project_access

def remove_user_from_project(project_access):

    with P4Connection('localhost', '1666', 'kalms') as p4:

        p4.remove_user_from_group(project_access.project.p4_access_group_name, project_access.user.name)
        project_access.delete()
