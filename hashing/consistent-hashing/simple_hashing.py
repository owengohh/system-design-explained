import hashlib

from demo_utils import print_moved_keys, print_state, snapshot_assignments


class SimpleHashing:
    def __init__(self, servers) -> None:
        """
        Initializes the SimpleHashing object with a list of servers.
        """
        self.servers = list(servers)

    def _hash(self, key):
        """
        Computes the hash value for a given key.
        """
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def get_node(self, key):
        """
        Find which server a key belongs to using simple modulo math
        """
        if not self.servers:
            return None
        return self.servers[self._hash(key) % len(self.servers)]

    def add_server(self, server):
        """Add a server to the cluster."""
        self.servers.append(server)

    def remove_server(self, server):
        """Remove a server from the cluster."""
        if server in self.servers:
            self.servers.remove(server)


if __name__ == "__main__":
    data_keys = [f"user_{i}" for i in range(20)]
    print("---- Simple Hashing ----")

    initial_cluster = SimpleHashing(servers=[f"Server {i}" for i in ["A", "B", "C"]])
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
