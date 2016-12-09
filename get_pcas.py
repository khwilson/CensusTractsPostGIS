import pandas as pd
import click
import os
from sqlalchemy import create_engine
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

WIDTH = 100

def random_points(multi_poly, num_points):
     points = []
     probs = np.array([p.area for p in multi_poly]) / sum(p.area for p in multi_poly)
     while len(points) < num_points:
         choice = np.random.choice(len(multi_poly), p=probs)
         poly = multi_poly[choice]
         minx, miny, maxx, maxy = poly.bounds
         while True:
             x = np.random.random() * (maxx - minx) + minx
             y = np.random.random() * (maxy - miny) + miny
             point = Point(x, y)
             if poly.contains(point):
                 points.append(point)
                 break
     return np.array([[point.x, point.y] for point in points])

def get_pg():
    return {key: os.environ['PG' + key.upper()] for key in ['database', 'host', 'user', 'password']}

def push_data(count, means, evecs, engine):
    click.echo("Pushing data....")
    tdf = pd.DataFrame({'ogc_fid': list(range(count-len(means)+1, count+1)),
                        'mean_x': [mean[0] for mean in means],
                        'mean_y': [mean[1] for mean in means],
                        'sigma_xx': [evec[0, 0] for evec in evecs],
                        'sigma_xy': [evec[0, 1] for evec in evecs],
                        'sigma_yx': [evec[1, 0] for evec in evecs],
                        'sigma_yy': [evec[1, 1] for evec in evecs]})
    tdf.to_sql('census_tracts_pca', engine, if_exists='append')

def main():
    engine = create_engine('postgresql://', connect_args=get_pg())
    conn = engine.raw_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM census_tracts")
        total_len = cur.fetchall()[0][0]
    click.echo("Found {} records".format(total_len))
    with click.progressbar(range(total_len), length=total_len) as pbar:
        means = []
        evecs = []
        for count in pbar:
            if count % WIDTH == 0:
                click.echo("Finished up to {}".format(count))
                if means:
                    push_data(count, means, evecs, engine)
                click.echo("Pulling data")
                df = gpd.GeoDataFrame.from_postgis('SELECT ogc_fid, wkb_geometry FROM census_tracts WHERE ogc_fid > %s AND ogc_fid <= %s', conn, geom_col='wkb_geometry', params=[count, count+WIDTH])
                click.echo("Pulled {} records".format(len(df)))
            multi_poly = df.wkb_geometry[count % WIDTH]
            points = random_points(multi_poly, 1000)
            mean = np.mean(points, axis=0)
            centered = points - mean[np.newaxis, :]
            transp = np.dot(centered.T, centered) / (centered.shape[0] - 1)
            evals, evec = np.linalg.eig(transp)
            evec *= np.sqrt(evals)[np.newaxis, :]
            means.append(mean)
            evecs.append(evec)
        push_data(count, means, evecs, engine)


if __name__ == '__main__':
    main()
