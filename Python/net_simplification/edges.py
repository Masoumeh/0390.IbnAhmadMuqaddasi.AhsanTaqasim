import geojson, csv


with open("../../Data/new_simplified_muq_coords_post_lines.geojson", 'r') as file:
    f = geojson.load(file)
    with open("../../Data/new_simplified_muq_coords_post_edges.csv", 'w') as edgeFile:
        writer = csv.writer(edgeFile, delimiter='\t')
        for l in f['features']:
            writer.writerow([l['properties']['start'], l['geometry']['coordinates'][0],
                             l['properties']['end'], l['geometry']['coordinates'][-1]])

