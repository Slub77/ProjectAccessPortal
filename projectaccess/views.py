from django.http import HttpResponse
from django.template import RequestContext, loader

import random

def generate_random_users(count):

    def generate_random_user():
        id = random.randint(0, 999999)
        return {
            'id': str(id),
            'name': 'user_name_' + str(id),
            'email': 'firstname_lastname_' + str(id)
            }

    users = [generate_random_user() for i in range(count)]
    
    return users
            

def index(request):
    users = generate_random_users(10)
    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': users,
    })
    return HttpResponse(template.render(context))
