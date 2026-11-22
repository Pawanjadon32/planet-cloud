"""
GKE Cluster — Pulumi Python
GCP par infovista-gke-cluster banata hai
"""

import pulumi
import pulumi_gcp as gcp

# ── Config ────────────────────────────────────────────────────────────────
config       = pulumi.Config()
project_id   = config.get("projectId")   or "infovista-510914"
region       = config.get("region")      or "asia-south1"
zone         = config.get("zone")        or "asia-south1-a"
cluster_name = config.get("clusterName") or "infovista-gke-cluster"
node_count   = config.get_int("nodeCount") or 2
machine_type = config.get("machineType") or "e2-medium"

# ── GKE Cluster ───────────────────────────────────────────────────────────
cluster = gcp.container.Cluster(
    cluster_name,
    name                     = cluster_name,
    location                 = zone,
    project                  = project_id,
    remove_default_node_pool = True,
    initial_node_count       = 1,
    deletion_protection      = False,

    addons_config = gcp.container.ClusterAddonsConfigArgs(
        http_load_balancing = gcp.container.ClusterAddonsConfigHttpLoadBalancingArgs(
            disabled=False
        ),
    ),
    opts = pulumi.ResourceOptions(ignore_changes=["node_config"])
)

# ── Node Pool ─────────────────────────────────────────────────────────────
node_pool = gcp.container.NodePool(
    f"{cluster_name}-nodes",
    name       = f"{cluster_name}-nodes",
    location   = zone,
    cluster    = cluster.name,
    project    = project_id,
    node_count = node_count,

    node_config = gcp.container.NodePoolNodeConfigArgs(
        machine_type = machine_type,
        disk_size_gb = 50,
        disk_type    = "pd-standard",
        oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"],
        labels       = {"env": "production"},
    ),

    autoscaling = gcp.container.NodePoolAutoscalingArgs(
        min_node_count = 1,
        max_node_count = 5,
    ),

    management = gcp.container.NodePoolManagementArgs(
        auto_repair  = True,
        auto_upgrade = True,
    ),
)

# ── Outputs ───────────────────────────────────────────────────────────────
pulumi.export("cluster_name",     cluster.name)
pulumi.export("cluster_endpoint", pulumi.Output.secret(cluster.endpoint))
pulumi.export("cluster_zone",     zone)
pulumi.export("project_id",       project_id)
