'''Shorty Views'''

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.six.moves.urllib.parse import urlparse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ShortURL
from .forms import ShortURLForm
from .app_settings import EXTERNAL_FLAG, CANONICAL_DOMAIN


def check_initial_redirect(request, path_slug):

    if not CANONICAL_DOMAIN:
        return None

    canonical_scheme, canonical_netloc = urlparse(CANONICAL_DOMAIN)[:2]
    current_scheme, current_netloc = urlparse(request.build_absolute_uri())[:2]
    if not (current_scheme == canonical_scheme and current_netloc == canonical_netloc):
        return '{}/{}'.format(CANONICAL_DOMAIN, path_slug)


def do_redirect(request, slug=None):

    path_slug = slug
    if not path_slug:
        try:
            path_slug = request.META['HTTP_HOST'].split('.', 1)[0]
        except KeyError:
            return HttpResponseBadRequest()

    initial_redirect = check_initial_redirect(request, path_slug)

    if initial_redirect:
        return HttpResponseRedirect(initial_redirect)

    try:
        short_url = ShortURL.objects.get(path=path_slug)
    except ShortURL.DoesNotExist:
        if not slug:
            return HttpResponseRedirect(reverse('home'))
        raise Http404

    if EXTERNAL_FLAG and not short_url.external and not request.user.is_authenticated():
        return login_required(lambda _: None)(request)

    if 'preview' in request.GET or 'p' in request.GET:
        return render(request, 'shorty/preview.html', {
            'url': short_url,
        })

    return HttpResponseRedirect(short_url.redirect)


@login_required
def home(request):

    path = None

    if 'path' in request.session:
        try:
            path = request.build_absolute_uri(reverse('redirect', kwargs={'slug': request.session['path']}))
        except NoReverseMatch:
            pass
        del request.session['path']

    if request.method == 'POST':
        form = ShortURLForm(request, request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.save()
            request.session['path'] = model.path
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ShortURLForm(request)

    paginator = Paginator(request.user.short_urls.all().order_by('-created'), 10)

    page = request.GET.get('page')
    try:
        short_urls = paginator.page(page)
    except PageNotAnInteger:
        short_urls = paginator.page(1)
    except EmptyPage:
        short_urls = paginator.page(paginator.num_pages)

    return render(request, 'shorty/home.html', {
        'EXTERNAL_FLAG': EXTERNAL_FLAG,
        'path': path,
        'form': form,
        'short_urls': short_urls,
        'redirect_base': request.build_absolute_uri(reverse('redirect_base')),
    })


@login_required
@require_POST
def delete(request):
    try:
        url = ShortURL.objects.get(pk=request.POST['id_short_url'], user=request.user)
    except (ShortURL.DoesNotExist, KeyError):
        return HttpResponseBadRequest()
    url.delete()
    return HttpResponseRedirect(reverse('home'))

