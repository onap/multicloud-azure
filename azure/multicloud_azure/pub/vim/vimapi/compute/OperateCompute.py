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

import logging

from multicloud_azure.pub.vim.vimapi.baseclient import baseclient


logger = logging.getLogger(__name__)


class OperateCompute(baseclient):

    def __init__(self, **kwargs):
        super(OperateCompute, self).__init__(**kwargs)

    def request(self, op, data, **kwargs):
        compute = self.get_compute_client(data)
        func = getattr(compute, op)
        return func
