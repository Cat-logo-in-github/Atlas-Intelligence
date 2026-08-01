import networkx as nx


def build(simulation):
    graph = nx.DiGraph()

    nodes = [
        ("Left Eye", {"type": "sensory organ"}),
        ("Right Eye", {"type": "sensory organ"}),
        ("Optic Nerve", {"type": "cranial nerve"}),
        ("Optic Chiasm", {"type": "crossing point"}),
        ("Left Optic Tract", {"type": "visual pathway"}),
        ("Right Optic Tract", {"type": "visual pathway"}),
        ("Lateral Geniculate Nucleus", {"type": "thalamus relay"}),
        ("Optic Radiation", {"type": "white matter pathway"}),
        ("Primary Visual Cortex (V1)", {"type": "occipital cortex"}),
        ("Visual Association Cortex", {"type": "higher visual processing"}),
        ("Dorsal Stream (Where Pathway)", {"type": "spatial processing"}),
        ("Ventral Stream (What Pathway)", {"type": "object recognition"}),
        ("Parietal Cortex", {"type": "spatial awareness"}),
        ("Temporal Cortex", {"type": "object and face recognition"}),
        ("Prefrontal Cortex", {"type": "attention and decision making"}),
        ("Superior Colliculus", {"type": "visual reflex processing"}),
    ]

    graph.add_nodes_from(nodes)

    edges = [
        ("Left Eye", "Optic Nerve", "photoreceptor signals from left retina"),
        ("Right Eye", "Optic Nerve", "photoreceptor signals from right retina"),
        ("Optic Nerve", "Optic Chiasm", "carries retinal visual information"),
        ("Optic Chiasm", "Left Optic Tract", "crossed and uncrossed fibers reorganized"),
        ("Optic Chiasm", "Right Optic Tract", "crossed and uncrossed fibers reorganized"),
        ("Left Optic Tract", "Lateral Geniculate Nucleus", "relays visual signals through thalamus"),
        ("Right Optic Tract", "Lateral Geniculate Nucleus", "relays visual signals through thalamus"),
        ("Lateral Geniculate Nucleus", "Optic Radiation", "thalamocortical visual transmission"),
        ("Optic Radiation", "Primary Visual Cortex (V1)", "delivers processed visual signals to occipital lobe"),
        ("Primary Visual Cortex (V1)", "Visual Association Cortex", "extracts edges, shapes, motion, and patterns"),
        ("Visual Association Cortex", "Dorsal Stream (Where Pathway)", "routes information for location and movement"),
        ("Visual Association Cortex", "Ventral Stream (What Pathway)", "routes information for identity and recognition"),
        ("Dorsal Stream (Where Pathway)", "Parietal Cortex", "supports spatial awareness and visual guidance"),
        ("Ventral Stream (What Pathway)", "Temporal Cortex", "supports object and face recognition"),
        ("Visual Association Cortex", "Prefrontal Cortex", "supports attention and conscious interpretation"),
        ("Optic Nerve", "Superior Colliculus", "supports rapid visual reflex responses"),
        ("Superior Colliculus", "Prefrontal Cortex", "contributes to attention and orienting responses"),
    ]

    for source, target, explanation in edges:
        graph.add_edge(
            source,
            target,
            weight=explanation
        )

    simulation.graph(graph, "visual_pathway_brain_network")