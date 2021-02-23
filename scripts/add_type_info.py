""" Returns a file with entity types of entities. """
import argparse
import collections
from os.path import join
from pprint import pprint
from tqdm import tqdm

import jsonlines
import ujson as json

print('Loading very large JSON files...')
WIKIDATA_DIR = 'process_wikidata_dump/processed_files'
QID_TO_PIDS = json.load(open(join(WIKIDATA_DIR, 'qid_to_pids.json')))
QID_TO_ALIASES = json.load(open(join(WIKIDATA_DIR, 'qid_to_aliases.json')))


def statistics(output_data):
    """ Prints out top 20 types with counts """
    type_counts = collections.defaultdict(int)

    for data_pt in output_data:
        for answer in data_pt['answer_ner']:
            for answer_dict in data_pt['answer_ner'][answer]:
                for type_dict in answer_dict.get('entity_types', []):
                    type_counts[type_dict['label']] += 1

    type_counts = sorted(type_counts.items(), key=lambda item: item[1], reverse=True)
    pprint(type_counts[:20])


def look_up_entity(qid):
    """ Returns all Wikidata entity types for a QID """
    if qid in QID_TO_PIDS and 'P31' in QID_TO_PIDS[qid]:
        # Get the entity types for the QID as a QID
        entity_types = [d['qid'] for d in QID_TO_PIDS[qid]['P31']]
        # Get the names of the entity type QIDs
        entity_types = [{'qid': t, 'label': QID_TO_ALIASES[t][-1]}
                        for t in entity_types if t in QID_TO_ALIASES]
        return entity_types
    else:
        return []


def add_wikidata_type_information(data):
    print('Adding type information...')
    for data_pt in tqdm(data):
        for answer in data_pt['answer_ner']:
            for answer_dict in data_pt['answer_ner'][answer]:
                if 'id' in answer_dict:
                    answer_dict['entity_types'] = look_up_entity(answer_dict['id'])

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file")
    args = parser.parse_args()

    input_data = [l for l in jsonlines.open(args.input_file)]
    output_data = add_wikidata_type_information(input_data)
    statistics(output_data)

    output_file = args.input_file + '_w_type_info'
    with open(output_file, 'w', encoding='utf-8') as f:
        for l in output_data:
            f.write(json.dumps(l, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
