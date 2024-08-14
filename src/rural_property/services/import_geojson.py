import json

from django.contrib.gis.geos import GEOSGeometry

from rural_property.models import RuralProperty, Tract, Field

geojson_file = '/home/zeldris/Área de trabalho/projects/arapuca/teste.geojson'

with open(geojson_file) as f:
    geojson_data = json.load(f)

for feature in geojson_data['features']:
    properties = feature['properties']
    geometry = GEOSGeometry(json.dumps(feature['geometry']))

    rural_property, _ = RuralProperty.objects.get_or_create(code=properties['property'], defaults=dict(name=properties['p_name']))
    tract, _ = Tract.objects.get_or_create(code=str(properties['tract']), rural_property=rural_property)
    field, _ = Field.objects.get_or_create(code=str(properties['field']), tract=tract, defaults=dict(geometry=geometry))

