from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import generic

from project import forms
from project import models
from member import models as member_models


class ProjectCreationView(LoginRequiredMixin, generic.CreateView):
    template_name = 'project/edit.html'
    model = models.Project
    fields = ['name', 'description']

    def form_valid(self, form):
        self.object = form.save()
        user = member_models.Member.object.get(
            pk=self.request.user.pk
        )
        self.object.admin.add(user)
        self.object.member.add(user)
        self.object.save()
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            urls.reverse('project:detail', kwargs={
                'pk': self.object.pk,
            }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project Creation'
        return context


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'project/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.member.all():
            return obj
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project View'
        return context


class ProjectMemberView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'project/member.html'
    model = models.Project
    fields = ['member']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['member'].queryset = member_models.Member.object
        return form

    def get_success_url(self):
        return urls.reverse('project:detail', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project Membership'
        return context


class ProjectAdminView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'project/member.html'
    model = models.Project
    fields = ['admin']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['admin'].queryset = self.get_object().member.all()
        return form

    def get_success_url(self):
        return urls.reverse('project:detail', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project Administrator'
        return context


class ProjectAdminListView(LoginRequiredMixin, generic.ListView):
    template_name = 'project/list.html'
    model = models.Project

    def get_queryset(self):
        user = member_models.Member.object.get(pk=self.request.user.pk)
        return user.project_admin.all()


class ProjectMemberListView(LoginRequiredMixin, generic.ListView):
    template_name = 'project/list.html'
    model = models.Project

    def get_queryset(self):
        return self.request.user.project_member.all()


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'project/delete.html'
    model = models.Project

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_success_url(self):
        return urls.reverse('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project Deletion'
        return context


class ProjectEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'project/edit.html'
    model = models.Project
    fields = ['name', 'description']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.admin.all():
            return obj
        else:
            raise PermissionDenied

    def get_success_url(self):
        return urls.reverse('project:detail', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project Editing'
        return context
