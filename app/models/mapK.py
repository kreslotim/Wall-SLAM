import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from kmeans import KMeans



    # Generate random data points
X = np.random.rand(100, 2)

# Apply K-means clustering
K = 10
kmeans1 = KMeans(K, X)
centers = kmeans1.fit(X)
labels = kmeans1.predict(X)
labels_str = labels.astype(str) # convert to string array

cmap = plt.get_cmap('Set1')
colors = cmap(np.arange(len(np.unique(labels_str)))).tolist()
label_color = [colors[i] for i in labels]

# Plot the clusters
plt.scatter(X[:,0], X[:,1], c=label_color)

# Find the convex hull for each cluster
for i in range(10):
    cluster_points = X[labels == i]
    hull = ConvexHull(cluster_points)
    plt.fill(cluster_points[hull.vertices,0], cluster_points[hull.vertices,1], alpha=0.2)

plt.show()
