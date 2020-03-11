import pandas as pd
import json
import subprocess

from kriging import process

def csv2json(fname):
    """
    Be careful as the function expects a standard comma separated csv
    with column names lat,lon and carb
    """
    df = pd.read_csv(fname)
    return [dict(lat=row.lat, lon=row.lon, value=row.carb) for row in df.itertuples()]


def save_json_data(obj):
    """
    This function will transform the data from coords.csv into a coords.js file 
    that is consumed by the index.html

    If you change the structure of the file, you'll have to reflect that in the
    js of index.html as well
    """
    with open('coords.js', 'w') as jsfile:
        code = 'var data = %s;' % json.dumps(obj)
        jsfile.write(code)



def interpolate():
    """
    runs the kriging.py

    Make all changes due to kriging into the kriging.py file
    """
    data, bounds = process()

    with open('coords.js', 'r') as js:
        code = js.read()
    with open('coords.js', 'w') as js:
        code = "%s\nvar img = '%s';\nvar bnd = %s;" % (code, data, json.dumps(bounds))
        js.write(code)



if __name__ == "__main__":
    print('Converting coordinate data')
    coords = csv2json('coords.csv')
    save_json_data(coords)
    
    print('done. Start kriging...')
    interpolate()
    print('done')
