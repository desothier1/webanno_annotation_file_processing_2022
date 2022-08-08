# webanno annotation file processing 2022 : annotation of events, sentiment, topics

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
   
## file processing annotation of IPTC topic classes and evaluation of topic prediction
folder IPTC_topic_classification

1. prepare annotation template from input file sample.json
  - run extractfromjson_compl_doc.py
    - with syntax : python extractfromjson_compl_doc.py
     - input file sample.json is read, and output file _ALLFILES_TITLE_LEAD_CONTENT.txt can be saved as excel file IPTC_annotations.xlsx 
2. 17 topic classes (level 1) as specified in https://www.iptc.org/std/NewsCodes/treeview/mediatopic/mediatopic-en-GB.html
are annotated for file IPTC_annotations.xlsx
  - For each of the 250 documents in the file, the relevant topic labels are ranked according to priority, by assigning those a number 1-17.
    - The resulting annotated file is IPTC_annotations_annotated.xlsx
3. Evaluation of IPTC topic classification performances (calculation of Precision - Recall - F score), comparing the annotated reference data and predictions
  - subfolder : calcul_F1
  - IPTC_ref_hyp_format.py converts (reference data) REFDATA.txt (exported .txt file from IPTC_annotations_annotated.xlsx)  and (predictions) sample.json respectively to REF_out.txt and HYP_out.txt
  - calcul_prom.py reads REF_out.txt and HYP_out.txt and generates Precison, Recall and F scores.
  
