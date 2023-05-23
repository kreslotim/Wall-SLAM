import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import ConvexHull
from app.models.kmeans import KMeans
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly
import json

class ClusterChart:
    def __init__(self, num_clusters=2):
        self.num_clusters = num_clusters

    from sklearn.neighbors import NearestNeighbors

    from sklearn.neighbors import NearestNeighbors

    def generate_shapes(self, num_shapes, min_neighbors=6):
        X = []
        shape_names = ['Triangle', 'Circle', 'Square', 'Pentagon', 'Hexagon', 'Octagon']

        for _ in range(num_shapes):
            # Randomly choose a shape
            shape_idx = np.random.randint(6)
            shape_name = shape_names[shape_idx]

            # Randomly generate center coordinates within (0-4, 0-4)
            center = np.random.rand(2) * 4

            # Generate points for the selected shape
            if shape_idx == 0:  # Triangle
                points = np.random.rand(50, 2) * 0.5 + center
                points = points[(points[:, 0] + points[:, 1] <= 0.6) & (points[:, 0] >= 0.5) & (points[:, 1] >= 0.5)]
            elif shape_idx == 1:  # Circle
                points = np.random.rand(100, 2) * 0.5 + center
                distances = np.linalg.norm(points - center, axis=1)
                points = points[distances <= 0.1]
            elif shape_idx == 2:  # Square
                points = np.random.rand(200, 2) * 0.5 + center
                points = points[(points[:, 0] >= center[0] - 0.1) & (points[:, 0] <= center[0] + 0.1) &
                                (points[:, 1] >= center[1] - 0.1) & (points[:, 1] <= center[1] + 0.1)]
            elif shape_idx == 3:  # Pentagon
                points = np.random.rand(20, 2) * 0.5 + center
                distances = np.sqrt((points[:, 0] - center[0]) ** 2 + (points[:, 1] - center[1]) ** 2)
                points = points[(distances <= 0.09) & (distances >= 0.07)]
            elif shape_idx == 4:  # Hexagon
                points = np.random.rand(20, 2) * 0.4 + center
                distances = np.sqrt((points[:, 0] - center[0]) ** 2 + (points[:, 1] - center[1]) ** 2)
                points = points[(distances <= 0.14) & (distances >= 0.1)]
            elif shape_idx == 5:  # Octagon
                points = np.random.rand(50, 2) * 0.6 + center
                distances = np.sqrt((points[:, 0] - center[0]) ** 2 + (points[:, 1] - center[1]) ** 2)
                points = points[(distances <= 0.14) | (distances >= 0.5)]

            # Remove points based on density using K-nearest neighbors
            if len(points) >= min_neighbors:
                nbrs = NearestNeighbors(n_neighbors=min_neighbors).fit(points)
                distances, _ = nbrs.kneighbors(points)
                avg_distances = np.mean(distances, axis=1)
                points = points[avg_distances >= np.percentile(avg_distances, 25)]

            # Add points to the data array
            X.extend(points)

        return np.array(X)
    def generate_chart_json(self):
        # Example usage
        num_shapes = 50
        X = self.generate_shapes(num_shapes)

        # Apply K-means clustering
        kmeans1 = KMeans(2*self.num_clusters, X)
        result = kmeans1.fit(X)
        self.num_clusters = result[1]
        print(result[1])
        labels = kmeans1.predict(X)
        labels_str = labels.astype(str)  # convert to string array

        cmap = plt.get_cmap('Set1')
        colors = cmap(np.arange(len(np.unique(labels_str)))).tolist()
        label_color = [colors[i] for i in labels]

        # Create a scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=X[:, 0],
            y=X[:, 1],
            mode='markers',
            marker=dict(color=label_color)
        ))

        # Plot the clusters

        plt.scatter(X[:, 0], X[:, 1], c=label_color)

        # Find the convex hull for each cluster
        for i in range(self.num_clusters):
            cluster_points = X[labels == i]
            hull = ConvexHull(cluster_points)
            plt.fill(cluster_points[hull.vertices, 0], cluster_points[hull.vertices, 1], alpha=0.2)

        plt.show()
        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return chart_json


