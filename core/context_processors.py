def is_active(request):
    return {
        'is_active': request.resolver_match.url_name
    }