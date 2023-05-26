import numpy as np
from scipy.spatial import ConvexHull
from app.models.kmeans import KMeans
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import json

import matplotlib.cm as cm


class ClusterChart:
    def __init__(self, train_split=0.9, threshold=0.3, max_k = 40, filter=10):
        self.num_clusters = 0
        self.train_split = train_split
        self.threshold = threshold
        self.max_k = max_k
        self.filter = filter
        self.kmeans = KMeans( max_k=max_k, filter = filter )

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
                points = np.random.rand(100, 2) * 0.5 + center
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
                points = np.random.rand(100, 2) * 0.5 + center
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.09) & (distances >= 0.07)]
            elif shape_idx == 4:  # Hexagon
                points = np.random.rand(100, 2) * 0.4 + center
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.14) & (distances >= 0.1)]
            elif shape_idx == 5:  # Octagon
                points = np.random.rand(50, 2) * 0.6 + center
                distances = np.sqrt((points[:, 0] - center[0])**2 + (points[:, 1] - center[1])**2)
                points = points[(distances <= 0.14) | (distances >= 0.5)]
            
            # Add points to the data array
            X.extend(points)
        
        return np.array(X)
    def generate_chart_json(self, data):
        # Example usage
        num_shapes = 25

        if not data:
            data = self.generate_shapes(num_shapes)

        data = np.array(data)
        xtrain = data
        xtest = data

        split = int(data.shape[0] * self.train_split)
        mix = np.random.permutation(data.shape[0])
        xtrain, xtest = data[mix[:split]], data[mix[split:]]

        # Calculate mean and standard deviation from the training set
        x_mean = np.mean(xtrain, keepdims=True)
        x_std = np.std(xtrain, keepdims=True)

        # Normalize the training and test sets using the training set's statistics
        xtrain = (xtrain - x_mean) / x_std
        xtest = (xtest - x_mean) / x_std

        # Filter hence breaking the shape.  
    
        train_cluster_assignment, self.num_clusters = self.kmeans.fit(xtrain, self.threshold)

        # Predict on unseen data
        preds = self.kmeans.predict(xtest)

        ## Report results: performance on train and valid/test sets
        acc = self.accuracy_fn(preds, train_cluster_assignment)
        print(f"Test set:  accuracy = {acc:.3f}%")

        # Generate a color map with 100 colors
        color_map = cm.get_cmap('tab20',self.num_clusters)

        data = []
        layout = {
            'title': 'K-means Clustering with Geometrical Shapes',
            'xaxis': {'title': 'X'},
            'yaxis': {'title': 'Y'},
            'showlegend': True
        }

        # Initialize 'shapes' key with an empty list
        layout['shapes'] = []

        for label in np.unique(train_cluster_assignment):
            mask = train_cluster_assignment == label
            cluster_data = xtrain[mask]

            if label == 9999:
                # Add the cluster data points as red scatter markers without rectangle
                data.append({
                    'x': cluster_data[:, 0].tolist(),
                    'y': cluster_data[:, 1].tolist(),
                    'mode': 'markers',
                    'name': 'Cluster Noisy',
                    'marker': {'color': 'red'}
                })
            else:
                # Calculate the bounding box of the cluster
                min_x = np.min(cluster_data[:, 0])
                max_x = np.max(cluster_data[:, 0])
                min_y = np.min(cluster_data[:, 1])
                max_y = np.max(cluster_data[:, 1])

                # Create a unique color for the cluster based on its label
                color = color_map(label)
                
                # Adjust the alpha value of the fill color
                alpha = 0.4

                # Extract the RGB values from the color string
                rgb_values = color[:3]

                # Create the fill color with adjusted alpha value
                fill_color = f'rgba({rgb_values[0]}, {rgb_values[1]}, {rgb_values[2]}, {alpha})'

                # Add the rectangle marker to the plot
                layout['shapes'].append({
                    'type': 'rect',
                    'x0': min_x,
                    'y0': min_y,
                    'x1': max_x,
                    'y1': max_y,
                    'line': {'color': color},
                    'fillcolor': fill_color,
                    'name': f'Cluster {label}'
                })

                # Add the cluster data points as scatter markers with the same color as the rectangle
                data.append({
                    'x': cluster_data[:, 0].tolist(),
                    'y': cluster_data[:, 1].tolist(),
                    'mode': 'markers',
                    'name': f'Cluster {label}',
                    'marker': {'color': color}
                })

        chart_data = {'data': data, 'layout': layout}
        chart_json = json.dumps(chart_data)
        return chart_json
    def accuracy_fn(self,preds, train_cluster_assignment):
        if not (preds.any() and train_cluster_assignment.any()):
            return 0
        num_samples = preds.shape[0]
        num_clusters = max(max(train_cluster_assignment), max(preds)) + 1

        cluster_mapping = [-1] * num_clusters
        assigned_clusters = set()

        correct = 0

        for i in range(num_samples):
            pred_cluster = preds[i]
            true_cluster = train_cluster_assignment[i]

            if pred_cluster not in assigned_clusters:
                cluster_mapping[pred_cluster] = true_cluster
                assigned_clusters.add(pred_cluster)

            if cluster_mapping[pred_cluster] == true_cluster:
                correct += 1

        accuracy = correct / num_samples * 100
        return accuracy

        """Return the macro F1-score."""
        class_ids = np.unique(gt_labels)
        macrof1 = 0
        for val in class_ids:
            predpos = (pred_labels == val)
            gtpos = (gt_labels==val)
            
            tp = sum(predpos*gtpos)
            fp = sum(predpos*~gtpos)
            fn = sum(~predpos*gtpos)
            if tp == 0:
                continue
            else:
                precision = tp/(tp+fp)
                recall = tp/(tp+fn)

            macrof1 += 2*(precision*recall)/(precision+recall)

        return macrof1/len(class_ids)