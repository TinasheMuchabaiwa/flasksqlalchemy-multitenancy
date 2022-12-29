from flask import url_for


def _pagination_nav_links(pagination, api_route):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for(
        api_route, page=this_page, per_page=per_page, _external=True
    )
    nav_links["first"] = url_for(api_route, page=1, per_page=per_page, _external=True)
    if pagination.has_prev:
        nav_links["prev"] = url_for(
            api_route, page=this_page - 1, per_page=per_page, _external=True
        )
    if pagination.has_next:
        nav_links["next"] = url_for(
            api_route, page=this_page + 1, per_page=per_page, _external=True
        )
    nav_links["last"] = url_for(
        api_route, page=last_page, per_page=per_page, _external=True
    )
    return nav_links


def _pagination_nav_header_links(pagination, api_route):
    url_dict = _pagination_nav_links(pagination, api_route)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")
