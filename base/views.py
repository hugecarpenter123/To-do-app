from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class CustomRegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        return super(CustomRegisterView, self).get(*args, **kwargs)




class TaskList(LoginRequiredMixin, ListView):
    model = Task


    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['object_list'] = self.request.user.task_set.all()
        context['object_list'] = context['object_list'].filter(user=self.request.user)
        context['count'] = context['object_list'].filter(complete=False)

        search_input = self.request.GET.get('search-text', '')
        if search_input:
            context['object_list'] = context['object_list'].filter(
                Q(description__icontains=search_input) |
                Q(title__icontains=search_input)
            )
            context['searched'] = search_input


        return context

    def get(self, request ,*args, **kwargs):
        return super(TaskList, self).get(request, *args, **kwargs)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    pk_url_kwarg = 'id'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        print("------form valid call -------------")
        print('form: {}, typeof {}'.format(form, type(form)))
        print('form.instance: {}, typeof {}'.format(form.instance, type(form.instance)))
        print('form.instance.user: {}, typeof {}'.format(form.instance.user, type(form.instance.user)))
        form.instance.user = self.request.user
        print("-----------------------------------")
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
