from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, ParseResult


def get_next_page(request, pagination, total):
    page = pagination['page']
    size = pagination['size']

    next_page = None
    if page * size < total:
        # Decompose the request path
        parsed_url = urlparse(request.full_path)
        parsed_query_params = parse_qs(parsed_url.query)

        # Update the page
        parsed_query_params['page'] = page + 1

        # Reconstruct the full url
        new_query = urlencode(parsed_query_params, doseq=True)
        new_url = ParseResult(scheme=parsed_url.scheme,
                              netloc=parsed_url.netloc,
                              path=parsed_url.path,
                              params=parsed_url.params,
                              query=new_query,
                              fragment=parsed_url.fragment)
        next_page = urlunparse(new_url)

    return next_page


def get_previous_page(request, pagination):
    page = pagination['page']

    prev_page = None
    if page > 1:
        # Decompose the request path
        parsed_url = urlparse(request.full_path)
        parsed_query_params = parse_qs(parsed_url.query)

        # Update the page
        parsed_query_params['page'] = page - 1

        # Reconstruct the full url
        new_query = urlencode(parsed_query_params, doseq=True)
        new_url = ParseResult(scheme=parsed_url.scheme,
                              netloc=parsed_url.netloc,
                              path=parsed_url.path,
                              params=parsed_url.params,
                              query=new_query,
                              fragment=parsed_url.fragment)
        prev_page = urlunparse(new_url)

    return prev_page
