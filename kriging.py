import io
import base64

import pandas as pd
import numpy as np
from pyproj import Transformer
from matplotlib.image import imsave

from skgstat import Variogram, OrdinaryKriging

# PUT the target CRS here, where kriging will work for you
CRS = 25832
# Additionally specify the variogram and kriging parameters here
VARIO = dict(
    n_lags=8,
    estimator='matheron',
    model='exponential'
)
KRIG = dict(
    min_points=3,
    max_points=10
)
# specify the number of cells in each dimension
GRIDSIZE = 100
# alternatively, you can change the algorithm directly in the process function



def get_data(fname):
    df = pd.read_csv(fname)

    t = Transformer.from_crs(4326, CRS)

    x,y =t.transform(df.lon.values, df.lat.values)
    df['x'] = x
    df['y'] = y

    return df


def variogram(df, **kwargs):
    """
    Returns a variogram
    
    If you make changes to the coords.csv, eg. renaming the headers
    you have to change the code here as well
    """
    # load data
    coords = df[['x', 'y']].values
    values = df.carb.values

    return Variogram(coords, values, **kwargs)


def get_bounds(df):
    # get the bounds
    xmin = df.x.min()
    xmax = df.x.max()
    ymin = df.y.min()
    ymax = df.y.max()

    return xmin, xmax, ymin, ymax

def build_grid(df, resolution=100):
    """
    """
    xmin, xmax, ymin, ymax = get_bounds(df)
    xx, yy = np.mgrid[xmin:xmax:resolution*1j, ymin:ymax:resolution*1j]

    return xx, yy


def krig(vario, grid, **kwargs):
    # get the grid
    xx, yy = grid

    ok = OrdinaryKriging(vario, **kwargs)
    field = ok.transform(xx.flatten(), yy.flatten())
    sigma = ok.sigma

    return field.reshape(xx.shape), sigma.reshape(xx.shape)


def asBase64(field, name):
    f = io.BytesIO()

    vmin = 1.02 * np.nanmin(field)
    vmax = .98 * np.nanmax(field)
    imsave(f, np.fliplr(field), vmin=vmin, vmax=vmax, cmap='BuGn_r')

    f.seek(0)
    s = base64.b64encode(f.read())
    return 'data:image/png;base64,%s' % s.decode()


# Put your code into this function
# you can use the asBase64 function to 
# conver the field into a bas64 string
def process():
    print('loading data')
    df = get_data('coords.csv')

    grid = build_grid(df, GRIDSIZE)
    V = variogram(df, normalize=False, **VARIO)

    field, sigma = krig(V, grid, **KRIG)

    data = asBase64(field, 'field.png')
    # get the data bounds
    bounds = [[df.lat.max(), df.lon.min()], [df.lat.min(), df.lon.max()]]

    return data, bounds


if __name__ == '__main__':
    data, bounds = process()
    print('image bounds:', bounds)
    print('image URL:', data)