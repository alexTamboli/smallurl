from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from ipware import get_client_ip
from cryptography.fernet import InvalidToken

from .forms import LinkForm, DecryptForm
from .models import ShortenedLink, AccessLog
from .shortener import Shortener
from .utils import extract_video_id, encrypt_link, decrypt_link


def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            original_link = form.cleaned_data['youtube_link']
            encryption_key = form.cleaned_data['encryption_key']
            
            try:
                # Shortening logic
                shortener = Shortener()
                short_url_token = shortener.issue_token()
                
                # Check for collisions and regenerate token if needed
                while ShortenedLink.objects.filter(short_url_hash=short_url_token).exists():
                    short_url_token = shortener.issue_token()
                
                base_url = request.build_absolute_uri('/')[:-1]
                short_url = base_url + "/" + short_url_token
                
                if encryption_key:
                    encrypted_link = encrypt_link(short_url, encryption_key)
                else:
                    encrypted_link = None

                shortened_link = ShortenedLink.objects.create(
                    original_link=original_link,
                    encrypted_url=encrypted_link,
                    short_url=short_url,
                    short_url_hash=short_url_token
                )

                return redirect(f'{short_url_token}/')
            except InvalidToken:
                error_message = "Invalid encryption key format. Please provide a valid key."
                messages.error(request, error_message)
            except ValueError as e:
                error_message = f"Encryption failed: {str(e)}"
                messages.error(request, error_message)
    else:
        form = LinkForm()
    
    return render(request, 'smallurl/index.html', {'form': form})


def view_smallurl(request, hash):
    try:
        shortened_link = ShortenedLink.objects.get(short_url_hash=hash)
    except ShortenedLink.DoesNotExist:
        raise Http404("ShortenedLink does not exist")

    client_ip, is_routable = get_client_ip(request)

    # Log access information
    AccessLog.objects.create(link=shortened_link, ip_address=client_ip)

    short_url = shortened_link.short_url
    encrypted_url = shortened_link.encrypted_url
    youtube_video_id = extract_video_id(shortened_link.original_link)
    if encrypted_url is not None:
        encrypted_url = encrypted_url[2:-1]
        
    context = {'youtube_video_id': youtube_video_id, 'short_url': short_url, 'encrypted_url': encrypted_url}
    return render(request, 'smallurl/target.html', context=context)


def view_links(request):
    # base_url = request.build_absolute_uri('/')[:-1]
    links = ShortenedLink.objects.all().order_by('-created_at')[:5]
    youtube_video_ids = [extract_video_id(link.original_link) for link in links]
    links_with_video_ids = zip(links, youtube_video_ids)

    context = {'links_with_video_ids': links_with_video_ids}
    return render(request, 'smallurl/view_links.html', context=context)


def access_logs(request):
    # base_url = request.build_absolute_uri('/')[:-1]
    logs = AccessLog.objects.all().order_by('-accessed_at')
    return render(request, 'smallurl/access_logs.html', {'logs': logs})


def decrypt_view(request):
    if request.method == 'POST':
        form = DecryptForm(request.POST)
        if form.is_valid():
            decryption_key = form.cleaned_data['decryption_key']
            encrypted_link = form.cleaned_data['encrypted_url']

            try:
                decrypted_link = decrypt_link(encrypted_link, decryption_key)

                return redirect(decrypted_link)
            except InvalidToken:
                error_message = "Invalid decryption key or encrypted link."
                messages.error(request, error_message)
                return render(request, 'smallurl/decrypt.html', {'form': form})
            except ValueError as e:
                error_message = f"Encryption failed: {str(e)}"
                messages.error(request, error_message)
    else:
        form = DecryptForm()

    return render(request, 'smallurl/decrypt.html', {'form': form})
