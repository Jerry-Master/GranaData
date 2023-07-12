from django.shortcuts import redirect

def redirect_to_create_user(request):
    return redirect('/simpleapp/create_user')
