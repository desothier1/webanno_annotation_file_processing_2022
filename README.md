# webanno_annotation_file_processing_2022

## processing of input json file to separate text files for webanno input

1. Root folder json_file_for_webanno:
  - subfolder sentence-splitter cloned from https://github.com/mediacloud/sentence-splitter
  - sample.json : input example file
  - zipped example output in output_files_for_webanno_annot.zip
  - script and syntax to convert sample.json file to separate webanno input files:
    - python extractfromjson.py
## Project annotation

LT3 webanno project code : EventDNA_2.0_event_sentiment_960SENT

Annotation of event spans, and labeling event prominence and sentiment labels, as specified in attached guidelines.
1. Prominence event labels
  - Main : reason why author wrote article
  - Background : more info about Main event.
  - None : raw sentence without event

2. Sentiment labels;;
  - Positive
  - Negative
  - Neutral

![bisexamp1](https://user-images.githubusercontent.com/50878643/179030034-9fc4adbe-095d-4fa0-909e-c8c3eff9b857.png)

[08042022_gettingstarted_webanno_TD.pdf](https://github.com/desothier1/webanno_annotation_file_processing_2022/files/9113576/08042022_gettingstarted_webanno_TD.pdf)

[eventdna_guidelines_v2_0.pdf](https://github.com/desothier1/webanno_annotation_file_processing_2022/files/9113466/eventdna_guidelines_v2_0.pdf)
    
## unzip and extract annotated files from webanno project   
1. unzip folder contents:
  - after annotation of the project, export the project, which results in a zipped folder with the annotations.
  - zipped webanno annotation project *EventDNA_2_project_2022-05-16_1150.zip*
  - script *unzipper.py*
    - syntax *python unzipper.py*
      - specify in script absolute path of 'annotation' folder from input zipped file (folder_root=)
      - specify in script absolute path of output folder (folder_root_min=) and outputfolder name (directory= )
      
   
  
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
