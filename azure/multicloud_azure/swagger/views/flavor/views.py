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

import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from multicloud_azure.pub.msapi import extsys
from multicloud_azure.pub.vim.vimapi.compute import OperateFlavors
from multicloud_azure.swagger import compute_utils
from multicloud_azure.pub.exceptions import VimDriverAzureException


class FlavorsView(APIView):

    def post(self, request, vimid):
        try:
            create_req = json.loads(request.body)
        except Exception:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverAzureException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'subscription_id': vim_info['cloud_extra_info'],
                'username': vim_info['username'],
                'password': vim_info['password'],
                'tenant_id': vim_info['default_tenant'],
                'region_id': vim_info['cloud_region']}
        rsp = {'vimId': vim_info['cloud_extra_info'],
               'vimName': vim_info['name']}
        flavor_name = create_req.get('name', None)
        flavor_id = create_req.get('id', None)
        flavors_op = OperateFlavors.OperateFlavors()
        try:
            target = flavor_id or flavor_name
            flavor = flavors_op.find_flavor(data, target)
            if flavor:
                flavor, extra_specs = flavors_op.get_flavor(
                    data, flavor.id)
                rsp['returnCode'] = 0
            else:
                rsp['returnCode'] = 1
                flavor, extra_specs = flavors_op.create_flavor(
                    data, create_req)
            flavor_dict = compute_utils.flavor_formatter(flavor, extra_specs)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        rsp.update(flavor_dict)
        return Response(data=rsp, status=status.HTTP_200_OK)

    def get(self, request, vimid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverAzureException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'subscription_id': vim_info['cloud_extra_info'],
                'username': vim_info['username'],
                'password': vim_info['password'],
                'tenant_id': vim_info['default_tenant'],
                'region_id': vim_info['cloud_region_id']}
        query = dict(request.query_params)
        flavors_op = OperateFlavors.OperateFlavors()
        try:
            flavors_result = flavors_op.list_flavors(data, **query)
            flavors_dict = [compute_utils.flavor_formatter(flavor, extra)
                            for flavor, extra in flavors_result]
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rsp = {'vimId': vim_info['cloud_extra_info'],
               'vimName': vim_info['name'],
               'flavors': flavors_dict}

        return Response(data=rsp, status=status.HTTP_200_OK)
