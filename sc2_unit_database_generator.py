from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pprint
import time
import csv
import functools 

PROTOSS_UNITS = [
  "Probe",
  "Zealot",
  "Stalker",
  "Sentry",
  "Adept",
  "High_Templar",
  "Dark_Templar",
  "Immortal",
  "Colossus",
  "Disruptor",
  "Archon",
  "Observer",
  "Warp_Prism",
  "Phoenix",
  "Void_Ray",
  "Oracle",
  "Carrier",
  "Tempest",
  "Mothership_Core",
  "Mothership"
]

TERRAN_UNITS = [
  "SCV",
  "MULE",
  "Marine",
  "Marauder",
  "Reaper",
  "Ghost",
  "Hellion",
  "Hellbat",
  "Siege_Tank",
  "Cyclone",
  "Widow_Mine",
  "Thor",
  "Auto-Turret",
  "Viking",
  "Medivac",
  "Liberator",
  "Raven",
  "Banshee",
  "Battlecruiser",
]

ZERG_UNITS = [
  "Larva",
  "Cocoon",
  "Drone",
  "Queen",
  "Zergling",
  "Cocoon",
  "Baneling",
  "Roach",
  "Cocoon",
  "Ravager",
  "Hydralisk",
  "Cocoon",
  "Lurker",
  "Infestor",
  "Swarm_Host",
  "Ultralisk",
  "Locust",
  "Broodling",
  "Changeling",
  "Infested_Terran",
  "Overlord",
  "Overseer",
  "Mutalisk",
  "Corruptor",
  "Brood_Lord",
  "Viper",
]

def raw_unit_data(unit_name):
  print('.')

  quote_page = f"https://liquipedia.net/starcraft2/{unit_name}"
  req = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0'})
  page = urlopen(req).read()
  soup = BeautifulSoup(page, 'html.parser')

  raw_data = list(map(lambda x: x.get_text(), soup.findAll("div", {"class": "infobox-cell-2"})))

  keys = raw_data[::2]
  values = raw_data[1::2]

  data = dict(zip(keys, values))
  data["Unit"] = unit_name

  return data

with open(f'sc2_unit_data.csv', 'w', newline='\n') as csvfile:
    unit_data = list(map(
      lambda unit: raw_unit_data(unit),
      PROTOSS_UNITS + TERRAN_UNITS + ZERG_UNITS
    ))

    unit_keys = list(map(
      lambda unit: list(unit.keys()),
      unit_data
    ))

    field_names = list(set([item for sublist in unit_keys for item in sublist]))

    writer = csv.DictWriter(csvfile, fieldnames=field_names)

    writer.writeheader()

    for unit in unit_data:
      writer.writerow(unit)