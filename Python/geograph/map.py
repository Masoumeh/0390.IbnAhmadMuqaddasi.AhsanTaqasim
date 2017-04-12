import math


def get_destination_latlng(lat, lng, azimuth, distance):
    """returns the lat and long of the destination point
    given the start lat, long, azimuth, and distance"""
    r = 6378.1  # Radius of the Earth in km
    bering = math.radians(azimuth)  # Bearing is degrees converted to radians.
    d = float(distance) / 1000  # Distance m converted to km
    lat1 = math.radians(lat)  # Current dd lat point converted to radians
    lon1 = math.radians(lng)  # Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d / r) + math.cos(lat1) * math.sin(d / r) * math.cos(bering))
    lon2 = lon1 + math.atan2(math.sin(bering) * math.sin(d / r) * math.cos(lat1),
                             math.cos(d / r) - math.sin(lat1) * math.sin(lat2))
    # convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2, lon2


def get_path_length(lat1, lng1, lat2, lng2):
    """calculates the distance between two lat, long coordinate pairs"""
    r = 6371000  # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    delta_lat = math.radians((lat2 - lat1))
    delta_lng = math.radians((lng2 - lng1))
    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(
        delta_lng / 2) * math.sin(delta_lng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c
    return d


def calculate_bearing(lat1, lng1, lat2, lng2):
    """calculates the azimuth in degrees from start point to end point"""
    start_lat = math.radians(lat1)
    start_lng = math.radians(lng1)
    end_lat = math.radians(lat2)
    end_lng = math.radians(lng2)
    d_lng = end_lng - start_lng
    d_phi = math.log(math.tan(end_lat / 2.0 + math.pi / 4.0) / math.tan(start_lat / 2.0 + math.pi / 4.0))
    if abs(d_lng) > math.pi:
        if d_lng > 0.0:
            d_lng = -(2.0 * math.pi - d_lng)
        else:
            d_lng = (2.0 * math.pi + d_lng)
    bearing = (math.degrees(math.atan2(d_lng, d_phi)) + 360.0) % 360.0
    return bearing


def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.

    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])
    diff_long = math.radians(pointB[1] - pointA[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    # return initial_bearing
    return compass_bearing


def find_intermediate_coord(interval, azimuth, lat1, lng1):
    """returns a coordinate pair between two coordinate
    pairs given the desired interval"""

    # azimuth = calculate_initial_compass_bearing((lat1, lng1), (lat2, lng2))
    return get_destination_latlng(lat1, lng1, azimuth, float(interval))
