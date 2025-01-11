import random
class ClusterWorkerDistribution:
    def __init__(self, worker_nodes: list[dict[str, int]], cluster_infos: dict[str, dict[str, int]]) -> None:
        if not isinstance(worker_nodes, list) or not worker_nodes:
            print("Error: Worker nodes must be a non-empty list.")
        if not isinstance(cluster_infos, dict) or not cluster_infos:
            print("Error: cluster_info must be a non-empty dictionary.")
        self.worker_nodes = worker_nodes
        self.cluster_infos = cluster_infos

    def distribute_cluster_nodes(self) -> dict[int, list] | None:
        """Distributes microservice instances across worker nodes based on CPU and memory limits.

        Args:
            worker_nodes: A list of dictionaries, where each dictionary represents a worker node
                and contains 'cpu' and 'memory' (available resources).
            microservices: A dictionary where keys are microservice names and values are dictionaries
                containing 'cpu', 'memory', and 'instances' (number of instances required).

        Returns:
            A dictionary where keys are worker node indices and values are lists of tuples,
            where each tuple contains (microservice name, instance number). Returns None if input is invalid
            or distribution is impossible.
        """
        for node in self.worker_nodes:
            if not isinstance(node, dict) or "cpu" not in node or "memory" not in node:
                print("Error: Each worker node must have 'cpu' and 'memory' keys")
                return None
            if not isinstance(node["cpu"], (int, float)) or node["cpu"] < 0 or not isinstance(node["memory"],
                                                                                              (int, float)) or node[
                "memory"] < 0:
                print("Error: Worker node cpu and memory must be non-negative numbers")
                return None

        for service in self.cluster_infos.values():
            if not isinstance(service,
                              dict) or "cpu" not in service or "memory" not in service or "instances" not in service:
                print("Error: Each cluster inf must have 'cpu', 'memory' and 'instances' keys")
                return None
            if not isinstance(service["cpu"], (int, float)) or service["cpu"] < 0 or not isinstance(service["memory"],
                                                                                                    (int, float)) or \
                    service["memory"] < 0 or not isinstance(service["instances"], int) or service["instances"] <= 0:
                print(
                    "Error: Microservice cpu, memory must be non-negative numbers and instances must be positive integer")
                return None

        num_nodes = len(self.worker_nodes)
        distribution = {i: [] for i in range(num_nodes)}

        # Create a list of all microservice instances to distribute
        all_instances = []
        for cluster_name, requirements in self.cluster_infos.items():
            for instance_num in range(requirements['instances']):
                all_instances.append((cluster_name, instance_num))

        # Sort microservices by their combined resource requirements (descending) to attempt to fit larger services first
        sorted_instances = sorted(all_instances,
                                  key=lambda item: self.cluster_infos[item[0]]['cpu'] + self.cluster_infos[item[0]][
                                      'memory'], reverse=True)
        # print(sorted_instances)
        for service_name, instance_num in sorted_instances:
            requirements = self.cluster_infos[service_name]
            #print(requirements)
            best_node = -1
            min_resource_usage = float('inf')

            for i in range(num_nodes):
                node = self.worker_nodes[i]
                current_cpu_usage = sum(
                    self.cluster_infos[s]['cpu'] for s, _ in distribution[i] if s in self.cluster_infos)
                current_memory_usage = sum(
                    self.cluster_infos[s]['memory'] for s, _ in distribution[i] if s in self.cluster_infos)

                if (node['cpu'] >= current_cpu_usage + requirements['cpu'] and
                        node['memory'] >= current_memory_usage + requirements['memory']):
                    resource_usage = current_cpu_usage + requirements['cpu'] + current_memory_usage + requirements[
                        'memory']
                    if resource_usage < min_resource_usage:
                        min_resource_usage = resource_usage
                        best_node = i

            if best_node != -1:
                distribution[best_node].append((service_name, instance_num))
            else:
                print(
                    f"Warning: Could not place instance {instance_num} of microservice '{service_name}'. Insufficient resources on all nodes.")
                return None

        return distribution


def main():
    worker_nodes = [
        {'cpu': 20, 'memory': 24},
        {'cpu': 20, 'memory': 24},
        {'cpu': 20, 'memory': 24},
        {'cpu': 20, 'memory': 24}
    ]

    microservices = {
        'service_a': {'cpu': 3, 'memory': 5, 'instances': 2},
        'service_b': {'cpu': 2, 'memory': 3, 'instances': 3},
        'service_c': {'cpu': 5, 'memory': 8, 'instances': 4},
        'service_d': {'cpu': 4, 'memory': 4, 'instances': 8}
    }
    cwn = ClusterWorkerDistribution(worker_nodes, microservices)
    distribution = cwn.distribute_cluster_nodes()
    #print(distribution)
    if distribution:
        for node_index, services in distribution.items():
            print(f"Node {node_index + 1}: {services}")
            node_cpu_usage = sum(microservices[s]['cpu'] for s, _ in services if s in microservices)
            node_mem_usage = sum(microservices[s]['memory'] for s, _ in services if s in microservices)
            print(
                f"  CPU Usage: {node_cpu_usage}/{worker_nodes[node_index]['cpu']}, Memory Usage: {node_mem_usage}/{worker_nodes[node_index]['memory']}")

    # Example where a service cannot be placed.
    microservices_impossible = {
        'service_a': {'cpu': 3, 'memory': 5, 'instances': 2},
        'service_b': {'cpu': 2, 'memory': 3, 'instances': 3},
        'service_c': {'cpu': 15, 'memory': 20, 'instances': 1}  # This service cannot be placed.
    }
    cwn = ClusterWorkerDistribution(worker_nodes, microservices_impossible)
    distribution_impossible = cwn.distribute_cluster_nodes()

    # microservices_invalid = {
    # 'service_a': {'cpu': 3, 'memory': 5, 'instances': -2},
    # }
    # distribution_invalid_microservices = distribute_microservices(worker_nodes, microservices_invalid)
    #
    # microservices_invalid_keys = {
    # 'service_a': {'cpu': 3, 'memory': 5},
    # }
    # distribution_invalid_microservices_keys = distribute_microservices(worker_nodes, microservices_invalid_keys)

if __name__ == "__main__":
    main()
