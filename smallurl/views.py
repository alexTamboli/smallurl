from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from .forms import LinkForm
from .models import ShortenedLink, AccessLog
from .shortener import Shortener
from .utils import extract_video_id


def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            original_link = form.cleaned_data['youtube_link']
            encryption_key = form.cleaned_data['encryption_key']
            
            # Perform encryption here if encryption_key is provided
            
            shortener = Shortener()
            short_url_token = shortener.issue_token()
            # short_url_token = shortener.shorten_url(original_link)
            
            # Check for collisions and regenerate token if needed
            while ShortenedLink.objects.filter(short_url_hash=short_url_token).exists():
                short_url_token = shortener.issue_token()

            shortened_link = ShortenedLink.objects.create(
                                            original_link=original_link, 
                                            short_url_hash=short_url_token)
            
            return redirect(f'{short_url_token}/')
    else:
        form = LinkForm()
    
    return render(request, 'smallurl/index.html', {'form': form})


def view_smallurl(request, hash):
    try:
        shortened_link = ShortenedLink.objects.get(short_url_hash=hash)
    except ShortenedLink.DoesNotExist:
        raise Http404("ShortenedLink does not exist")

    ip_address = request.META.get('REMOTE_ADDR')

    # Log access information
    AccessLog.objects.create(link=shortened_link, ip_address=ip_address)

    short_url = request.build_absolute_uri(reverse('smallurl_view', args=[hash]))
    youtube_video_id = extract_video_id(shortened_link.original_link)
    
    context = {'youtube_video_id': youtube_video_id, 'short_url': short_url}
    return render(request, 'smallurl/target.html', context=context)


def view_links(request):
    links = ShortenedLink.objects.all().order_by('-created_at')
    return render(request, 'smallurl/view_links.html', {'links': links})


def access_logs(request):
    base_url = request.build_absolute_uri('/')[:-1]
    logs = AccessLog.objects.all().order_by('-accessed_at')
    return render(request, 'smallurl/access_logs.html', {'base_url': base_url, 'logs': logs})
