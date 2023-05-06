# simple geometric functions
# primarly for 2d stuff 
import numpy as np

class Geometry:


    @staticmethod
    def unit(vector):
        """Spits out unit vectors

        Parameters
        ----------
        vector: ndarray (N, )

        Returns
        -------
        unit: ndarray (N, )
        """
        return vector / np.linalg.norm(vector)
    

    @staticmethod
    def distance(a, b):
        """ Calculates the squared distance

        Parameters
        ----------
        a: ndarray (N, )
            N-dim point
        b: ndarray (N, )
            N-dim point
        
        Returns
        -------
        distance: float
        """
        return np.linalg.norm(a - b)
    

    @staticmethod
    def closest_point(start, group):
        """ Find closest point in a group to an initial point

        Parameters
        ----------
        start: ndarray (N, )
            N-dim point
        group: ndarray (C, N)
            C N-dim points
        
        Returns
        -------
        closest: ndarray (N,)
            Closest point
        """
        if not(group):
            return None
        sq_distances = np.apply_along_axis(Geometry.sq_distance(), 1, group, start)
        return group[np.argmin(sq_distances)]
    
    
    @staticmethod
    def angle_X(v):
        v_u = Geometry.unit(v)


        return (np.sign(v[1]) * np.arccos(np.dot(v_u, np.array([1,0]))))% 2*np.pi


    @staticmethod
    def has_intersection(point, angle, a, b):
        """ Determines if a ray from a point with an angle will intersect the line AB

        Parameters
        ----------
        point: ndarray (N, )
        angle: float
            [0: 2 pi[
        a: ndarray (N, )
        b: ndarray (N, )
        
        Returns
        -------
        intersects: bool
        """
        ang_a, ang_b = Geometry.angle_X(a - point), Geometry.angle_X(b - point)
        max_ang, min_ang = max(ang_a, ang_b), min(ang_a, ang_b)

        return max_ang >= angle and min_ang <= angle
    
    @staticmethod
    def intersection(point, angle, a, b):
        if not(Geometry.has_intersection(point, angle, a, b)):
            return None
        
        

        return None