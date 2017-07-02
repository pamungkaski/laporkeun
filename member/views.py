from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from member import forms, models


def member_creation_view(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(urls.reverse('home'))

    if request.method == 'POST':
        form = forms.MemberEditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(urls.reverse('member:login'))
    else:
        form = forms.MemberEditForm()

    template_name = 'member/creation.html'
    return render(request, template_name, {
        'form': form,
        'title': 'Member Creation'
    })


class MemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'member/update.html'
    model = models.Member
    fields = ['username', 'email', 'name', ]

    def get_object(self, queryset=None):
        return models.Member.object.get(
            pk=self.request.user.pk
        )

    def get_success_url(self):
        return urls.reverse('member:update')
