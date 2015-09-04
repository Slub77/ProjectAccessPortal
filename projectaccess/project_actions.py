
from p4access import P4Connection
from models import PAUser, PAProject

def create_new_project(project_name):

    p4_path = '//Projects2/%s' % project_name
    p4_access_group_name = 'Projects2-%s-ReadWrite' % project_name

    project = PAProject.objects.create(name=project_name, p4_path=p4_path, p4_access_group_name=p4_access_group_name)

#    with P4Connection('localhost', '1666', 'kalms') as p4:
#
#        # TODO: update protections in P4
#        update_p4_protections()

    return project

def delete_project(project):

    project.delete()

    with P4Connection('localhost', '1666', 'kalms') as p4:

        # Delete group in P4
        # TODO: perhaps check for group existence before deleting? That will allow for ignoring a narrower range of exceptions
        try:
            p4.delete_group(project.p4_access_group_name)
        except:
            pass

#        # TODO: update protections in P4
#        update_p4_protections()

    pass
