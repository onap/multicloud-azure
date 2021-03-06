# Copyright (c) 2018 Amdocs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from multicloud_azure.swagger.views.swagger_json import SwaggerJsonView

# Registry
from multicloud_azure.swagger.views.registry.views import Registry
from multicloud_azure.swagger.views.registry.views import UnRegistry
from multicloud_azure.swagger.views.registry.views import APIv1Registry
from multicloud_azure.swagger.views.registry.views import APIv1UnRegistry

from multicloud_azure.swagger.views.infra_workload.views import InfraWorkload
from multicloud_azure.swagger.views.infra_workload.views import GetStackView

urlpatterns = [
    # swagger
    url(r'^api/multicloud-azure/v0/swagger.json$', SwaggerJsonView.as_view()),

    # Registry
    url(r'^api/multicloud-azure/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/registry$',
        Registry.as_view()),

    url(r'^api/multicloud-azure/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)$',
        UnRegistry.as_view()),

    url(r'^api/multicloud-azure/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)'
        r'/(?P<cloud_region_id>[0-9a-zA-Z_-]+)/registry$',
        APIv1Registry.as_view()),

    url(r'^api/multicloud-azure/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)'
        r'/(?P<cloud_region_id>[0-9a-zA-Z_-]+)$',
        APIv1UnRegistry.as_view()),

    url(r'^api/multicloud-azure/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)'
        r'/(?P<cloud_region_id>[0-9a-zA-Z_-]+)/infra_workload$',
        InfraWorkload.as_view()),

    url(r'^api/multicloud-azure/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region_id>[0-9a-zA-Z_-]+)/infra_workload/'
        r'(?P<workload_id>[0-9a-zA-Z\-\_]+)$',
        GetStackView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
