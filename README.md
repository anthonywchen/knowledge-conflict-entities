# Finding Entities for Knowledge Conflicts


### Setting up environment
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

Then follow the README instructions in `process_wikidata_dump/`.

### Scripts

* `add_type_info.py`: Adds type information to the answers from the MRQA NQ datasets.
    * `--input_file`: The MRQA file you want to add Wikdata type info to.
    
    The output file is `<input_file>_w_type_info`.
    
    
* `get_entities_by_type.py`: Returns a list of entities for specified entity types.
    * `--entity_types`: A list of entity types specified by QIDs 
    * `-n` : The number of entities to find per entity type
    
    Example run which returns 500 entities of type human and type TV show:
    
    `python get_entities_by_type.py --entity_types Q5 Q5398426 -n 500`
    
    The output file for this example would be `Q5_Q5398426_500_entities.json`.
    
   
