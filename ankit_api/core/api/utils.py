from importlib import import_module

from django.apps import apps


def get_api_urls():
    all_patterns = []
    for app_config in apps.get_app_configs():
        try:
            qualified_name = app_config.module.__name__ + ".api.urls"
            urls_module = import_module(qualified_name)
            all_patterns += urls_module.urlpatterns
        except ImportError:
            pass
    return all_patterns
