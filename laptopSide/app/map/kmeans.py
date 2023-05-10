import numpy as np



#global functions
def compute_distance(data, centers):
    """
    Compute the euclidean distance between each datapoint and each center.
    
    Arguments:    
        data: array of shape (N, D) where N is the number of data points, D is the number of features (:=pixels).
        centers: array of shape (K, D), centers of the K clusters.
    Returns:
        distances: array of shape (N, K) with the distances between the N points and the K clusters.
    """
    N = data.shape[0]
    K = centers.shape[0]

    ### WRITE YOUR CODE HERE
    # Here, we will loop over the cluster
    distances = np.zeros((N, K))
    for k in range(K):
        # Compute the euclidean distance for each data to each center
        center = centers[k]
        distances[:, k] = np.sqrt(((data - center) ** 2).sum(axis=1))
        
    return distances


def init_centers(data, K):
    """
    Randomly pick one data point from the data as first initial center, then 
    iteratively pick the next center from the remaining data points based on the 
    distance to the already picked centers, weighted by their distances to their 
    closest center. 

    This is the kmeans++ initialization, which generally leads to better results than 
    completely random initialization.

    Arguments: 
        data: array of shape (NxD) where N is the number of data points and D is the 
              number of features (:=pixels).
        K: int, the number of clusters.
        
    Returns:
        centers: array of shape (KxD) of initial cluster centers
    """
    centers = np.zeros((K, data.shape[1]))
    # Pick one center uniformly at random from the data
    centers[0] = data[np.random.choice(data.shape[0])]

    for i in range(1, K):
        # Compute the distance to the closest center for each data point
        distances = compute_distance(data, centers[:i])
        closest_distances = np.min(distances, axis=1)
        # Compute the weights as the squares of the distances to the closest centers
        weights = closest_distances**2
        # Normalize the weights
        weights /= np.sum(weights)
        # Pick the next center from the remaining data points based on the weights
        centers[i] = data[np.random.choice(data.shape[0], p=weights)]

    return centers

def find_closest_cluster(distances):
    """
    Assign datapoints to the closest clusters.
    
    Arguments:
        distances: array of shape (N, K), the distance of each data point to each cluster center.
    Returns:
        cluster_assignments: array of shape (N,), cluster assignment of each datapoint, which are an integer between 0 and K-1.
    """
    return np.argmin(distances, axis=1)


def compute_centers(data, cluster_assignments, K):
    """
    Compute the center of each cluster based on the assigned points.

    Arguments: 
        data: data array of shape (N,D), where N is the number of samples, D is number of features
        cluster_assignments: the assigned cluster of each data sample as returned by find_closest_cluster(), shape is (N,)
        K: the number of clusters
    Returns:
        centers: the new centers of each cluster, shape is (K,D) where K is the number of clusters, D the number of features
    """
    #initialization:
    centers = np.zeros((K, data.shape[1]))
    for k in range(K):
        cluster_points = data[cluster_assignments == k]
        if len(cluster_points) > 0:
            centers[k] = np.sum(cluster_points, axis=0) / len(cluster_points)
    return centers


class KMeans(object):


    """
    K-Means clustering class.

    We also use it to make prediction by attributing labels to clusters.
    """

    def __init__(self, K, max_iters=100):
        """
        Initialize the new object (see dummy_methods.py)
        and set its arguments.

        Arguments:
            K (int): number of clusters
            max_iters (int): maximum number of iterations
        """
        self.K = K
        self.max_iters = max_iters

    def k_means(self, data, max_iter):
        """
        Main K-Means algorithm that performs clustering of the data.
        
        Arguments: 
            data (array): shape (N,D) where N is the number of data samples, D is number of features.
            max_iter (int): the maximum number of iterations
        Returns:
            centers (array): shape (K,D), the final cluster centers.
            cluster_assignments (array): shape (N,) final cluster assignment for each data point.
        """
        centers = init_centers(data, self.K) # initializes randomly the cluster centers 
        sse = np.zeros(self.K) # initialize SSE for each cluster

        # Loop over the iterations to update the centers every iteration
        max_iter=100
        for i in range(max_iter): 
            if ((i+1) % 10 == 0):
                print(f"Iteration {i+1}/{max_iter}...")
        
            old_centers = centers.copy()  # keep in memory the centers of the previous iteration
            
            centers = compute_centers(data, find_closest_cluster(compute_distance(data,old_centers)),self.K)

            # End of the algorithm if the centers have not moved (hint: use old_centers and look into np.all)
            if np.allclose(old_centers, centers): #compare the old centers `old_centers` and the new centers `centers` of each iteration
                for k in range(self.K):
                    cluster_assignments = find_closest_cluster(compute_distance(data, centers))
                    sse[k] = np.sum((data[cluster_assignments == k] - old_centers[k])**2)

                print(f"K-Means has converged after {i+1} iterations! for K= {self.K}")
                break
        
        return centers, cluster_assignments, sse
    

    def fit(self, training_data):
        """
        Train the model and return predicted labels for training data.

        You will need to first find the clusters by applying K-means to
        the data, then to attribute a label to each cluster based on the labels.
        
        Arguments:
            training_data (array): training data of shape (N,D)
        Returns:
            pred_labels (array): labels of shape (N,)
        """

        ##
        # First, find the clusters by applying K-means to the data
        nbOfRun = self.K

        # create an empty list to store the sum of squared distances for each k value
        ssd = []
        centers = []
        for i in range(nbOfRun):

            self.K = i+1
            self.centers, cluster_assignments, sse = self.k_means(training_data, self.max_iters)
            centers.append(self.centers)
            ssd.append(sse)


        # find the value of k where the elbow curve is optimal
        optimal_K = self.K-1  # add 1 because of zero-based indexing and we skipped k=0
        print(f"The optimal value of k is {optimal_K}")


        return centers[self.K-1]


    def predict(self, data):
        """
        Assigns each data point to its closest cluster center.
        
        Arguments:
            data: array of shape (N, D) where N is the number of data points, D is the number of features.
        Returns:
            labels: array of shape (N,) with the cluster assignment of each data point.
        """
        distances = compute_distance(data, self.centers)
        labels = find_closest_cluster(distances)
        return labels
        



