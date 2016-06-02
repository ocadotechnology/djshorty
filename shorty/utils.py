'''Shorty utils'''

def is_external_request(request):
    if 'HTTP_X_LOCAL' in request.META and request.META['HTTP_X_LOCAL'].lower() == 'yes':
        return False
    return True
