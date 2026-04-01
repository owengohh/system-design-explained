# Consistent Hashing Examples

This folder contains three small Python scripts that demonstrate different hashing strategies:

- `simple_hashing.py` - basic modulo-based hashing
- `basic_consistent_hashing.py` - consistent hashing with a single vnode per server
- `consistent_hashing_vnodes.py` - consistent hashing with virtual nodes

## Quick Comparison

| Script | Technique | Distribution | Key Movement on Change | Best For |
| --- | --- | --- | --- | --- |
| `simple_hashing.py` | Hash % number of servers | Can be uneven | High | Showing the simplest possible baseline |
| `basic_consistent_hashing.py` | Consistent hash ring | Usually better than modulo, but can still be uneven | Lower than simple hashing | Introducing the ring concept |
| `consistent_hashing_vnodes.py` | Consistent hashing with virtual nodes | Usually the smoothest of the three | Lowest of the three in most cases | Showing why virtual nodes help |

## Requirements

- Python 3

No third-party packages are required.

## How to run

From this directory, run any script with `python3`:

```bash
python3 simple_hashing.py
python3 basic_consistent_hashing.py
python3 consistent_hashing_vnodes.py
```

Each script prints:

- the initial key distribution across servers
- the distribution after adding `Server D`
- the distribution after removing `Server C`
- the keys that moved between servers after each change

## What to expect

- `simple_hashing.py` will usually move a lot of keys when the server list changes.
- `basic_consistent_hashing.py` should move fewer keys than simple hashing.
- `consistent_hashing_vnodes.py` should usually give the smoothest distribution and the fewest key movements of the three.

## Notes

- The demo data uses 20 sample keys: `user_0` through `user_19`.
- The examples are intentionally small so the movement between scenarios is easy to read.
