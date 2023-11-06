exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

def makePoints(width, height):
    width_2 = width*0.5
    height_2 = height*0.5
    return [ npa([-width_2, -height_2]),
             npa([-width_2,  height_2]),
             npa([ width_2,  height_2]),
             npa([ width_2, -height_2]) ]

pos = ib.unprojectPoints(makePoints(800, 600), centerRelative=True, depth=5.0)
bx = mkshapes.makeBox(np.linalg.norm(pos[1] - pos[2]), np.linalg.norm(pos[0] - pos[1]), 0.01, texture='image_filename.png')
cds, fov = ib.getCameraCoords()
cds.translate(coordinates.Z*5.0)
bx.newcoords(cds)
