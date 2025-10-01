#!/usr/bin/env python3

#!/usr/bin/python

# Copyright: (c) 2025, Rune Juhl <runejuhl@petardo.dk>
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import subprocess
import yaml

from functools import reduce
import operator
import requests
from os import environ

## Debugging
#
# $ python3
#   .ansible/collections/ansible_collections/petardo/k8s/plugins/modules/kubectl.py
#   <<< '{"ANSIBLE_MODULE_ARGS": {"namespace":"kube-system", "kind":
#   "configmap", "manifest": "", "name": "coredns"}}'

__metaclass__ = type

DOCUMENTATION = r"""
---
module: petardo.vmware.vra_workflows

short_description: Do something with VMware vRA workflows

version_added: "2.0.0"

description: FIXME:

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Rune Juhl (@runejuhl)
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
"""

RETURN = r"""
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
"""

from ansible.module_utils.basic import AnsibleModule

DEBUG = True
DEBUG_FILE = False  # "/tmp/stuff.log"


def _debug(*args):
    """Print `args` to stdout or file."""
    if not DEBUG:
        return

    if DEBUG_FILE:
        with open(DEBUG_FILE, "a") as f:
            f.writelines(args + ("\n",))
    else:
        print(*args)


def run_module():
    module_args = dict(
        id=dict(type="str", required=False),
    )

    result = {
        "changed": False,
        "args": module_args,
    }

    if DEBUG:
        result["debug"] = {
            "netrc": environ["NETRC"],
            # "netrc_contents": open(environ["NETRC"]).read(),
        }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    id = module.params["id"]
    result["id"] = id

    req = requests.request(
        method="GET",
        url=f"https://adc-vro.adc.lan/vco/api/workflows/{id}/content",
        verify=False,
    )

    result["request"] = {"url": req.url, "method": req.request.method}
    result["response"] = {"status": req.status_code}

    if not req.ok:
        result["response"]["text"] = req.text
        module.fail_json(
            msg=f"""Request failed with code {req.status_code}""", **result
        )

    result["workflow"] = req.json()

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
