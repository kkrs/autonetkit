#!/usr/bin/python
# -*- coding: utf-8 -*-
import autonetkit.ank as ank_utils
import autonetkit.config
import autonetkit.log as log

SETTINGS = autonetkit.config.settings


# TODO: refactor to go in chronological workflow order




#@call_log
def build_ip(anm):
    g_ip = anm.add_overlay('ip')
    g_l2 = anm['layer2']
    g_phy = anm['phy']
    # Retain arbitrary ASN allocation for IP addressing
    g_ip.copy_nodes_from(g_l2)
    ank_utils.copy_node_attr_from(g_l2, g_ip, "broadcast_domain")
    ank_utils.copy_node_attr_from(g_l2, g_ip, "asn")
    g_ip.copy_edges_from(g_l2.edges())

    #TODO:
    for bc in g_ip.nodes("broadcast_domain"):
        bc.set('allocate', True)

    for bc in g_ip.nodes("broadcast_domain"):
        if bc.get('asn') is None:
            # arbitrary choice
            asn = ank_utils.neigh_most_frequent(g_l2, bc, 'asn', g_phy)
            bc.set('asn', asn)

        for neigh in bc.neighbors():
            if (neigh.get('device_type') in ("external_connector", "switch")
                and neigh.get('device_subtype') in ("FLAT", "SNAT")):
                bc.set('allocate', False)

                for neigh_int in bc.neighbor_interfaces():
                    neigh_int.set('allocate', False)

        # Encapsulated if any neighbor interface has
        for edge in bc.edges():
            if edge.dst_int['phy'].get('l2_encapsulated'):
                log.debug("Removing IP allocation for broadcast_domain %s "
                         "as neighbor %s is L2 encapsulated", bc, edge.dst)

                #g_ip.remove_node(bc)
                bc.set('allocate', False)

                # and mark on connected interfaces
                for neigh_int in bc.neighbor_interfaces():
                    neigh_int.set('allocate', False)

                break

    # copy over skipped loopbacks
    #TODO: check if loopbck copy attr
    for node in g_ip.l3devices():
        for interface in node.loopback_interfaces():
            if interface['phy'].get('allocate') is not None:
                interface['ip'].set('allocate', interface['phy'].get('allocate'))


def build_ipv4(anm, infrastructure=True):
    import autonetkit.design.ip_addressing.ipv4
    autonetkit.design.ip_addressing.ipv4.build_ipv4(
        anm, infrastructure=infrastructure)

def build_ipv6(anm):
    #TODO: check why ipv6 doesn't take infrastructure
    import autonetkit.design.ip_addressing.ipv6
    autonetkit.design.ip_addressing.ipv6.build_ipv6(anm)
#@call_log
