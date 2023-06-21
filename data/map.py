from model.map import Map
from typing import Iterator, Tuple
from model.coordinate import Coordinate
from model.edge import Edge
import data.page as page_data
from selenium.common.exceptions import NoSuchElementException

CE_MAP = Map()

CE_MAP.insert_system_connections('Kelsey', [('Ethan', 5), ('Franklyn', 5), ('Antioch', 5), ('Lorat', 7), ('Grantham', 5)])
CE_MAP.insert_system_connections('Ethan', [('Kelsey', 5), ('Feris', 5)])
CE_MAP.insert_system_connections('Feris', [('Ethan', 5), ('Farpoint 1', 2)])
CE_MAP.insert_system_connections('Farpoint 1', [('Feris', 2), ('Farpoint 2', 2)])
CE_MAP.insert_system_connections('Farpoint 2', [('Farpoint 1', 2)])
CE_MAP.insert_system_connections('Franklyn', [('Kelsey', 5)])
CE_MAP.insert_system_connections('Antioch', [('Kelsey', 5), ('Hexham', 7)])
CE_MAP.insert_system_connections('Hexham', [('Antioch', 7)])
CE_MAP.insert_system_connections('Lorat', [('Kelsey', 7), ('Drakos', 5)])
CE_MAP.insert_system_connections('Drakos', [('Lorat', 5), ('Fieron', 3)])
CE_MAP.insert_system_connections('Fieron', [('Drakos', 3), ('Descarte', 7)])
CE_MAP.insert_system_connections('Grantham', [('Kelsey', 5), ('Palham', 5)])
CE_MAP.insert_system_connections('Palham', [('Grantham', 5), ('Descarte', 4)])
CE_MAP.insert_system_connections('Descarte', [('Palham', 4), ('Fieron', 7), ('Bedlam', 5)])
CE_MAP.insert_system_connections('Bedlam', [('Descarte', 5)])

CE_MAP.insert_system_planet('Kelsey', 'Cinq Port')
CE_MAP.insert_system_planet('Feris', 'New Orion')
CE_MAP.insert_system_planet('Feris', 'Starbase-51')
CE_MAP.insert_system_planet('Franklyn', 'Port Ross')
CE_MAP.insert_system_planet('Antioch', 'Graninis')
CE_MAP.insert_system_planet('Lorat', 'Wimbourne')
CE_MAP.insert_system_planet('Fieron', 'Welling')
CE_MAP.insert_system_planet('Palham', 'Wolsley')
CE_MAP.insert_system_planet('Descarte', 'San Ferran')
CE_MAP.insert_system_planet('Descarte', 'San Miguel')
CE_MAP.insert_system_planet('Descarte', 'Daphine')

CE_MAP.insert_planet_port('Kelsey', 'Cinq Port', 'Cinq Port', 50)
CE_MAP.insert_planet_port('Feris', 'New Orion', 'IQ Academy', 50)
CE_MAP.insert_planet_port('Feris', 'Starbase-51', 'Starbase-51', 50)
CE_MAP.insert_planet_port('Franklyn', 'Port Ross', 'Port Ross', 50)
CE_MAP.insert_planet_port('Antioch', 'Graninis', 'Graninis', 50)
CE_MAP.insert_planet_port('Lorat', 'Wimbourne', 'Unimatrix 001', 37)
CE_MAP.insert_planet_port('Fieron', 'Welling', 'Welling', 50)
CE_MAP.insert_planet_port('Palham', 'Wolsley', 'Mysfits', 10)
CE_MAP.insert_planet_port('Descarte', 'San Ferran', 'San Ferran', 50)
CE_MAP.insert_planet_port('Descarte', 'San Miguel', 'San Miguel', 50)
CE_MAP.insert_planet_port('Descarte', 'Daphine', 'Shipwreck Island', 50)

CE_MAP.insert_port_building('Kelsey', 'Cinq Port', 'Cinq Port', 'Ashar Corporation')
CE_MAP.insert_port_building('Feris', 'New Orion', 'IQ Academy', 'Ashar Corporation')
CE_MAP.insert_port_building('Feris', 'Starbase-51', 'Starbase-51', 'Ashar Corporation')
CE_MAP.insert_port_building('Franklyn', 'Port Ross', 'Port Ross', 'Ashar Corporation')
CE_MAP.insert_port_building('Antioch', 'Graninis', 'Graninis', 'Ashar Corporation')
CE_MAP.insert_port_building('Lorat', 'Wimbourne', 'Unimatrix 001', 'Ashar Corporation')
CE_MAP.insert_port_building('Fieron', 'Welling', 'Welling', 'Ashar Corporation')
CE_MAP.insert_port_building('Palham', 'Wolsley', 'Mysfits', 'Ashar Corporation')
CE_MAP.insert_port_building('Descarte', 'San Ferran', 'San Ferran', 'Ashar Corporation')
CE_MAP.insert_port_building('Descarte', 'San Miguel', 'San Miguel', 'Ashar Corporation')
CE_MAP.insert_port_building('Descarte', 'Daphine', 'Shipwreck Island', 'Ashar Corporation')

CENTER_TABLES = "/html/body/div/div[@align='center']/table/tbody"
CENTER_ROWS = "/html/body/div/div[@align='center']/table/tbody/tr"


def get_edges(start: Coordinate) -> Iterator[Tuple[Coordinate, Edge]]:
    return CE_MAP.get_edges(start)

def execute_edge(next: Coordinate, edge: Edge):
    if edge.action == Edge.INTER_SYSTEM:
        page_data.press_button(f"{CENTER_ROWS}[child::td[2][normalize-space()='{next.system}']]//input[@value='Jump']")
    elif edge.action == Edge.INTER_PLANET:
        page_data.press_button(f"{CENTER_ROWS}//input[@alt='{next.planet}']")
    elif edge.action == Edge.DOCK_PORT:
        page_data.press_button(f"{CENTER_ROWS}//a[@href='dock.php']")
        try:
            page_data.press_button(f"{CENTER_ROWS}[child::td[1][normalize-space()='{next.port}']]//input[@value='Dock Here']")
        except NoSuchElementException:
            page_data.press_button(f"{CENTER_ROWS}//input[@value='Dock Now']")
    elif edge.action == Edge.UNDOCK_PORT:
        page_data.press_button(f"{CENTER_ROWS}//input[contains(@value,'Undock')]")
    elif edge.action == Edge.ENTER_BUILDING:
        page_data.press_button(f"{CENTER_ROWS}[child::td[1][normalize-space()='{next.building}']]//input[@value='View']")
        page_data.press_button(f"/html/body//input[contains(@value, 'Enter')]")
    elif edge.action == Edge.EXIT_BUILDING:
        page_data.press_button(f"{CENTER_ROWS}//a[@href='index.php']")
