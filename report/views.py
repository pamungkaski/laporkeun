from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import generic

from . import models
from member import models as member_models
from task import models as task_models
from project import models as project_models


class ReportCreationView(LoginRequiredMixin, generic.CreateView):
    template_name = 'report/edit.html'
    model = models.Report
    fields = ['done', 'todo', 'problem']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        reporter = member_models.Member.object.get(
            pk=self.request.user.pk
        )
        task = task_models.Task.objects.get(pk=self.kwargs['pk_task'])
        self.object.reporter = reporter
        self.object.task = task
        self.object.save()
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            urls.reverse('task:detail', kwargs={
                'pk': task.pk,
            }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Report Creation'
        return context


class ReportUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'report/edit.html'
    model = models.Report
    fields = ['done', 'todo', 'problem']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.pk in obj.member.pk:
            return obj
        else:
            raise PermissionDenied

    def get_success_url(self):
        return urls.reverse('task:detail', kwargs={
            'pk': self.object.task.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Report Editing'
        return context


class ReportMemberListView(LoginRequiredMixin, generic.ListView):
    template_name = 'report/list.html'
    model = models.Report

    def get_queryset(self):
        return self.request.user.report_set.all()


class ReportTaskListView(LoginRequiredMixin, generic.ListView):
    template_name = 'report/list.html'
    model = models.Report

    def get_queryset(self):
        task = task_models.Task.objects.get(
            pk=self.kwargs['pk_task']
        )
        if self.request.user in task.project.member.all():
            return task.report_set.all()
        else:
            raise PermissionDenied
