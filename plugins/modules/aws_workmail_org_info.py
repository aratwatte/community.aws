#!/usr/bin/python

# Copyright: (c) 2020, Anuja Ratwatte
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: aws_workmail_org_info

short_description: This is a module that gathers information about a Workmail Organization within an AWS Account.

version_added: "1.0.0"

description: This is my longer description explaining my test info module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str

author:
    - Anuja Ratwatte (@aratwatte)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test_info:
    name: hello world
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''

from ansible.module_utils.aws.core import AnsibleAWSModule

def get_org_id_from_alias(connection, module):
    requested_alias = module.params['name']

    try:
        paginator = connection.get_paginator('list_organizations')
        response_iterator = paginator.paginate(PaginationConfig={ 'MaxItems': 123, 'PageSize': 123 })
    except Exception as e:
        module.fail_json_aws(e)
    
    for page in response_iterator:
        for org_summary in page['OrganizationSummaries']:
            if org_summary['Alias'] == requested_alias:
                return org_summary['OrganizationId']
    
    module.fail_json(msg="Workmail organization alias %s does not exist in the AWS Account." % (requested_alias))
    


def run_module():
    # define available arguments/parameters a user can pass to the module
    argument_spec = dict(
        name=dict(type='str', required=True, aliases=['alias']),
    )

    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    connection = module.client('workmail')

    org_id = get_org_id_from_alias(connection, module)

    try:
        result = connection.describe_organization(OrganizationId=org_id)
    except Exception as e:
        module.fail_json_aws(e)

    module.exit_json(changed=False, **camel_dict_to_snake_dict(result))

def main():
    run_module()


if __name__ == '__main__':
    main()