from django.http import HttpResponse
from django.template import RequestContext, loader

import random
from P4 import P4, P4Exception

from models import MetaUser

def index(request):

    from updateldap import updateldap
    updateldap()

    from updatep4 import updatep4
    updatep4()

    from updatemeta import updatemeta
    updatemeta()

    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': MetaUser.objects.all(),
    })
    return HttpResponse(template.render(context))
