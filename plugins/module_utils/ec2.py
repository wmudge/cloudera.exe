# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

"""
Common Amazon EC2 functions shared between modules
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass

from ansible.module_utils.common.text.converters import container_to_text
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict

from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import ansible_dict_to_boto3_tag_list
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import boto3_tag_list_to_ansible_dict

        
def describe_instance_type_offerings(client, module, location_type='region', **kwargs):
    filters = ansible_dict_to_boto3_filter_list(kwargs)
    try:
        results = AWSRetry.jittered_backoff(retries=10)(
            _describe_instance_type_offerings
        )(client, LocationType=location_type, Filters=filters)
        return results.get('InstanceTypeOfferings')
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg="Failed to describe instance types")
    
    
@AWSRetry.jittered_backoff()
def _describe_instance_type_offerings(client, **params):
    paginator = client.get_paginator('describe_instance_type_offerings')
    return paginator.paginate(**params).build_full_result()
    #return client.describe_instance_type_offerings(LocationType=location_type, Filters=filters)


def ansible_dict_to_boto3_filter_list(filter_dict, filter_name_key_name='Name', filter_value_key_name='Values'):
    """ Convert a flat dict of key:value pairs representing AWS resource filters to a boto3 list of dicts
    Args:
        filter_dict (dict): Dict representing AWS filter.
        filter_name_key_name (str): Value to use as the key for all filter keys (useful because boto3 doesn't always use "Name")
        filter_value_key_name (str): Value to use as the key for all filter values (useful because boto3 doesn't always use "Values")
    Basic Usage:
        >>> filter_dict = {'MyFilterKey': 'MyFilterValue'}
        >>> ansible_dict_to_boto3_filter_list(filter_dict)
        {
            'MyFilterKey': 'MyFilterValue'
        }
    Returns:
        List: List of dicts containing tag keys and values
        [
            {
                'Name': 'MyFilterKey',
                'Values': ['MyFilterValue']
            }
        ]
    """

    if not filter_dict:
        return []

    filters_list = []
    for k, v in filter_dict.items():
        filters_list.append({filter_name_key_name: k, filter_value_key_name: container_to_text(v)})

    return filters_list