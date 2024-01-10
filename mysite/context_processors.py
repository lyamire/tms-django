from django.http import HttpRequest

def base_template_context_processor(request: HttpRequest) -> dict:
    if 'next' not in request.GET:
        return {}
    next = request.GET['next']
    if next.startswith('/polls'):
        return {'base_template': 'polls/base.html'}
    if next.startswith('/articles'):
        return {'base_template': 'articles/base.html'}
    if next.startswith('/shop'):
        return {'base_template': 'shop/base.html'}
    return {}






