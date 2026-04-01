import bisect
import hashlib
from collections import defaultdict

from demo_utils import print_moved_keys, print_state, snapshot_assignments


class ConsistentHashingWithVnodes:
    def __init__(self, servers, vnodes=100):
        """Initialize the consistent hashing ring with virtual nodes."""
        self.vnodes = vnodes
        self.ring = []
        self.server_vnodes = defaultdict(list)
        self.node_map = {}

        for server in servers:
            self.add_server(server)

    def _hash(self, key):
        """Hash a key to a 64-bit integer."""
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def get_node(self, key):
        """Find the node by moving clockwise from the key's hash value."""
        if not self.ring:
            return None

        hash_value = self._hash(key)
        index = bisect.bisect_right(self.ring, hash_value)
        if index >= len(self.ring):
            index = 0

        vnode_hash = self.ring[index]
        return self.node_map[vnode_hash]

    def add_server(self, server):
        """Add a server to the consistent hashing ring."""
        for i in range(self.vnodes):
            vnode_hash = self._hash(f"{server}-{i}")
            bisect.insort(self.ring, vnode_hash)
            self.node_map[vnode_hash] = server
            self.server_vnodes[server].append(vnode_hash)

    def remove_server(self, server):
        """Remove a server from the consistent hashing ring."""
        if server not in self.server_vnodes:
            return

        for vnode_hash in self.server_vnodes[server]:
            index = bisect.bisect_left(self.ring, vnode_hash)
            if index < len(self.ring) and self.ring[index] == vnode_hash:
                self.ring.pop(index)
                del self.node_map[vnode_hash]

        del self.server_vnodes[server]


if __name__ == "__main__":
    data_keys = [f"user_{i}" for i in range(20)]
    print("---- Consistent Hashing With Virtual Nodes ----")

    initial_cluster = ConsistentHashingWithVnodes(
        servers=[f"Server {i}" for i in ["A", "B", "C"]],
        vnodes=100,
    )
    initial_assignments = snapshot_assignments(initial_cluster, data_keys)
    print_state("\n---- Initial State (3 Servers) ----", initial_cluster, data_keys)

    initial_cluster.add_server("Server D")
    after_add_assignments = snapshot_assignments(initial_cluster, data_keys)
    print_state("\n---- After Adding Server D ----", initial_cluster, data_keys)
    print_moved_keys("\n---- Nodes moved after adding ----", initial_assignments, after_add_assignments)

    initial_cluster.remove_server("Server C")
    after_remove_assignments = snapshot_assignments(initial_cluster, data_keys)
    print_state("\n---- After Removing Server C ----", initial_cluster, data_keys)
    print_moved_keys("\n---- Nodes moved after removing ----", after_add_assignments, after_remove_assignments)
