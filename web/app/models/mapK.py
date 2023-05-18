import numpy as np
from scipy.spatial import ConvexHull
from app.models.kmeans import KMeans
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly
import json

class ClusterChart:
    def __init__(self, num_clusters=2):
        self.num_clusters = num_clusters


    def generate_chart_json(self):
        # Generate random data points
        X = np.random.rand(20, 2)

        # Apply K-means clustering
        kmeans1 = KMeans(self.num_clusters, X)
        centers = kmeans1.fit(X)
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

      # Find the convex hull for each cluster
        for i in range(self.num_clusters):
            cluster_points = X[labels == i]
            hull = ConvexHull(cluster_points)
            fig.add_trace(go.Scatter(
                x=cluster_points[hull.vertices, 0],
                y=cluster_points[hull.vertices, 1],
                fill='toself',
                fillcolor=f'rgb({int(colors[i][0]*255)},{int(colors[i][1]*255)},{int(colors[i][2]*255)})',
                line=dict(color=f'rgb({int(colors[i][0]*255)},{int(colors[i][1]*255)},{int(colors[i][2]*255)})'),
                opacity=0.2
            ))

        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return chart_json

