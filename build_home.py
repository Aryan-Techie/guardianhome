"""GuardianHome: digital twin of an apartment for fall response (Cyberwave catalog assets)."""
import json, math
from dotenv import load_dotenv
load_dotenv("/Users/aryan/Workspace/Hackathons/winwin/mastersunion-cyberwave/.env")
from cyberwave import Cyberwave
from cyberwave.rest.models.environment_create_schema import EnvironmentCreateSchema

cw = Cyberwave()
DESC = ("Real-world problem: falls kill ~684,000 people a year (WHO); older people living alone wait hours for help. "
        "GuardianHome: a real camera + Claude vision detects a fall, the resident's avatar falls in this twin, and a robot team "
        "(TurtleBot3 with phone and medkit, Go2 lighting the way, SO-101 preparing medication) responds. Every robot move is "
        "rehearsed here and passes a safety gate (robots keep >= 0.5 m from the person). Caregiver gets a live alert; no answer "
        "in 20 s escalates. Built with Cyberwave + Supabase + Claude.")
env = cw.environments.create(name="GuardianHome - Fall Response Digital Twin", description=DESC)
EID = env.uuid
print("ENV", EID, env.slug)

def q(yaw=0, pitch=0, roll=0):
    cy, sy = math.cos(math.radians(yaw) / 2), math.sin(math.radians(yaw) / 2)
    cp, sp = math.cos(math.radians(pitch) / 2), math.sin(math.radians(pitch) / 2)
    cr, sr = math.cos(math.radians(roll) / 2), math.sin(math.radians(roll) / 2)
    return dict(rotation_w=cr*cp*cy+sr*sp*sy, rotation_x=sr*cp*cy-cr*sp*sy, rotation_y=cr*sp*cy+sr*cp*sy, rotation_z=cr*cp*sy-sr*sp*cy)

assets = {a: cw.assets.get_by_registry_id(a).uuid for a in [
    "cyberwave/generic_cube", "the-robot-studio/so101", "robotis/turtlebot3-waffle", "unitree/go2",
    "unitree/unitree-g1", "logitech/c275"]}
W = 0.08
SCENE = [  # name, asset, (x, y, z), (yaw, pitch, roll), scale
    ("Floor", "cyberwave/generic_cube", (0, 0, -0.02), (0, 0, 0), (6.2, 4.2, 0.02)),
    ("Wall North", "cyberwave/generic_cube", (0, 2.05, 0), (0, 0, 0), (6.2, W, 1.0)),
    ("Wall South", "cyberwave/generic_cube", (0, -2.05, 0), (0, 0, 0), (6.2, W, 1.0)),
    ("Wall West", "cyberwave/generic_cube", (-3.05, 0, 0), (0, 0, 0), (W, 4.2, 1.0)),
    ("Wall East", "cyberwave/generic_cube", (3.05, 0, 0), (0, 0, 0), (W, 4.2, 1.0)),
    ("Wall Bedroom (south part)", "cyberwave/generic_cube", (0, -0.9, 0), (0, 0, 0), (W, 2.2, 1.0)),
    ("Wall Bedroom (north part)", "cyberwave/generic_cube", (0, 1.75, 0), (0, 0, 0), (W, 0.6, 1.0)),
    ("Bed", "cyberwave/generic_cube", (2.0, 1.2, 0), (0, 0, 0), (1.9, 1.1, 0.45)),
    ("Nightstand", "cyberwave/generic_cube", (0.75, 1.75, 0), (0, 0, 0), (0.4, 0.4, 0.5)),
    ("Sofa", "cyberwave/generic_cube", (-2.0, 1.55, 0), (0, 0, 0), (1.8, 0.7, 0.45)),
    ("Coffee Table", "cyberwave/generic_cube", (-2.0, 0.6, 0), (0, 0, 0), (0.9, 0.5, 0.4)),
    ("Medicine Counter", "cyberwave/generic_cube", (-0.9, -1.7, 0), (0, 0, 0), (1.1, 0.5, 0.9)),
    ("Pill Organizer", "cyberwave/generic_cube", (-0.65, -1.62, 0.9), (0, 0, 0), (0.12, 0.06, 0.04)),
    ("Charging Dock", "cyberwave/generic_cube", (-2.6, -1.6, 0), (0, 0, 0), (0.45, 0.45, 0.03)),
    ("Medication Arm (SO-101)", "the-robot-studio/so101", (-0.95, -1.75, 0.9), (90, 0, 0), None),
    ("Response Rover (TurtleBot3)", "robotis/turtlebot3-waffle", (-2.6, -1.6, 0.03), (0, 0, 0), None),
    ("Escort Quadruped (Go2)", "unitree/go2", (-1.6, -0.2, 0.3), (0, 0, 0), None),
    ("Resident (avatar)", "unitree/unitree-g1", (1.2, -0.7, 0.793), (180, 0, 0), None),
    ("Room Camera", "logitech/c275", (2.9, -1.9, 2.2), (135, 35, 0), None),
]
out = {"environment": EID, "slug": env.slug, "twins": {}}
for name, asset, (x, y, z), (yaw, pitch, roll), sc in SCENE:
    kw = dict(name=name, position_x=x, position_y=y, position_z=z, **q(yaw, pitch, roll))
    if sc:
        kw.update(scale_x=sc[0], scale_y=sc[1], scale_z=sc[2])
    t = cw.twins.create(asset_id=assets[asset], environment_id=EID, **kw)
    out["twins"][name] = t.uuid
    print(f"{name:32s} {t.uuid}")
for wp, (x, y) in {"dock": (-2.6, -1.6), "hall": (-0.6, 1.0), "bedroom_door": (0.4, 1.0), "resident": (1.2, -0.7)}.items():
    try:
        cw.environments.create_waypoint(EID, name=wp, position={"x": x, "y": y, "z": 0})
    except Exception as e:
        print("waypoint", wp, e)
cw.api.src_app_api_environments_update_environment(EID, EnvironmentCreateSchema(
    name="GuardianHome - Fall Response Digital Twin", description=DESC, visibility="public",
    tags=["hackathon", "eldercare", "fall-detection", "supabase", "claude", "turtlebot3", "go2", "so101", "g1"]))
link = cw.api.src_app_api_environments_sharing_create_environment_link(EID)
out["viewer"] = "https://cyberwave.com" + link.share_url
print("VIEWER", out["viewer"])
json.dump(out, open("/Users/aryan/Workspace/Hackathons/winwin/mastersunion-cyberwave/home.json", "w"), indent=1)
