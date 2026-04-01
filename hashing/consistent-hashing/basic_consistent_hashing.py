import hashlib
import bisect

from demo_utils import print_moved_keys, print_state, snapshot_assignments


class BasicConsistentHashing:
    def __init__(self, servers):
        """Initialize the consistent hashing with a list of servers."""
        self.ring = []
        self.node_map = {}  # maps a hash integer back to server name

        for server in servers:
            self.add_server(server)

    def _hash(self, key):
        """Hash the key using MD5 and return the integer value."""
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def get_node(self, key):
        """Find the node by moving clockwise from the key's hash value."""
        if not self.ring:
            return None
        hash_value = self._hash(key)
        index = bisect.bisect_right(self.ring, hash_value)
        if index >= len(self.ring):
            index = 0
        return self.node_map[self.ring[index]]

    def add_server(self, server):
        """Add a server to the consistent hash ring."""
        hash_value = self._hash(server)
        bisect.insort(self.ring, hash_value)
        self.node_map[hash_value] = server

    def remove_server(self, server):
        """Remove a server from the consistent hash ring."""
        hash_value = self._hash(server)
        if hash_value not in self.node_map:
            return

        index = bisect.bisect_left(self.ring, hash_value)
        if index < len(self.ring) and self.ring[index] == hash_value:
            self.ring.pop(index)
            del self.node_map[hash_value]


if __name__ == "__main__":
    data_keys = [f"user_{i}" for i in range(20)]
    print("---- Basic Consistent Hashing ----")
    initial_ring = BasicConsistentHashing(servers=[f"Server {i}" for i in ["A", "B", "C"]])
    initial_assignments = snapshot_assignments(initial_ring, data_keys)
    print_state("\n---- Initial State (3 Servers) ----", initial_ring, data_keys)

    initial_ring.add_server("Server D")
    after_add_assignments = snapshot_assignments(initial_ring, data_keys)
    print_state("\n---- After Adding Server D ----", initial_ring, data_keys)
    print_moved_keys("\n---- Nodes moved after adding ----", initial_assignments, after_add_assignments)

    initial_ring.remove_server("Server C")
    after_remove_assignments = snapshot_assignments(initial_ring, data_keys)
    print_state("\n---- After Removing Server C ----", initial_ring, data_keys)
    print_moved_keys("\n---- Nodes moved after removing ----", after_add_assignments, after_remove_assignments)
