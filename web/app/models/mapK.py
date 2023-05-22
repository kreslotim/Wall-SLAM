import numpy as np
from scipy.spatial import ConvexHull
from app.models.kmeans import KMeans
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly
from scipy.spatial import Delaunay
from alphashape import alphashape
import json

class ClusterChart:
    def __init__(self, num_clusters=2):
        self.num_clusters = num_clusters
    def generate_shapes(self,num_shapes):
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
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.09) & (distances >= 0.07)]
            elif shape_idx == 4:  # Hexagon
                points = np.random.rand(20, 2) * 0.4 + center
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.14) & (distances >= 0.1)]
            elif shape_idx == 5:  # Octagon
                points = np.random.rand(50, 2) * 0.6 + center
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.14) | (distances >= 0.5)]
            
            # Add points to the data array
            X.extend(points)
        
        return np.array(X)
    def generate_chart_json(self):
        # Example usage
        num_shapes = 50
        filter = 10
        X = self.generate_shapes(num_shapes)

        # Apply K-means clustering
        kmeans1 = KMeans(2*self.num_clusters, X, filter)
        data_filter,cluster_assignment, self.num_clusters = kmeans1.fit(X)
   
        labels = kmeans1.predict(data_filter)
        labels_str = labels.astype(str)  # convert to string array

            # Create the scatter plot with circle markers for each cluster
       # Create the scatter plot with cluster shapes
        fig = go.Figure()

        for label in np.unique(labels):
            mask = labels == label
            cluster_data = data_filter[mask]
            
            # Calculate the Delaunay triangulation of the cluster
            tri = Delaunay(cluster_data)
            
            # Define the alpha value to control the shape flexibility (smaller value for more flexibility)
            alpha = 1
            
            # Calculate the alpha shape of the cluster
            alpha_shape = alphashape(cluster_data, alpha)
            alpha_points = np.array(alpha_shape.exterior.coords)
            
            # Add the cluster shape to the plot
            fig.add_trace(go.Scatter(x=alpha_points[:, 0], y=alpha_points[:, 1], mode='lines', name=f'Cluster {label}'))

            # Add the cluster data points as scatter markers
            fig.add_trace(go.Scatter(x=cluster_data[:, 0], y=cluster_data[:, 1], mode='markers', name=f'Cluster {label}'))

        fig.update_layout(title='K-means Clustering with Cluster Shapes (Alpha Shapes)',
                        xaxis_title='X',
                        yaxis_title='Y',
                        showlegend=True)

 
        



        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return chart_json

