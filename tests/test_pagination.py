import pytest
from locations.pagination import get_next_page, get_previous_page


class MReq:
    def __init__(self, path):
        self.full_path = f'http://test/{path}'


@pytest.mark.parametrize(
    ['req', 'pagination', 'total', 'expected'],
    [
        (MReq('path?size=5'), {'size': 5, 'page': 1}, 5, None),
        (MReq('path?size=5&page=2'), {'size': 5, 'page': 2}, 6, None),
        (MReq('path?size=5&page=1&something=1'), {'size': 5, 'page': 1}, 5,
         None),
        (MReq('path?size=5'), {'size': 5, 'page': 1}, 6, 'size=5&page=2'),
        (MReq('path?size=5&page=1&something=1'), {'size': 5, 'page': 1}, 6,
         'size=5&page=2&something=1'),
    ]
)
def test_get_next_page(req, pagination, total, expected):
    next_page = get_next_page(req, pagination, total)
    print(next_page)
    if expected:
        assert expected in next_page
    else:
        assert next_page is None


@pytest.mark.parametrize(
    ['req', 'pagination', 'expected'],
    [
        (MReq('path?size=5'), {'size': 5, 'page': 1}, None),
        (MReq('path?size=5&page=2'), {'size': 5, 'page': 2}, 'size=5&page=1'),
        (MReq('path?size=5&page=1&something=1'), {'size': 5, 'page': 1}, None),
        (MReq('path?size=5&page=2&something=1'), {'size': 5, 'page': 2},
         'size=5&page=1&something=1'),
    ]
)
def test_get_prev_page(req, pagination, expected):
    prev_page = get_previous_page(req, pagination)
    if expected:
        assert expected in prev_page
    else:
        assert prev_page is None
