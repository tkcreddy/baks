import random

def distribute_pods(nodes, applications):
    """Distributes fruit varieties across nodes with balanced counts.

    Args:
        nodes: The number of nodes (n).
        applications: A dictionary where keys are fruit names and values are their quantities.

    Returns:
        A list of dictionaries, where each dictionary represents a node and contains
        the distributed fruits and their quantities. Returns None if input is invalid.
    """

    if not isinstance(nodes, int) or nodes <= 0:
        print("Error: Number of nodes must be a positive integer.")
        return None
    if not isinstance(applications, dict) or not applications:
        print("Error: Applications must be a non-empty dictionary.")
        return None
    for quantity in applications.values():
        if not isinstance(quantity, int) or quantity < 0:
            print("Error: Pod quantities must be non-negative integers.")
            return None

    distributed_nodes = [{} for _ in range(nodes)]
    total_pods = sum(applications.values())

    if total_pods < nodes:
        print("Warning: There are fewer pods than nodes. Some nodes will be empty or have less variety.")

    # Calculate target number of fruits per node
    target_per_node = total_pods // nodes
    remainder = total_pods % nodes

    for i in range(remainder):
        distributed_nodes[i]["remainder_pod"] = distributed_nodes[i].get("remainder_pod",0)+1

    for application, quantity in applications.items():
        if quantity == 0:
            continue
        for _ in range(quantity):
            min_node_index = 0
            min_count = sum(distributed_nodes[0].values())
            for i in range(1, nodes):
                current_count = sum(distributed_nodes[i].values())
                if current_count < min_count:
                    min_count = current_count
                    min_node_index = i

            distributed_nodes[min_node_index][application] = distributed_nodes[min_node_index].get(application, 0) + 1

    #Remove the remainder fruit key.
    for node in distributed_nodes:
        if "remainder_pod" in node:
            del node["remainder_pod"]


    return distributed_nodes

# Example usage:
num_nodes = 5
pods = {
    "app1": 12,
    "app2": 8,
    "app3": 5,
    "app4": 3,
    "app5": 0,
    "app6": 12,
    "app7": 20
}

distributed_result = distribute_pods(num_nodes, pods)

if distributed_result:
    for i, node in enumerate(distributed_result):
        print(f"node {i + 1}: {node} (Total: {sum(node.values())})")
