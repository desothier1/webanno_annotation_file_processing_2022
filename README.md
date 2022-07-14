# webanno_annotation_file_processing_2022

## processing of input json file to separate text files for webanno input

1. Root folder json_file_for_webanno:
  - subfolder sentence-splitter cloned from https://github.com/mediacloud/sentence-splitter
  - sample.json : input example file
  - zipped example output in output_files_for_webanno_annot.zip
  - script and syntax to convert sample.json file to separate webanno input files:
    - python extractfromjson.py
  
## processing of exported .json files to readable .json files
folder process_json with subfolders:

1. Root folder process_json
   - script *main.py* 
     - with syntax: *python main.py*
       - reads input folders *extracted_annotations*, generates output folders with content *extracted_annotations_out_example*
       - reads scripts in subfolder reformat to reformat input files to more readable json format.
   - OVERVIEW_examp.txt
     - overview of processed data
   - extracted_annotations_all.zip
     - 250 json files. These can be copied to folder *extracted_annotations* to use as input data.

2. Folder reformat   
   - scripts  *util.py*, *json2readable.py* that are called by *main.py* in root folder

3. Folder extracted_annotations : 
   - 10 example exported annotated .json files 
   - as input files to be processed for generating more readable format
   
4. Folder extracted_annotations_out_example :
   - 10 example output files in readable format
