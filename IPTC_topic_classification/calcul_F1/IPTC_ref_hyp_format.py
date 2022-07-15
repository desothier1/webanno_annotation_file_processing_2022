import json
import re
import fileinput
import argparse
import os.path

### SPLIT INTO SENTENCES, ONE SENTENCE PER LINE

from pathlib import Path

#splitter = SentenceSplitter(language='nl')



class Evaluate_IPTC_topics:

 def __init__ (self, identif, refers=[], hypoths=[]):
   self.identif, self.refs, self.hyps = identif, refers, hypoths

 def eval_proces(self):
   outlist=[]
   counter=0
   for hyp_item in self.hyps:
     counter+=1
     #print(counter,ref_item,self.identif)
     #if HYP in refs = hypothesis is correct
     #concatenate filename+iptc topic identifier + '\t' + 'CORRECT'
     #otherwise : 
     #concatenate filename+iptc topic identifier + '\t' + 'ERROR' 
     if hyp_item in self.refs:
        ITEM_HYP = self.identif + "_" + str(counter) + '\t' + hyp_item + '\t' + hyp_item
        #outlist.append(ITEM_REF)
        #print(ITEM_HYP)
        outlist.append(ITEM_HYP)
     else:
        ITEM_HYP = self.identif + "_" + str(counter) + '\t' + hyp_item + '\t' + "None"
        #outlist.append(ITEM_REF)
        #print(ITEM_HYP)
        outlist.append(ITEM_HYP)

   #print(outlist)
   return outlist
   #ITEM_HYP=""
   #counter=0
   #outlist=[]
   #print(self.identif, self.refs, self.hyps)
   #output format : dmf20211112_94497931 ['5000000', '14000000'] ['5000000', '8000000', '14000000']
   #                ID                   REF topic items         HYP topic items
   # for hyp_item in self.hyps:
   #     counter+=1
       #if HYP in refs = hypothesis is correct
       #concatenate filename+iptc topic identifier + '\t' + 'CORRECT'
       #otherwise : 
       #concatenate filename+iptc topic identifier + '\t' + 'ERROR' 
   #     if hyp_item in self.refs:
   #        ITEM_HYP = self.identif + "_" + str(counter) + '\t' + hyp_item + '\t' + hyp_item
   #     else:
   #        ITEM_HYP = self.identif + "_" + str(counter) + '\t' + hyp_item + '\t' + "None"         
   #     return ITEM_HYP
   #print(len(self.refs))
   #for ref_item in self.refs:
       #counter+=1
       #print(counter)

       #print(self.identif,ref_item,self.refs)
       #if HYP in refs = hypothesis is correct
       #concatenate filename+iptc topic identifier + '\t' + 'CORRECT'
       #otherwise : 
       #concatenate filename+iptc topic identifier + '\t' + 'ERROR' 
       #if ref_item in self.hyps:
       #   ITEM_REF = self.identif + "_" + str(counter) + '\t' + ref_item + '\t' + ref_item
       #   outlist.append(ITEM_REF)
       #else:
       #   ITEM_REF = self.identif + "_" + str(counter) + '\t' + ref_item + '\t' + "None"
       #   outlist.append(ITEM_REF)
       #print(outlist)      
       #return outlist



if __name__ == '__main__':

 IPTC_TOPIC_LEVEL1_LIST=[1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 11000000, 12000000, 13000000, 14000000, 15000000, 16000000, 17000000]

 OUT_REF=open('REF_out.txt','w')
 OUT_HYP=open('HYP_out.txt','w')

#PREDICTED IPTC DATA

 INFILE=open('sample.json','r')
 data=json.load(INFILE)
 #OUTTOTAL=open('_ALLFILES.txt','w')
 counter=0
 PREDICTED_DATA=[]
 for item in data:
   #print filename
   itemlist=[]
   #print(item)
   itemlist.append(item)

   for a in data[item]:
      if "topics" in a:
         newlist=[]
         newlist = data[item][a]
         #print(data[item][a])
         #print(newlist)
        
         for elem in newlist:
          
            for a in elem:

              if "id" in a:
               #print(a,elem[a])
               #itemlist.append(elem[a])
               #only select the 17 Level 1 topics
               #if (int(elem[a])) in IPTC_TOPIC_LEVEL1_LIST:
                id=elem[a]
               #remove leading '0'
                id=re.sub(r'^0','',id)

               #id_score_dict={}
              if "score" in a:
               #print(a,elem[a])
               #itemlist.append(elem[a])
                score=elem[a]

             #id_score_dict[score]=id
             #print(id_score_dict)
            tuple_id_score=(id,score)
           #check that only LEVEL 1 topics are selected
            if (int(tuple_id_score[0])) in IPTC_TOPIC_LEVEL1_LIST:
             #select minimum value of conf. score : default 0
             #CONF MEAS >= 0
             #if tuple_id_score[1] >= 0:            
             #CONF MEAS >= 0.75
              if tuple_id_score[1] >= 0.75:
              #print(tuple_id_score[1])
               itemlist.append(tuple_id_score[0])

  #print(itemlist)
   PREDICTED_DATA.append(itemlist)
  #outfilestring=""
  #outfilestring= str(item) + "." + "json"


  #OUTFILE = open(outfilestring, "w")
  
  #json.dump(data[item], OUTFILE, indent = 6)
  
  #OUTFILE.close()
#print(itemlist)

#print(PREDICTED_DATA)
#FORMAT : list of lists
#each list: filename, IPTC topic + conf measure score
#['dmf20211112_94497931', ('05000000', 0.9986758828163147), ('08000000', 0.46577557921409607), ('14000000', 0.7848258018493652)]
#for item in PREDICTED_DATA:
#  print(item)


#REFERENCE IPTC DATA

 INFILE_REF=open('REFDATA.txt','r')
 REFERENCE_DATA=[]
 for line in INFILE_REF:
    REF_ITEM_LIST=[]

    line=line.strip()
   #print(line)
    segs=line.split('\t')
   #ADD FILENAME TO LIST
    REF_ITEM_LIST.append(segs[0])
   #print(segs)
   #print(len(segs))
   #list of split segments fields
    seg_numbers = [4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52]
    for item in seg_numbers:
      item_minus_2 = item - 2
      if len(segs[item]) > 0:
       tuple_ID_rank=(segs[item_minus_2],int(segs[item]))
      #in tuple : IPTC topic level 1 identifier, and ranking
      #we keep only identifier of IPTC topic level 1
       REF_ITEM_LIST.append(tuple_ID_rank[0])
   #print(REF_ITEM_LIST)
    REFERENCE_DATA.append(REF_ITEM_LIST)

#print(REFERENCE_DATA)

 for REF_item,PRED_item in zip(REFERENCE_DATA,PREDICTED_DATA):
   #print(str(REF_item) + "\t" + str(PRED_item))
   #extract from REF_ITEM : filename, and ref. iptc topics level1 // extract from PRED_ITEM, predicted IPTC topics
   #print(REF_item[0],REF_item[1:],PRED_item[1:])
   
   #EVALUATE HYP IPTC TOPICS
    REF_HYP_obj=Evaluate_IPTC_topics(REF_item[0],REF_item[1:],PRED_item[1:])
    RESULT_ITEM=REF_HYP_obj.eval_proces()
    for item in RESULT_ITEM:
      itemsegs=item.split('\t')
      refitem=""
      hypitem=""
      refitem=str(itemsegs[1])
      hypitem=str(itemsegs[2])
      OUT_REF.write("%s\n"%(refitem))
      OUT_HYP.write("%s\n"%(hypitem))



