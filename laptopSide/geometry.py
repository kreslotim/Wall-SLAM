# simple geometric functions
# primarly for 2d stuff 
import numpy as np

class geometry:


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
    def angle_unit(angle):
        return np.array([np.cos(angle), np.sin(angle)])
    

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
        if group is None:
            return None
        sq_distances = np.apply_along_axis(geometry.distance, 1, group, start)
        return group[np.argmin(sq_distances)]
    

    @staticmethod
    def ray_param(p, alpha):
        m_p = np.tan(alpha)
        x_p = p[1] - m_p * p[0]
        return m_p, x_p

    @staticmethod
    def line_param(a, b):
        m_l = (b[1] - a[1])/(b[0] - a[0])
        x_l = a[1] - m_l * a[0]
        return m_l, x_l
    
    @staticmethod
    def double_linear_intersection(m_a, x_a, m_b, x_b):
        if m_a == m_b:
            if(x_a == x_b):
                return np.array([np.Infinity])
            return np.array([None])
        
        x_i = - (x_a - x_b)/(m_a - m_b)
        return np.array([x_i, m_a * x_i + x_a])
    

    @staticmethod
    def linear_constant_intersection(m, b, x):
        return np.array([x, m*x + b])


    @staticmethod
    def within_range(p, alpha, a, b, i):
        if not(min(a[0], b[0]) <= i[0] and max(a[0], b[0]) >= i[0]):
            return False
        
        return p[0] <= i[0] if(alpha < 0.5 * np.pi or alpha > 1.5 * np.pi) else p[0] >= i[0]


    @staticmethod
    def ray_intersection(p, alpha, a, b):
        p_vert = alpha == 0.5 * np.pi or alpha == 1.5 * np.pi
        l_vert = a[0] == b[0]
        
        if(int(p_vert) + int(l_vert) == 2):   ## If double vertical lines
            if(p[0] != a[0]):
                return None
            
            i = geometry.closest_point(p, np.array([a, b]))
            if (alpha == 0.5 * np.pi):
                return i if(i[1] >= p[1]) else None
            else:
                return i if(i[1] <= p[1]) else None
  
        i = None
        if(p_vert + l_vert == 0):   ## If double non-verticla lines
            ## Slopes
            m_p, x_p = geometry.ray_param(p, alpha)
            m_l, x_l = geometry.line_param(a, b)

            i = geometry.double_linear_intersection(m_p, x_p, m_l, x_l)
            
            if i[0] is None:
                return None
            elif(i[0] == np.Infinity):
                i = geometry.closest_point(p, np.array([a, b]))
        else:                       ## If one vertical line
            m, q, x = None, None, None
            if(p_vert):
                m, q = geometry.line_param(a,b)
                x = p[0]
            else:
                m, q = geometry.ray_param(p, alpha)
                x = a[0]

            i = geometry.linear_constant_intersection(m, q, x)

            if(i[1] > max(a[1], b[1]) or i[1] < min(a[1], b[1])):
                return None
            
        return i if(geometry.within_range(p, alpha, a, b, i)) else None