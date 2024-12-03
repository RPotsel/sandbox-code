#!/usr/bin/env python3
# https://libvirt.gitlab.io/libvirt-appdev-guide-python/
# https://github.com/ansible-collections/community.general/tree/main/plugins/inventory

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
name: libvirt_qemu
extends_documentation_fragment:
    - constructed
short_description: Libvirt inventory source
description:
    - Get libvirt guests in an inventory source.
options:
    plugin:
        description: Token that ensures this is a source file for the 'libvirt' plugin.
        required: True
        type: str
    uri:
        description: Libvirt Connection URI
        required: True
        type: str
'''

EXAMPLES = r'''
plugin: libvirt_qemu
uri: 'qemu:///system'
'''

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.utils.display import Display
from ansible.module_utils._text import to_native

try:
    import libvirt
except ImportError:
    raise AnsibleError('The libvirt dynamic inventory plugin requires libvirt-python')

VIRDOMAINSTATE = ["nostate", "running", "blocked", "paused", "shutdown", "shutoff", "crashed", "pmsuspended", "last"]
display = Display()

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'libvirt_qemu'

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('libvirt_qemu.yml', 'libvirt_qemu.yaml')):
                return True
        display.debug("libvirt_qemu inventory filename must end with 'libvirt_qemu.yml' or 'libvirt_qemu.yaml'")
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self._read_config_data(path)

        uri = self.get_option('uri')

        if not uri:
            raise AnsibleError("hypervisor uri not given")

        connection = libvirt.open(uri)
        if not connection:
            raise AnsibleError("hypervisor connection failure")


        for instance in connection.listAllDomains():
            inventory_hostname = instance.name()
            inventory_uuid     = instance.UUIDString()

            self.inventory.add_host(inventory_hostname)

            try:
                domain = connection.lookupByUUIDString(inventory_uuid)
            except libvirt.libvirtError as e:
                self.inventory.set_variable(inventory_hostname, 'ERROR', str(e))

            _domain_state, _domain_maxmem, _domain_mem, _domain_cpus, _domain_cput = domain.info()
            domain_info = {"state_number": _domain_state,
                           "state": VIRDOMAINSTATE[_domain_state],
                           "maxMem_kb": _domain_maxmem,
                           "memory_kb": _domain_mem,
                           "nrVirtCpu": _domain_cpus,
                           "cpuTime_ns": _domain_cput}
            self.inventory.set_variable(
                inventory_hostname,
                'info',
                domain_info
            )

            # self.inventory.set_variable(
            #     inventory_hostname,
            #     'xml_desc',
            #     domain.XMLDesc()
            # )

            # This needs the guest powered on, 'qemu-guest-agent' installed and the org.qemu.guest_agent.0 channel configured.
            if domain.isActive():
                domain_guestInfo = ''
                try:
                    # type==0 returns all types (users, os, timezone, hostname, filesystem, disks, interfaces)
                    domain_guestInfo = domain.guestInfo(types=0)
                except libvirt.libvirtError as e:
                    domain_guestInfo = {"error": str(e)}
                finally:
                    self.inventory.set_variable(
                        inventory_hostname,
                        'guest_info',
                        domain_guestInfo
                    )

                domain_interfaceAddresses = ''
                try:
                    domain_interfaceAddresses = domain.interfaceAddresses(source=libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
                except libvirt.libvirtError as e:
                    domain_interfaceAddresses = {"error": str(e)}
                finally:
                    self.inventory.set_variable(
                        inventory_hostname,
                        'interface_addresses',
                        domain_interfaceAddresses
                    )
                    for (name, val) in domain_interfaceAddresses.items():
                        if (name.startswith('eth') or name.startswith('enp')) and val['addrs']:
                            for ipaddr in val['addrs']:
                                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                                    self.inventory.set_variable(
                                        inventory_hostname,
                                        'ansible_host',
                                        to_native(ipaddr['addr'])
                                    )
                                    break

                # Get variables for compose
                variables = self.inventory.hosts[inventory_hostname].get_vars()

                # Use constructed if applicable
                strict = self.get_option('strict')

                # Set composed variables
                self._set_composite_vars(
                    self.get_option('compose'),
                    variables,
                    inventory_hostname,
                    strict=strict,
                )

                # Add host to composed groups
                self._add_host_to_composed_groups(
                    self.get_option('groups'),
                    variables,
                    inventory_hostname,
                    strict=strict,
                )

                # Add host to keyed groups
                self._add_host_to_keyed_groups(
                    self.get_option('keyed_groups'),
                    variables,
                    inventory_hostname,
                    strict=strict,
                )

        connection.close()
