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
        print(data_filter.shape)
        print(X.shape)
        print("label")
        print(labels.shape)
        cmap = plt.get_cmap('Set1')
        colors = cmap(np.arange(len(np.unique(labels_str)))).tolist()
        print(colors)
        label_color = [colors[i] for i in labels]


        # Create a scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data_filter[:, 0],
            y=data_filter[:, 1],
            mode='markers',
            marker=dict(color=label_color)
        ))
        print(data_filter)

      # Find the convex hull for each cluster
        for i in range(self.num_clusters):
            cluster_points = data_filter[labels == i]
            if cluster_points.size != 0 :
                hull = ConvexHull(cluster_points)
                fig.add_trace(go.Scatter(
                    x=data_filter[hull.vertices, 0],
                    y=data_filter[hull.vertices, 1],
                    fill='toself',
                    fillcolor=f'rgb({int(colors[i][0]*255)},{int(colors[i][1]*255)},{int(colors[i][2]*255)})',
                    line=dict(color=f'rgb({int(colors[i][0]*255)},{int(colors[i][1]*255)},{int(colors[i][2]*255)})'),
                    opacity=0.5
                ))

        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return chart_json

