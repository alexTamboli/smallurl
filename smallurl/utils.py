from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url):
    """
    Extracts the YouTube video ID from a YouTube URL.
    """
    url_data = urlparse(youtube_url)
    query_params = parse_qs(url_data.query)

    if 'v' in query_params:
        return query_params['v'][0]
    elif 'youtu.be' in url_data.netloc:
        return url_data.path[1:]  # Remove leading '/'
    else:
        return None
    

def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    return ip_addr
