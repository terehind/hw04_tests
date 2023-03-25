from django.shortcuts import render


def page_not_found(request, exception):
    template = 'core/404.html'
    context = {'path': request.path}
    return render(request, template, context, status=404)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')
