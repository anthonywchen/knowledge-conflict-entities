# Processing Wikidata Dump

To process the dump, run the following:

1. Download and process the raw dump. This takes a while (maybe a full day? I don't quite remember.)

    `./download_and_process.sh`
   
2. Take those processed files and extract out useful info:
   ```
   python build_qid_popularity_dictionary.py
   python maps_pids_to_labels.py
   python maps_qids_to_aliases.py
   python map_qids_to_pids.py
   ```

    
    
The final files will be in `process_wikidata_dump/processed_files`.