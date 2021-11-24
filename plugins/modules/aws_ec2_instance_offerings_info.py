#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ..module_utils.ec2 import describe_instance_type_offerings

def main():
    argument_spec = dict(
        availability_zone=dict(aliases=['az']),
        availability_zone_id=dict(aliases=['az_id', 'zone_id']),
        instance_type=dict()
    )
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    client = module.client('ec2')

    payload = dict()
    if module.params['availability_zone'] is not None:
        payload.update(location_type="availability-zone", location=[module.params['availability_zone']])

    instance_types = describe_instance_type_offerings(client, module, **payload)
    module.exit_json(instance_types=instance_types)
    

if __name__ == '__main__':
    main()