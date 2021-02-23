""" Given entity types, return associated entities sorted by popularity """
import argparse
import collections
from os.path import join
from tqdm import tqdm

import ujson as json

print('Loading very large JSON files...')
WIKIDATA_DIR = 'process_wikidata_dump/processed_files'
QID_TO_PIDS = json.load(open(join(WIKIDATA_DIR, 'qid_to_pids.json')))
QID_TO_ALIASES = json.load(open(join(WIKIDATA_DIR, 'qid_to_aliases.json')))
QID_TO_POPS = json.load(open(join(WIKIDATA_DIR, 'qid_popularities.json')))

def get_entities_by_type(entity_types, n):
    print('Getting entities for specified types...')
    entities_by_type = collections.defaultdict(dict)

    for ent_type in entity_types:
        # Iterate through all entities
        for qid in QID_TO_ALIASES:
            if len(entities_by_type[ent_type]) >= n:
                break

            qid_types = [d['qid'] for d in
                         QID_TO_PIDS.get(qid, {}).get('P31', [])]

            if ent_type in qid_types:
                if qid in QID_TO_ALIASES and qid in QID_TO_POPS:
                    entities_by_type[ent_type][qid] = {
                        'aliases': QID_TO_ALIASES[qid],
                        'pop': int(10**QID_TO_POPS[qid])
                    }

        # Sort entities for current `ent_type` by popularity
        entities_by_type[ent_type] = sorted(entities_by_type[ent_type].items(),
                                            key=lambda k_v: k_v[1]['pop'], reverse=True)

    return entities_by_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entity_types", nargs='+', default=['Q5'],
                        help='Entity types represented by QIDs.')
    parser.add_argument("-n", type=int, default=5000,
                        help='Number of entities to return per type')
    args = parser.parse_args()

    entities_by_type = get_entities_by_type(args.entity_types, args.n)

    # Writes out a file like `Q5_1000_entities.json`
    entity_types = '_'.join(sorted(args.entity_types))
    output_file = f'{entity_types}_{args.n}_entities.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(entities_by_type, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()