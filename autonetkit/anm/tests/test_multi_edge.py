import autonetkit
import autonetkit.log as log
import autonetkit.ank as ank_utils

log.info("Testing ANM")

def test():

    anm = autonetkit.NetworkModel()
    g_phy = anm['phy']
    g_phy.create_nodes_from(["r1", "r2", "r3", "r4", "r5"])
    for node in g_phy:
        node.set('device_type', "router")

    g_phy.node("r1").set('x', 100)
    g_phy.node("r1").set('y', 100)
    g_phy.node("r2").set('x', 250)
    g_phy.node("r2").set('y', 250)
    g_phy.node("r3").set('x', 100)
    g_phy.node("r3").set('y', 300)
    g_phy.node("r4").set('x', 600)
    g_phy.node("r4").set('y', 600)
    g_phy.node("r5").set('x', 600)
    g_phy.node("r5").set('y', 300)

    r1 = g_phy.node('r1')
    r2 = g_phy.node('r2')
    r3 = g_phy.node('r3')
    iface_r1 = r1.add_interface(description='test')
    iface2_r1 = r1.add_interface(description='test2')
    iface_r2 = r2.add_interface()
    iface_r3 = r3.add_interface()

    g_phy.create_edge(iface_r1, iface_r2)
    g_phy.create_edge(iface2_r1, iface_r3)
    #g_phy.add_edges_from(([("r2", "r3")]))
    #g_phy.add_edges_from(([("r2", "r4")]))
    #g_phy.add_edges_from(([("r4", "r3")]))
    #g_phy.add_edges_from(([("r4", "r5")]))
    g_simple = anm.add_overlay("simple")
    g_simple.copy_nodes_from(g_phy)
    r1 = g_simple.node('r1')
    r2 = g_simple.node('r2')
    g_simple.create_edge(r1.interface(iface_r1), r2.interface(iface_r2))
    r4 = g_simple.node('r4')
    r3 = g_simple.node('r3')
    g_simple.create_edge(r4.add_interface(), r3.interface(iface_r3))


    g_me = anm.add_overlay("multi", multi_edge = True)
    graph = g_me._graph

    g_me.copy_nodes_from(g_phy)
    r1 = g_me.node('r1')
    r2 = g_me.node('r2')
    r3 = g_me.node('r3')
    iface_r1 = r1.add_interface(description='multi')
    iface_r2 = r2.add_interface(description='multi')
    iface_r3 = r3.add_interface(description='multi')
    # add two edges
    g_me.create_edge(iface_r1, iface_r2)
    g_me.create_edge(iface_r1, iface_r2)
    g_me.create_edge(iface_r1, iface_r2)
    g_me.create_edge(iface_r1, iface_r2)
    g_me.create_edge(iface_r1, iface_r2)
    g_me.create_edge(iface_r1, iface_r3)
    g_me.create_edge(iface_r2, iface_r3)
    g_me.create_edge(iface_r2, iface_r3)

    for index, edge in enumerate(g_me.edges()):
        #print index, edge
        edge.set('index', "i_%s" % index)

    for edge in r1.edges():
        #print edge, edge.index
        pass


    """
    e1 = r1.edges()[0]
    e1a = g_me.edge(e1)
    assert(e1 == e1a)
    e2 = r1.edges()[1]
    assert(e1 != e2)
    #TODO: check why neq != also returns true for e1 != e1a
    """

    #print g_me.edge("r1", "r2", 0).index
    #print g_me.edge("r1", "r2", 1).index

    print "edges"
    for edge in g_me.edges():
        print edge

    out_of_order = [g_me.edge("r1", "r2", x) for x in [4, 1, 3, 2, 0]]
    #print [e.index for e in out_of_order]
    in_order = sorted(out_of_order)
    #print in_order
    #print [e.index for e in in_order]

    # test adding to another mutli edge graph
    print "adding"
    g_me2 = anm.add_overlay("multi2", multi_edge = True)
    g_me2.copy_nodes_from(g_me)
    print "add", len(g_me.edges())
    g_me2.copy_edges_from(g_me.edges())
    ank_utils.copy_edge_attr_from(g_me, g_me2, 'index')
    for edge in g_me2.edges():
        print edge, edge.get('index')

    # examine underlying nx structure


    #print graph
    #print type(graph)

    for u, v, k in graph.edges(keys=True):
        pass
        #print u, v, k
        #print graph[u][v][k].items()
        #graph[u][v][k]['test'] = 123

    g_dir = anm.add_overlay("dir", directed=True)
    g_dir.copy_nodes_from(g_phy)
    r1 = g_dir.node('r1')
    r2 = g_dir.node('r2')
    r3 = g_dir.node('r3')
    iface_r1 = r1.add_interface()
    iface_r2 = r2.add_interface()
    iface_r3 = r3.add_interface()
    g_dir.create_edge(iface_r1, iface_r2)
    g_dir.create_edge(iface_r2, iface_r1)
    g_dir.create_edge(iface_r1, iface_r3)

    g_dir_multi = anm.add_overlay("dir_multi", directed = True, multi_edge = True)
    g_dir_multi.copy_nodes_from(g_phy)
    r1 = g_dir_multi.node('r1')
    r2 = g_dir_multi.node('r2')
    r3 = g_dir_multi.node('r3')
    iface_r1 = r1.add_interface()
    iface_r2 = r2.add_interface()
    iface_r3 = r3.add_interface()
    g_dir_multi.create_edge(iface_r1, iface_r2)
    g_dir_multi.create_edge(iface_r1, iface_r2)
    g_dir_multi.create_edge(iface_r1, iface_r2)
    g_dir_multi.create_edge(iface_r1, iface_r2)
    g_dir_multi.create_edge(iface_r2, iface_r1)
    g_dir_multi.create_edge(iface_r2, iface_r1)
    g_dir_multi.create_edge(iface_r2, iface_r1)
    g_dir_multi.create_edge(iface_r2, iface_r1)
    g_dir_multi.create_edge(iface_r2, iface_r1)
    g_dir_multi.create_edge(iface_r1, iface_r3)

    for index, edge in enumerate(g_dir_multi.edges()):
        #print index, edge
        edge.set('index', "i_%s" % index)

    from networkx.readwrite import json_graph
    import json
    data = json_graph.node_link_data(graph)
    with open("multi.json", "w") as fh:
        fh.write(json.dumps(data, indent=2))

    autonetkit.update_http(anm)
