#!/bin/sh
# Copyright (c) 2018 Amdocs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

sed -i "s/MSB_SERVICE_IP =.*/MSB_SERVICE_IP = \"${MSB_ADDR}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/MSB_SERVICE_PORT =.*/MSB_SERVICE_PORT = \"${MSB_PORT}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/AAI_ADDR =.*/AAI_ADDR = \"${AAI_ADDR}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/AAI_PORT =.*/AAI_PORT = \"${AAI_PORT}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/AAI_SCHEMA_VERSION =.*/AAI_SCHEMA_VERSION = \"${AAI_SCHEMA_VERSION}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/AAI_USERNAME =.*/AAI_USERNAME = \"${AAI_USERNAME}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/AAI_PASSWORD =.*/AAI_PASSWORD = \"${AAI_PASSWORD}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/MR_ADDR =.*/MR_ADDR = \"${MR_ADDR}\"/g" multicloud_azure/pub/config/config.py
sed -i "s/MR_PORT =.*/MR_PORT = \"${MR_PORT}\"/g" multicloud_azure/pub/config/config.py


logDir="/var/log/onap/multicloud/azure"

if [ "$WEB_FRAMEWORK" == "pecan" ]
then
    python multivimbroker/scripts/api.py
else
    # nohup python manage.py runserver 0.0.0.0:9008 2>&1 &
    nohup aria-rest 2>&1 &
    nohup uwsgi --http :9008 --module multicloud_azure.wsgi --master --processes 4 &
    nohup python -m multicloud_azure.event_listener.server 2>&1 &

    while [ ! -f  $logDir/azure.log ]; do
        sleep 1
    done
tail -F $logDir/azure.log
fi
