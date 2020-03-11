# skgstat-leaflet
A demo how to display skgstat interpolations on a leaflet map

This is just a demo project and not meant to be used for production cases. It assumes that you

* have a list of coordinates in a csv with heading lat,lon,carb
* use skgstat to interpolate the coordinates
* want to display the map and the coordinate locations on a leaflet map

I will try to rework the example to work with any input and be more flexible on output. This is just a demo-case how things could be done.

## Install

First install all dependencies:

```
git clone https://github.com/hydrocode-de/skgstat-leaflet.git
cd skgstat-leaflet
pip install -r requirements.txt
```

Then you can run replace the `coords.csv` with you data. **Do not change the heading!**

1. Run ``python main.py`` 
2. open ``index.html`` with your browser

## What does it do?

The ``main.py`` will convert the data in the csv file and run the interpolation. This interpolation is done in kriging.py. 
That's also the place to change kriging parameters. This file will return the result as base64 encoded image strings and a set of
bounding box coordinates. ``main.py`` injects the coordinates, the interpolation image and its bounds into the coords.js file. 
This is ultimately use by ``index.html`` to create the leaflet map.

## Improvements?

1. Make main.py more accessible. 
2. Infer the column names from the csv. 
3. Maybe use argparse to set kriging options. 
4. Append interpolation results to a array to display more than one result
