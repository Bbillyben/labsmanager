"""This module provides template tags for handling plugins."""

from django import template
from django.conf import settings as djangosettings
from django.templatetags.static import static
from django.urls import reverse

from settings.accessor import get_global_setting
from plugin.registry import registry
from django.conf import settings
register = template.Library()

@register.simple_tag()
def plugin_enabled(*args, **kwargs):
    """Is plugin navigation enabled?"""
    if djangosettings.PLUGIN_TESTING:
        return True
    return settings.PLUGINS_ENABLED  # pragma: no cover

@register.simple_tag()
def plugin_list(*args, **kwargs):
    """List of all installed plugins."""
    return registry.plugins

@register.simple_tag()
def plugin_list_mixin(mixin, active=True, *args, **kwargs):
    """List of all installed plugins."""
    return registry.with_mixin(mixin, active=active)

@register.simple_tag()
def inactive_plugin_list(*args, **kwargs):
    """List of all inactive plugins."""
    return registry.plugins_inactive


@register.simple_tag()
def plugin_settings(plugin, *args, **kwargs):
    """List of all settings for the plugin."""
    return registry.mixins_settings.get(plugin)


@register.simple_tag(takes_context=True)
def plugin_settings_content(context, plugin, *args, **kwargs):
    """Get the settings content for the plugin."""
    plg = registry.get_plugin(plugin)
    if hasattr(plg, 'get_settings_content'):
        return plg.get_settings_content(context.request)
    return None

@register.simple_tag()
def plugin_filter_choice_clug(pluginSlug, filter, *args, **kwargs):
    """return a slug for a plugin filter ."""
    from django.utils.text import slugify
    return pluginSlug + "-"+slugify(filter)

@register.simple_tag()
def mixin_enabled(plugin, key, *args, **kwargs):
    """Is the mixin registered and configured in the plugin?"""
    return plugin.mixin_enabled(key)


@register.simple_tag()
def mixin_available(mixin, *args, **kwargs):
    """Returns True if there is at least one active plugin which supports the provided mixin."""
    return len(registry.with_mixin(mixin)) > 0


@register.simple_tag()
def navigation_enabled(*args, **kwargs):
    """Is plugin navigation enabled?"""
    if djangosettings.PLUGIN_TESTING:
        return True
    return get_global_setting('ENABLE_PLUGINS_NAVIGATION')  # pragma: no cover


@register.simple_tag()
def safe_url(view_name, *args, **kwargs):
    """Safe lookup fnc for URLs.

    Returns None if not found
    """
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except Exception:
        return None


@register.simple_tag()
def plugin_errors(*args, **kwargs):
    """All plugin errors in the current session."""
    return registry.errors



@register.simple_tag(takes_context=True)
def plugin_static(context, file: str, **kwargs):
    """Return the URL for a static file within a plugin.

    Arguments:
        file: The path to the file within the plugin static directory

    Keyword Arguments:
        plugin: The plugin slug (optional, will be inferred from the context if not provided)

    """
    plugin = context.get('plugin', None)

    plugin = plugin.slug if plugin else kwargs.get('plugin', None)

    if not plugin:
        return file

    return static(f'plugins/{plugin}/{file}')


@register.simple_tag()
def plugin_scheduled_tasks(plugin, *args, **kwargs):
    from django_q.models import Schedule
    tasks_names = plugin.get_task_names()
    result={"task_names":tasks_names,}
    for task_name in tasks_names:
        scheduled_plugin_tasks = Schedule.objects.filter(
                name=task_name
            )
        result[task_name]=scheduled_plugin_tasks #.values()
    return result
    
    
    