from django.shortcuts import render


def index(request):
    if request.user.is_authenticated():
        return render(
            request,
            template_name='home/index_authenticated.html',
            context={
                'request': request,
                'title': 'home'
            }
        )
    else:
        return render(
            request,
            template_name='home/index_anonymous.html'
        )