#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ..module_utils.ec2 import describe_instance_type_offerings

def main():
    argument_spec = {
        'availability_zone': dict(type='list', aliases=['az']),
        'availability_zone_id': dict(type='list', aliases=['az_id', 'zone_id']),
        'instance_type': dict(type='list', aliases=['type'])
    }
    mutually_exclusive = ['availability_zone', 'availability_zone_id']
    module = AnsibleAWSModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, 
                              supports_check_mode=True)
    client = module.client('ec2')

    payload = {
        'location_type': 'region', 
        'location': [module.params['region']]
    }
    
    if module.params['availability_zone'] is not None:
        payload.update({
            'location_type': 'availability-zone', 
            'location': module.params['availability_zone'] if isinstance(module.params['availability_zone'], list)
                else [module.params['availability_zone']]
        })
    elif module.params['availability_zone_id'] is not None:
        payload.update({
            'location_type': 'availability-zone-id',
            'location': module.params['availability_zone_id'] if isinstance(module.params['availability_zone_id'], list)
                else [module.params['availability_zone_id']]  
        })
    if module.params['instance_type'] is not None:
        payload.update({
            'instance-type': module.params['instance_type'] if isinstance(module.params['instance_type'], list)
                else [module.params['instance_type']] 
        })

    instance_types = describe_instance_type_offerings(client, module, **payload)
    module.exit_json(instance_types=instance_types)
    

if __name__ == '__main__':
    main()