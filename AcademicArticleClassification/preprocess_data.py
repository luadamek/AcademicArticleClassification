import json
import pandas as pd
import numpy as np

def count_lines(json_filename):
    count = 0
    with open(json_filename, 'r') as input_file:
        for line in input_file: count += 1
    return count

def get_keys(json_filename):
     with open(json_filename, 'r') as input_file:
         for line in input_file:
             return json.loads(line).keys()


# a map of all the document codes for things uploaded into arxix
subclass_map = {
    "Physics":["astro-ph","cond-mat","gr-qc","hep-ex","hep-lat",\
              "hep-ph","hep-th","math-ph","nlin","nucl-ex","nucl-th",\
              "physics","quant-ph"],\
    "Mathematics":["math"],\
    "Computer Science":["cs", "CoRR"],\
    "Quantitative Biology":["q-bio"],\
    "Quantitative Finance":["q-fin"],\
    "Statistics":["stat"],\
    "Electrical Engineering and Systems Science":["eess"],\
    "Economics":["econ"],\
}

inverted_subclass_map = {}
for key in subclass_map:
    for el in subclass_map[key]:
        inverted_subclass_map[el] = key

classes = list(subclass_map.keys())
all_subclasses = set()
for c in classes:
    for subclass in subclass_map[c]:
        assert subclass not in all_subclasses
        all_subclasses.add(subclass)

def get_categories(cat_string):
    subclasses = cat_string.split(" ")
    subclasses = [el.split(".") for el in subclasses]
    subclasses = [el[0] for el in subclasses if len(el) > 1]
    return subclasses

def all_categories_nentries(json_filename):
    categories = set()
    count = 0

    with open(json_filename, 'r') as input_file:
        for line in input_file:
            loaded = json.loads(line)
            string = loaded["categories"]
            these_subclasses =  get_categories(string)
            these_subclasses = {c for c in these_subclasses if c in all_subclasses}
            if these_subclasses: count += 1
            categories.update(these_subclasses)

    return categories, count

if __name__ == '__main__':
    categories, count = all_categories_nentries('/project/def-psavard/ladamek/ArxivFiles/arxiv-metadata-oai-snapshot.json')

    encoding_indices = {}
    for i, c in enumerate(classes):
        encoding_indices[c] = i
    encoding_vector = np.zeros((count,len(classes)), dtype=np.uint8)
    abstracts = []

    json_filename = '/project/def-psavard/ladamek/ArxivFiles/arxiv-metadata-oai-snapshot.json'
    count = 0
    with open(json_filename, 'r') as input_file:
        for line in input_file:
            loaded = json.loads(line)
            string = loaded["categories"]
            these_subclasses =  get_categories(string)
            these_subclasses = {c for c in these_subclasses if c in all_subclasses}
            if not these_subclasses: continue
            for subclass in these_subclasses:
                encoding_vector[count,encoding_indices[inverted_subclass_map[subclass]]] = 1
            abstracts.append(loaded["abstract"])
            count += 1

    #okay load the encoding vectors into a pandas dataframe
    data = {"abstracts": abstracts}
    for c in classes:
        data[c] = encoding_vector[:, encoding_indices[c]]
    frame = pd.DataFrame.from_dict(data)
    frame.to_hdf("/project/def-psavard/ladamek/ArxivFiles/arxiv-metadata-oai-snapshot.hdf", "abstract_data")






