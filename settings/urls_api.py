
from django.urls import include, path, re_path
from . import views, apiviews

urlpatterns = [
    # User settings
    re_path(r'^user/', include([
        # User Settings Detail
        re_path(r'^(?P<key>\w+)/',apiviews.UserSettingsDetail.as_view(), name='api-user-setting-detail'),

        # User Settings List
        re_path(r'^.*$', apiviews.UserSettingsList.as_view(), name='api-user-setting-list'),
    ])),
]