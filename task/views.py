from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic

from . import models
from project import models as project_models
from member import models as member_models


class TaskCreationView(LoginRequiredMixin, generic.CreateView):
    template_name = 'task/edit.html'
    model = models.Task
    fields = ['name', 'description']

    # todo permission control

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = project
        self.object.save()
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            urls.reverse('task:detail', kwargs={
                'pk': self.object.pk,
            }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Creation'
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'task/detail.html'
    model = models.Task

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.project.member.all():
            return obj
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task View'
        return context


class TaskAssignedView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'task/assigned.html'
    model = models.Task
    fields = ['assigned']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.project.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['assigned'].queryset = \
            self.get_object().project.member.all()
        return form

    def get_success_url(self):
        return urls.reverse('task:detail', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Assignation'
        return context


class TaskAssignedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/list.html'
    model = models.Task

    def get_queryset(self):
        return self.request.user.task_assigned.all()


class TaskProjectListView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/list.html'
    model = models.Task

    def get_queryset(self):
        project = project_models.Project.objects.get(
            pk=int(self.kwargs['pk_project']))
        if self.request.user in project.member.all:
            return project.task_set.all()
        else:
            raise PermissionDenied


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task/delete.html'
    model = models.Task

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.project.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_success_url(self):
        return urls.reverse('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Deletion'
        return context


class TaskEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'task/edit.html'
    model = models.Task
    fields = ['name', 'description']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.project.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_success_url(self):
        return urls.reverse('task:detail', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Editing'
        return context
