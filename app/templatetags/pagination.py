from django import template
from django.urls import reverse

register = template.Library()

@register.inclusion_tag("app/partials/pagination.html")
def pagination(urlname, **kwargs):
    """
    This template tag for pagination in the all pages.
    page key in view_kwargs should removed because some time
    don't generate url like this --> /example/page/1/page/1/.
    """
    view_kwargs = kwargs.get("view_kwargs", {}).copy()
    view_kwargs.pop("page", {})
    view_kwargs.pop("slug", {})

    get_url = reverse(urlname, kwargs=kwargs.get("view_kwargs", {}))
    context = kwargs.get("context", {})

    return {
        "get_url": get_url,
        **context
    }
    