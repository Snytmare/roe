#Recursive Onion Encryption
# Inspired by EMF-style recursive identity logic and TOR
# Each node stores identity and encryption keys temporarily

import random
import uuid

# ---------------------------
# Node Definition
# ---------------------------
class Node:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.temp_key = None
        self.visited = False

    def __repr__(self):
        return f"Node({self.name})"

    def generate_key(self):
        self.temp_key = f"key_{self.name}_{random.randint(1000,9999)}"
        return self.temp_key

    def provide_key(self):
        return self.temp_key

# ---------------------------
# Circuit Definition
# ---------------------------
class ROECircuit:
    def __init__(self, nodes):
        self.nodes = nodes
        self.path = []
        self.key_sequence = []

    def hop(self, from_node, to_node):
        print(f"Hopping: {from_node.name} ➔ {to_node.name}")
        to_node.visited = True
        self.path.append((from_node.name, to_node.name))

    def traverse(self):
        entry_node = random.choice(self.nodes)
        entry_node.visited = True
        print(f"\n✨ Entry Node: {entry_node.name}")
        entry_node.generate_key()

        # Hop forward to random node
        middle_node = random.choice([n for n in self.nodes if n != entry_node])
        self.hop(entry_node, middle_node)
        middle_node.generate_key()

        # Recursive hop back to entry to grab encryption key
        print("\n⟳ Recursing back to Entry Node for key...")
        encryption_key = entry_node.provide_key()
        self.key_sequence.append(encryption_key)
        print(f"Retrieved key from {entry_node.name}: {encryption_key}")

        # Final hop to exit node
        exit_node = random.choice([n for n in self.nodes if n != middle_node and n != entry_node])
        self.hop(middle_node, exit_node)
        exit_node.generate_key()
        self.key_sequence.append(exit_node.provide_key())

        print(f"\n🔐 Final key sequence: {self.key_sequence}")
        print(f"🔄 Routing path: {self.path}")


# ---------------------------
# Run Simulation
# ---------------------------
if __name__ == "__main__":
    node_pool = [Node(f"Node_{i}") for i in range(5)]
    roe = ROECircuit(node_pool)
    roe.traverse()
