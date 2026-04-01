from collections import defaultdict


def build_state(cluster, keys):
    state = defaultdict(list)
    for key in keys:
        state[cluster.get_node(key)].append(key)
    return dict(sorted(state.items()))


def print_state(title, cluster, keys):
    print(title)
    state = build_state(cluster, keys)
    for server, users in state.items():
        print(f"{server}: {', '.join(users)}")


def snapshot_assignments(cluster, keys):
    return {key: cluster.get_node(key) for key in keys}


def print_moved_keys(title, old_assignments, new_assignments):
    print(title)
    moved_count = 0
    for key, old_server in old_assignments.items():
        new_server = new_assignments[key]
        if old_server != new_server:
            moved_count += 1
            print(f"{key}: moved from {old_server} to {new_server}")
    print(f"\nTotal nodes moved: {moved_count}")
