#!/usr/bin/env python

# Copyright (c) 2018 Intel Labs.
# authors: German Ros (german.ros@intel.com)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example of automatic vehicle control from client side."""

from __future__ import print_function

import argparse
import collections
import datetime
import glob
import logging
import math
import os
import random
import re
import sys
import weakref
import matplotlib.pyplot as plt

import time



def distanceBetweenCoords(lat1, lon1, lat2, lon2):
    rad=math.pi/180
    dlat=lat2-lat1
    dlon=lon2-lon1
    R=6372.795477598
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia=2*R*math.asin(math.sqrt(a))
    return distancia *1000

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_q
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError(
        'cannot import numpy, make sure numpy package is installed')

# ==============================================================================
# -- Find CARLA module ---------------------------------------------------------
# ==============================================================================
try:
    sys.path.append(glob.glob('/home/salabeta/carlasimulator/CARLA_0.9.11-dirty/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- Add PythonAPI for release mode --------------------------------------------
# ==============================================================================
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass

import carla
from carla import ColorConverter as cc



try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    map = world.get_map()

    generados = map.generate_waypoints(15)

    outputfileXY = open("outFile_waypointsXY.txt", "w")
    outputfileLatLon = open("outFile_waypointsLatLon.txt", "w")
    
    x = []
    y = []
    filtrados=[]
    beforeCoord = [0, 0]
    for i in generados:
        latitud = i.transform.location
        latitud = map.transform_to_geolocation(carla.Location(x=latitud.x, y=latitud.y, z=0))
        #if str(i.right_lane_marking.type)=="Broken" and str(i.left_lane_marking.type)=="Broken":
        # if str(f.right_lane_marking.type) == "NONE" and str(f.left_lane_marking.type) == "NONE":
        #if (i.is_junction and i.left_lane_marking.type != "NONE") or (str(i.right_lane_marking.type) == "Broken" and str(i.left_lane_marking.type) == "Broken"):
        if i.is_junction and (str(i.right_lane_marking.type) != "NONE" and str(i.left_lane_marking.type) != "NONE") :
            if latitud.longitude < -6.338950801925578 and latitud.longitude > -6.344916034757305 and latitud.latitude < 39.48059130922252 and latitud.latitude > 39.47907173926249:
                if distanceBetweenCoords(beforeCoord[0], beforeCoord[1], latitud.latitude, latitud.longitude) > 10 :
                    #print("Lat: " + str(latitud.latitude) + " Lon: " + str(latitud.longitude))
                    #print("X: " + str(i.transform.location.x) + " Y: " + str(i.transform.location.y))
                    x.append(i.transform.location.x)
                    y.append(i.transform.location.y)
                    filtrados.append(i)
                    outputfileXY.write(str(i.transform.location.x) + "#" + str(i.transform.location.y) + "\n")
                    outputfileLatLon.write(str(latitud.latitude) + "#" + str(latitud.longitude) + "\n")
                    #print(i.left_lane_marking.type)
                    #print(i.right_lane_marking.type)
                    beforeCoord = [latitud.latitude, latitud.longitude]
    outputfileXY.close()
    outputfileLatLon.close

    #plt.plot(x, y, 'ro')
    #plt.show()


    for index in range(len(x)):
        pass #print("point: [",x[index],",",y[index], "]\n")
    
    # world = client.get_world()
    current_map = world.get_map()
    actors = world.get_actors()

    for actor in actors:
        if 'vehicle.carro' in actor.type_id:
            vehicle = actor
            break

    print(vehicle.get_location())

    vehicle.set_autopilot(True)
    #time.sleep(100)
    #vehicle.apply_control(carla.VehicleControl(throttle=-0, steer=0))

    #blueprint_library = world.get_blueprint_library()
    #vehicle_bp = random.choice(blueprint_library.filter('vehicle.*'))


    #print("Vehicle init pos: " , vehicle.get_location())


 


finally:
    
    print('destroying actors')
    print('done.')

