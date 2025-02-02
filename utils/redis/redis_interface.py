import redis
import json


class RedisInterface:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # Nodes Storage
    def save_node(self, name, ipaddress):
        self.redis_client.hset("nodes", name, json.dumps({"ipaddress": ipaddress}))

    def get_nodes(self):
        nodes = self.redis_client.hgetall("nodes")
        return {name: json.loads(data) for name, data in nodes.items()}

    # Get a Node by Name
    def get_node_by_name(self, name):
        data = self.redis_client.hget("nodes", name)
        return json.loads(data) if data else None

    # Get a Node by IP Address (Search All Nodes)
    def get_node_by_ip(self, ipaddress):
        nodes = self.redis_client.hgetall("nodes")
        for name, data in nodes.items():
            node_data = json.loads(data)
            if node_data["ipaddress"] == ipaddress:
                return {"name": name, "ipaddress": node_data["ipaddress"]}
        return None

    # Container Storage
    def save_container(self, container_name, ipaddress, node):
        self.redis_client.hset("containers", container_name, json.dumps({"ipaddress": ipaddress, "node": node}))

    def get_containers(self):
        containers = self.redis_client.hgetall("containers")
        return {cid: json.loads(data) for cid, data in containers.items()}

    # Get a Container by Name
    def get_container_by_name(self, name):
        data = self.redis_client.hget("containers", name)
        return json.loads(data) if data else None

    def get_containers_node(self, node_name):
        containers_on_node = []
        containers = self.redis_client.hgetall("containers")
        for name, data in containers.items():
            containers_data = json.loads(data)
            if containers_data["node"] == node_name:
                containers_on_node.append(name)
                return containers_on_node
        return None

    # Namespace to Node Mapping
    def save_namespace_mapping(self, namespace, node):
        self.redis_client.hset("namespace_mapping", namespace, node)

    def get_namespace_mappings(self):
        return self.redis_client.hgetall("namespace_mapping")

    # Container to App Cluster Mapping
    def save_container_cluster(self, container_id, cluster):
        self.redis_client.hset("container_clusters", container_id, cluster)

    def get_container_clusters(self):
        return self.redis_client.hgetall("container_clusters")

    # Cluster Health Check Configuration
    def save_cluster_health(self, cluster, port, url, interval, checks):
        self.redis_client.hset("cluster_health", cluster, json.dumps({
            "port": port,
            "url": url,
            "interval": interval,
            "checks": checks
        }))

    def get_cluster_health(self):
        clusters = self.redis_client.hgetall("cluster_health")
        return {cluster: json.loads(data) for cluster, data in clusters.items()}

    # Healthy Containers in a Cluster
    def add_healthy_container(self, cluster, container_id):
        self.redis_client.sadd(f"healthy_containers:{cluster}", container_id)

    def get_healthy_containers(self, cluster):
        return self.redis_client.smembers(f"healthy_containers:{cluster}")
#
# # Usage Example
# redis_manager = RedisClusterManager()
#
# # Store Nodes
# redis_manager.save_node("node1", "192.168.1.1")
# redis_manager.save_node("node2", "192.168.1.2")
#
# # Store Containers
# redis_manager.save_container("container1", "10.0.0.1", "node1")
# redis_manager.save_container("container2", "10.0.0.2", "node2")
#
# # Namespace to Node Mapping
# redis_manager.save_namespace_mapping("namespace1", "node1")
# redis_manager.save_namespace_mapping("namespace2", "node2")
#
# # Container to Cluster Mapping
# redis_manager.save_container_cluster("container1", "cluster1")
# redis_manager.save_container_cluster("container2", "cluster2")
#
# # Cluster Health Configuration
# redis_manager.save_cluster_health("cluster1", 8080, "http://cluster1/health", 30, 3)
# redis_manager.save_cluster_health("cluster2", 9090, "http://cluster2/health", 60, 5)
#
# # Add Healthy Containers
# redis_manager.add_healthy_container("cluster1", "container1")
# redis_manager.add_healthy_container("cluster2", "container2")
#
# # Retrieve Data
# print("Nodes:", redis_manager.get_nodes())
# print("Containers:", redis_manager.get_containers())
# print("Namespace Mappings:", redis_manager.get_namespace_mappings())
# print("Container Clusters:", redis_manager.get_container_clusters())
# print("Cluster Health Config:", redis_manager.get_cluster_health())
# print("Healthy Containers in Cluster1:", redis_manager.get_healthy_containers("cluster1"))
