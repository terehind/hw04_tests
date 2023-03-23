from django.core.paginator import Paginator


def paginator(request, objects, count_on_page=10):
    page_number = request.GET.get('page')
    return Paginator(objects, count_on_page).get_page(page_number)
