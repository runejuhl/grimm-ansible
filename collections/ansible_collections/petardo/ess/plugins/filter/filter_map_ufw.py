#!/usr/bin/env python3

from typing import Dict, List

from ansible.errors import AnsibleFilterError
from ansible.utils.display import Display

display = Display()


def filter_map_ufw(data: Dict) -> Dict | None:
    result = {}  # {"state": "present"}
    for k, v in data.items():
        match k:
            case "Protocol":
                k = "proto"
                if v == "*":
                    v = "any"
                else:
                    v = v.lower()
            case "Source":
                k = "src"
            case "Source port":
                k = "from_port"
            case "Destination":
                k = "dest"
            case "Destination port":
                k = "to_port"
            case "Ingress interface":
                k = "interface_in"
            case "Egress interface":
                k = "interface_out"
            case "Log":
                k = "log"
            case "Comment":
                k = "comment"
            case "Action":
                k = "rule"
                match v.lower():
                    case "accept":
                        v = "allow"
                    case "reject":
                        v = "reject"
                    case "drop":
                        v = "deny"
            case _:
                raise AnsibleFilterError(f"unable to map '{k}' to ufw")

        result[k] = v

        if result.get("proto") == "icmp":
            display.warning("The ufw module doesn't allow configuring ICMP rules")
            return None

    return result


def filter_map_ufws(datas: List[Dict]) -> List[Dict | None]:
    return [filter_map_ufw(data) for data in datas]


class FilterModule(object):
    def filters(self):
        return {
            "map_ufw": filter_map_ufw,
            "map_ufws": filter_map_ufws,
        }
