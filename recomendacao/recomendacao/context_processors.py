from django.conf import settings


def full_absolute_urls(request):
    context = {
        'full_url_with_query_string': request.build_absolute_uri(),
        'full_url': request.build_absolute_uri('?'),
        'absolute_root': request.build_absolute_uri('/')[:-1].strip("/"),
        'absolute_root_url': request.build_absolute_uri('/').strip("/"),
    }
    return context

def settings(request):
    context = {
        'FILES_URL': settings.FILES_URL,
    }
    return context
