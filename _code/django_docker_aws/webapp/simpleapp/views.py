from django.views.generic.edit import CreateView
from .models import User
from .forms import UserForm

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = '/simpleapp/create_user'
