'''Shorty Views'''

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ShortURL
from .forms import ShortURLForm


def do_redirect(request, slug=None):
    path_slug = slug
    if not path_slug:
        path_slug = request.META['HTTP_HOST'].split('.', 1)[0]
    try:
        short_url = ShortURL.objects.get(path=path_slug)
    except ShortURL.DoesNotExist:
        if not slug:
            return HttpResponseRedirect(reverse('home'))
        raise Http404
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
        return HttpResponseBadRequest
    url.delete()
    return HttpResponseRedirect(reverse('home'))

