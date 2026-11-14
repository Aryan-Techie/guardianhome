import math, json
from dotenv import load_dotenv
load_dotenv("/Users/aryan/Workspace/Hackathons/winwin/mastersunion-cyberwave/.env")
from cyberwave import Cyberwave
cw = Cyberwave(); EID = "ae980ceb-428a-4b37-898d-ffacd298dc75"
def q(yaw=0):
    return dict(rotation_w=math.cos(math.radians(yaw)/2), rotation_x=0, rotation_y=0, rotation_z=math.sin(math.radians(yaw)/2))
cube = cw.assets.get_by_registry_id("cyberwave/generic_cube").uuid
cam = cw.assets.get_by_registry_id("logitech/c275").uuid
items = [
 ("TV Stand", (-2.0, -1.85, 0), (1.2, 0.3, 0.5), 0),
 ("TV", (-2.0, -1.9, 0.5), (1.0, 0.05, 0.6), 0),
 ("Living Room Rug", (-2.0, 0.9, 0), (2.0, 1.3, 0.01), 0),
 ("Dining Table", (-1.0, -0.6, 0), (0.8, 0.8, 0.75), 0),
 ("Dining Chair 1", (-1.0, -1.15, 0), (0.4, 0.4, 0.45), 0),
 ("Dining Chair 2", (-1.6, -0.6, 0), (0.4, 0.4, 0.45), 0),
 ("Wardrobe", (2.75, -1.25, 0), (0.5, 1.2, 1.0), 0),
 ("Bedside Lamp", (0.75, 1.75, 0.5), (0.12, 0.12, 0.3), 0),
 ("Plant (living room)", (-2.85, -0.7, 0), (0.3, 0.3, 0.8), 0),
 ("Plant (bedroom)", (0.35, -1.85, 0), (0.3, 0.3, 0.7), 0),
 ("Bedroom Rug", (2.0, 0.2, 0), (1.6, 0.8, 0.01), 0),
 ("Door Header", (0, 0.825, 0.92), (0.1, 1.15, 0.08), 0),
]
route = [(-2.6, -1.6), (-0.6, 1.0), (0.4, 1.0), (0.75, -0.25)]
for i, ((x0, y0), (x1, y1)) in enumerate(zip(route, route[1:])):
    L = math.hypot(x1 - x0, y1 - y0); yaw = math.degrees(math.atan2(y1 - y0, x1 - x0))
    items.append((f"Emergency Route Marker {i+1}", ((x0 + x1) / 2, (y0 + y1) / 2, 0), (L, 0.05, 0.006), yaw))
for name, (x, y, z), (sx, sy, sz), yaw in items:
    t = cw.twins.create(asset_id=cube, environment_id=EID, name=name, position_x=x, position_y=y, position_z=z, scale_x=sx, scale_y=sy, scale_z=sz, **q(yaw))
    print(name, t.uuid)
t = cw.twins.create(asset_id=cam, environment_id=EID, name="Living Room Camera", position_x=-2.9, position_y=1.9, position_z=2.2, **q(-45))
print("cam", t.uuid)
