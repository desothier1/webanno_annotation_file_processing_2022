"""Transforming Webanno output formats to the readable Data Format (readab).
"""

import json
from collections import defaultdict
from pathlib import Path
from pprint import pprint

from loguru import logger

from reformat import util
import re

#MOSTFREQSENT = open('MOST_FREQ_SENT.txt','w')

def make_freq_dict(my_list,filename):
   
   freqsent = {}
   valueslist=[]
   valueslisttup=[]
   maxval=0
   for item in my_list:
     if (item in freqsent):
         freqsent[item] += 1
     else:
         freqsent[item] = 1
   for key, value in freqsent.items():
           valueslist.append(value)
           valueslisttup.append((value,key))
   if len(valueslist) > 0:
     maxval=(max(valueslist))
     for val,key in valueslisttup:
      if maxval==val:
         print(key)
         MOSTFREQSENT.write("%s\t%s\n"%(key,filename)) 
   else:
         MOSTFREQSENT.write("EMPTY\t%s\n"%(filename)) 
   #print(valueslisttup)
   #m = max(valueslist)
   #maxelementslist =   [j for i, j in enumerate(valueslist) if j == m]           
   #print(maxelementslist)



def format_over_corpus(corpus_json_dirp, out_dirp, test=False):
    """Expects an input dir of json files. For each json, writes a corresponding readable file to `our_dirp`.
    If `test` is true, only a small number of files will be processed.
    """
    source_jsons = list(corpus_json_dirp.iterdir())
    print(source_jsons)
    #assert len(source_jsons) == 1745
    ##print(len(source_jsons))
    #assert len(source_jsons) == 1
    assert all(f.suffix == ".json" for f in source_jsons)
    if test == True:
        source_jsons = source_jsons[:100]
    OVERVIEWFILE = open('OVERVIEW.txt','w')
    for source_f in source_jsons:
            sentiment_list=[]
        # logger.info("Processing file {}...", source_f.stem)
            #print(source_f)
        #try:
            with open(source_f, "r") as json_fo:
                readab = json2readab(json_fo, source_f.stem)
            outfile = (out_dirp / source_f.stem).with_suffix(".json")
            #EVENTS
            #for item in readab['doc']['annotations']['events']:
            newdict = {}
            newdict = readab['doc']['annotations']['events']
            for k,v in newdict.items():
                #event number
                #event_3
                #print(v)
                value_dict = {}
                value_dict = v
                #{'annotation_type': 'event', 'string': 'Op zondag start het spektakel al om 18 uur', 'features': {'span': [51, 52, 53, 54, 55, 56, 57, 58, 59], 'prominence': 'Background', 'EventPolarity': 'EVE positive'}, 'home_sentence': 'sentence_4'}
                minilist=[]
                minilist.append(source_f.stem)
                minilist.append(k)
                #print(k)
                #print(value_dict)
                for a,b in value_dict.items():
                   #print(a,b)
                   #    a_dictionary = {"a": 1, "b": 2, "c":3}
                   keys_list = list(value_dict)
                   #key0 = keys_list[0]
                   #print(key0)
                key1 = keys_list[1]
                #print(value_dict[key1])
                key2 = keys_list[2]
                #print(value_dict[key2])
                key3 = keys_list[3]
                #print(value_dict[key3])
                feature_dict={}
                feature_dict = value_dict[key2]
                
                for c,d in feature_dict.items():
                  if not c.startswith('span'):
                   minilist.append(d) 
                   #print("%s\t%s\t%s"%(k,c,d)) 
                   
                minilist.append(value_dict[key3])
                minilist.append(value_dict[key1])
                #print(minilist[3])
                #append sentiment to list, to generate sentim. freq. dict
                sentiment_list.append(minilist[3])

                newstring =  '\t'. join(minilist)
                OVERVIEWFILE.write("%s\n"%(newstring))


            #make_freq_dict(sentiment_list,source_f)
            #make_freq_dict(original_labels)

            #NONE-EVENTS
            nonenewdict = {}
            nonenewdict = readab['doc']['annotations']['none_events']
            for k,v in nonenewdict.items():
                #event number
                #event_3
                #print(k)
                value_dict = {}
                value_dict = v
                #{'annotation_type': 'event', 'string': 'Op zondag start het spektakel al om 18 uur', 'features': {'span': [51, 52, 53, 54, 55, 56, 57, 58, 59], 'prominence': 'Background', 'EventPolarity': 'EVE positive'}, 'home_sentence': 'sentence_4'}
                noneminilist=[]
                noneminilist.append(source_f.stem)
                noneminilist.append(k)
                #print(noneminilist)

                for a,b in value_dict.items():
                   #print(a,b)
                   #    a_dictionary = {"a": 1, "b": 2, "c":3}
                   keys_list = list(value_dict)
                   #key0 = keys_list[0]
                   #print(key0)
                key1 = keys_list[1]
                #print(value_dict[key1])
                key2 = keys_list[2]
                #print(value_dict[key2])
                feature_dict={}
                feature_dict = value_dict[key2]
                
                for c,d in feature_dict.items():
                  if not c.startswith('span'):
                   noneminilist.append(d) 
                   #print("%s\t%s\t%s"%(k,c,d)) 
                #minilist.append(value_dict[key3])
                noneminilist.append(k)
                noneminilist.append(value_dict[key1])

                nonenewstring =  '\t'. join(noneminilist)
                #print(nonenewstring)
                OVERVIEWFILE.write("%s\n"%(nonenewstring))


            with open(outfile, "w") as o:
                json.dump(readab, o)
        #except AssertionError as ae:
        #    logger.warning("Failed to parse {}. Skipping document.", source_f.stem)
        #    print(ae)


def test():
    example_json = Path(r"example_data\jemen.json")
    readab = json2readab(example_json, "example_id")
    pprint(readab)
    with open(Path("example_data") / "example_readab_out.json", "w") as outfile:
        json.dump(readab, outfile)


def json2readab(json_fileobject, doc_id, strict=True):
    """Returns a readab-formatted dict.

    If strict is True, articles that contain no IPTC topic annotations, entities or events are discarded.
    """

    ## AUX

    def is_in_spanObject(query_spanObject, target_spanObject):
        """A `spanObject` is a dict object that has `"begin"` and `"end"` as keys.
        The `"begin"` attritube of each object is missing if it is 0.
        Returns true if the query object's span in inside the target object's.
        """
        qb = query_spanObject["begin"] if "begin" in query_spanObject else 0
        qe = query_spanObject["end"]
        tb = target_spanObject["begin"] if "begin" in target_spanObject else 0
        te = target_spanObject["end"]
        return qb >= tb and qe <= te

    def annotation_tokens(annotation, source_tokens):        
        """`source_tokens` is a list of e.g. `{"sofa" : 12,  "begin" : 26,  "end" : 32 }`.
        """
        return [
            i
            for i, tok in enumerate(source_tokens)
            if is_in_spanObject(tok, annotation)
        ]

    def tokensIds_to_string(token_ids, token_string):  
        
        return " ".join([token_string.split(" ")[i] for i in token_ids])

    # id generators
    sentIds = (f"sentence_{n}" for n in range(1, 100))
    entity_annIds = (f"entity_{n}" for n in range(1, 100))
    event_annIds = (f"event_{n}" for n in range(1, 100))

    ## BODY

    source = json.load(json_fileobject)

    source_initialView = source["_views"]["_InitialView"]

    ##if strict:
        # check: doc must contain at least one entity and at least one event annotation to appear in the corpus
        #assert "Entities" in source_initialView, f"{doc_id} contains no entities."
        #assert "Eventclauses" in source_initialView, f"{doc_id} contains no events."

    # initialize readab skeleton with initial values
    readab = {
        "meta": {"id": None, "author": None},
        "doc": {
            "token_string": None,
            "token_ids": [],
            "sentences": {},
            "annotations": {
                ##"entities": {},
                "events": {},
                "none_events": {},
                ##"coreference": {},
                ##"iptc_codes": {},
            },
        },
    }

    ## METADATA

    readab["meta"]["id"] = doc_id
    print(doc_id)
    author = source_initialView["DocumentMetaData"][0]["documentId"]
    readab["meta"]["author"] = author

    ## TEXT AND TOKENS

    # the sofa string is always in the node mysteriously named "12"
    tokens = source["_referenced_fss"]["12"]["sofaString"].split(" ")
    tokens = [tok.strip() for tok in tokens]
    readab["doc"]["token_string"] = " ".join(tokens)
    readab["doc"]["token_ids"] = [i for i, _ in enumerate(tokens)]

    # check
    # get tokens defined in source and verify they match with the readab tokens
    # e.g. [{"sofa" : 12,  "end" : 9 }, {"sofa" : 12,  "begin" : 10,  "end" : 19 }]
    source_tokens = source_initialView["Token"]
    #assert len(readab["doc"]["token_ids"]) == len(
    #    source_tokens
    #), f"{doc_id}: tokens badly parsed."

    ## SENTENCES

    # e.g. [{"sofa" : 12,  "end" : 32 }, {"sofa" : 12,  "begin" : 34,  "end" : 106 }]
    source_sentences = source_initialView["Sentence"]
    sort_by_end = lambda l: sorted(l, key=lambda el: el["end"])

    # for each sentence, find which tokens belong to it
    # then add sentences to readab
    for source_sentence in sort_by_end(source_sentences):
        ss_tokenIndices = [
            i
            for i, source_tok in enumerate(source_tokens)
            if is_in_spanObject(source_tok, source_sentence)
        ]
        sentence = {"token_ids": ss_tokenIndices}
        readab["doc"]["sentences"][next(sentIds)] = sentence

    ## ANNOTATIONS
    # annotations in `source_initialView["Entities"]` or the corresponding `events` entries come in two flavours
    # either directly as a dict e.g. `{"sofa" : 12,  "begin" : 253,  "end" : 283,  "Entitytype" : "PER",  "Head" : [{"_type" : "EntitiesHeadLink",  "role" : "Head",  "target" : 714 } ],  "Individuality" : "GROUP",  "Mentionleveltype" : "NOM" }`
    # either as an int reference to an object listed in `source["_referenced_fss]"`


    # --> transform them into buckets
    def resolve_buckets(link_annotations):
        links = [(l["Dependent"], l["Governor"]) for l in link_annotations]
        buckets = []
        for a, b in links:
            bucket = [a, b]
            for l in links:
                if a in l or b in l:
                    bucket.extend(l)
            bucket = set(bucket)
            if bucket not in buckets:
                buckets.append(bucket)
        return buckets



    ## COLLECT EVENTS ##
    events = source_initialView.get("Eventclauses")
    if events == None:
        events = []
    for source_ann in events:

        ann_id = next(event_annIds)

        if isinstance(source_ann, int):
            sourceId_to_readabId[source_ann] = ann_id
            source_ann = source["_referenced_fss"][str(source_ann)]
        toks = annotation_tokens(source_ann, source_tokens)

        new_event = {
            "annotation_type": "event",
            "string": tokensIds_to_string(toks, readab["doc"]["token_string"]),
            "features": {
                "span": toks,
                #"arguments": [],  # will be filled up
                #"type": source_ann["Eventtype"],
                #"subtype": source_ann["Eventsubtype"],
                #"modality": source_ann["Modality"],
                #"pos_neg": source_ann["Positivenegative"],
                "prominence": source_ann["Prominence"],
                "EventPolarity": source_ann["EventPolarity"],
                #"tense": source_ann["Tense"],
            },
        }

        readab["doc"]["annotations"]["events"][ann_id] = new_event



    # add info to the annotations: in which sentence does it occur?

    def which_sentence(annotation):
        for s_id, s_tokens in readab["doc"]["sentences"].items():
            if annotation["features"]["span"][0] in s_tokens["token_ids"]:
                return s_id
        assert (
            False
        ), f"{doc_id}: no home sentence found for event. Should be impossible."

    ##for entity in readab["doc"]["annotations"]["entities"].values():
    ##    entity["home_sentence"] = which_sentence(entity)
    for event in readab["doc"]["annotations"]["events"].values():
        event["home_sentence"] = which_sentence(event)


    ## COLLECT NONE EVENTS ##

    #access to sentences to check None events
    #make list of tuples with list of token ids as left element, and string as right elem., of complete sentence that are 'NONE' event:
    #[17, 18, 19, 20, 21, 22, 23] De Gentsche Sosseteit staat te popelen .
    #print(readab["doc"]["token_string"])
    token_vals_sentences = []
    for key,val in readab["doc"]["sentences"].items():
        for item in val:
          #print(val[item])
          #print(tokensIds_to_string(val[item], readab["doc"]["token_string"]))
          #print(tokensIds_to_string(val[item], readab["doc"]["token_string"]))
          token_vals_sentences.append((val[item],tokensIds_to_string(val[item], readab["doc"]["token_string"]),key))
          
    for source_ann in events:

        ann_id = next(event_annIds)

        if isinstance(source_ann, int):
            sourceId_to_readabId[source_ann] = ann_id
            source_ann = source["_referenced_fss"][str(source_ann)]
        toks = annotation_tokens(source_ann, source_tokens)
        #check all sentence toks :if event toks are in all sent toks:
        for tokens,string,sentid in token_vals_sentences:
               #print(tokens)
               #print(toks)
               #if event tokens are part of complete sentence tokens, remove toks, string tuple from the list, in order to have only None events
               if(set(toks).issubset(set(tokens))):
                    
                    token_vals_sentences.remove((tokens,string,sentid))
               #else:
               #     pass


    
    for toks,string,sentid in token_vals_sentences:



        none_event = {
            "annotation_type": "none_event",
            "string": string,
            "features": {
                "span": toks,
                #"arguments": [],  # will be filled up
                #"type": source_ann["Eventtype"],
                #"subtype": source_ann["Eventsubtype"],
                #"modality": source_ann["Modality"],
                #"pos_neg": source_ann["Positivenegative"],
                "prominence": "None",
                "EventPolarity": "None",
                #"tense": source_ann["Tense"],
                #"home_sentence": sentid,
            },
        }
        #print(none_event)
              
        readab["doc"]["annotations"]["none_events"][sentid] = none_event

    #print(readab)
    return readab
