#-------------------------------------------------------------------------------
# Name:        ipol
# Purpose:
#
# Authors:     Maik Heistermann, Stephan Jacobi and Thomas Pfaff
#
# Created:     26.10.2011
# Copyright:   (c) Maik Heistermann, Stephan Jacobi and Thomas Pfaff 2011
# Licence:     The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""
Interpolation
^^^^^^^^^^^^^

Interpolation allows to transfer data from one set of locations to another.
This includes for example:
- interpolating the data from a polar grid to a cartesian grid or irregular points

.. autosummary::
   :nosignatures:
   :toctree: generated/

   Nearest


"""

from scipy.spatial import cKDTree
import numpy as np


class Nearest():
    """
    Nearest(src, trg)

    Nearest-neighbour interpolation in N dimensions.

    Parameters
    ----------
    src : ndarray of floats, shape (npoints, ndims)
        Data point coordinates of the source points.
    trg : ndarray of floats, shape (npoints, ndims)
        Data point coordinates of the target points.

    Notes
    -----
    Uses ``scipy.spatial.cKDTree``

    """

    def __init__(self, src, trg):
        src = self._make_coord_arrays(src)
        trg = self._make_coord_arrays(trg)
        # remember some things
        self.numtargets = len(trg)
        self.numsources = len(src)
        # plant a tree
        self.tree = cKDTree(src)
        self.dists, self.ix = self.tree.query(trg, k=1)
    def __call__(self, vals, maxdist=None):
        """
        Evaluate interpolator for values given at the source points.

        Parameters
        ----------
        vals : ndarray of float, shape (numsources)
            Values at the source points which to interpolate
        maxdist : the maximum distance up to which an interpolated values is
            assigned - if maxdist is exceeded, np.nan will be assigned
            If maxdist==None, values will be assigned everywhere

        Returns
        -------
        output : ndarray of float with shape (numtargetpoints,...)

        """
        self._check_shape(vals)
        out = vals[self.ix]
        if maxdist==None:
            return out
        else:
            return np.where(self.dists>maxdist, np.nan, out)
    def _check_shape(self, vals):
        """
        Checks whether the values correspond to the source points

        Parameters
        ----------
        vals : ndarray of float
        """
        assert len(vals)==self.numsources, 'Length of value array %d does not correspond to \
        number of source points %d' % (len(vals), self.numsources)
    def _make_coord_arrays(self, x):
        """
        Make sure that the coordinates are provided as ndarray
        of shape (numpoints, ndim)

        Parameters
        ----------
        x : ndarray of float with shape (numpoints, ndim)
            OR a sequence of ndarrays of float with len(sequence)==ndim and the length
            of the ndarray corresponding to the number of points

        """
        if type(x) in [list, tuple]:
            x = [item.ravel() for item in x]
            x = np.array(x).transpose()
        elif type(x)==np.ndarray:
            if x.ndim==1:
                x = x.reshape(-1,1)
            elif x.ndim==2:
                pass
            else:
                raise Exception('Cannot deal wih 3-d ')
        return x



if __name__ == '__main__':
    import datetime as dt
    import pylab as pl
    from scipy.interpolate import griddata
    xsrc = np.loadtxt('../examples/data/bin_coords.dat')
#    xtrg = np.loadtxt('../examples/data/target_coords.dat')
    xtrg = np.meshgrid(np.linspace(3300000.0, 3300000.0+900000,900), np.linspace(5200000.0, 5200000.0+900000.,900))
#    xtrg = np.transpose(np.vstack((xtrg[0].ravel(), xtrg[1].ravel())))
    vals = np.loadtxt('../examples/data/polar_R.dat').ravel()

    print 'Linear interpolation takes:'
    t0 = dt.datetime.now()
    test = griddata(xsrc, vals, xtrg, 'linear')
    print dt.datetime.now()-t0
##    pl.scatter(xtrg[0], xtrg[1], c=test.ravel(), s=5, edgecolor='none')
##    pl.show()
##    pl.close()

##    print 'Building the object takes:'
##    t0 = dt.datetime.now()
##    ip = NearestNDInterpolator(xsrc, vals)
##    print dt.datetime.now()-t0
##    print 'Calling the object takes:'
##    t0 = dt.datetime.now()
##    test = ip(xtrg)
##    print dt.datetime.now()-t0
##    pl.scatter(xtrg[0], xtrg[1], c=test.ravel(), s=5, edgecolor='none')
##    pl.show()
##    pl.close()

    print 'Building our object takes:'
    t0 = dt.datetime.now()
    ip = Nearest(xsrc, xtrg)
    print dt.datetime.now()-t0
    print 'Calling the object takes:'
    t0 = dt.datetime.now()
    test = ip(vals)
    print dt.datetime.now()-t0
    pl.scatter(xtrg[0].ravel(), xtrg[1].ravel(), c=test.ravel(), s=5, edgecolor='none')
    pl.show()
    pl.close()

    xsrc = np.arange(10)[:,None]
    xtrg = np.linspace(0,20,40)[:,None]
    vals = np.sin(xsrc).ravel()
    ip = Nearest(xsrc, xtrg)
    test = ip(vals)
    print vals, test
    pl.plot(xsrc.ravel(), vals, 'b+')
    pl.plot(xtrg.ravel(), test, 'r+')
    pl.show()
    pl.close()



    print 'wradlib: Calling module <ipol> as main...'