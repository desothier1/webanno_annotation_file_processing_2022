import json
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import re
import fileinput
import argparse
import os.path

### SPLIT INTO SENTENCES, ONE SENTENCE PER LINE

from pathlib import Path

splitter = SentenceSplitter(language='nl')

INFILE=open('sample.json','r')
data=json.load(INFILE)
OUTTOTAL=open('_ALLFILES.txt','w')
counter=0
for item in data:
  print(item)
  counter+=1
  TITLE=data[item]['title']
  SUBTITLE=data[item]['subtitle']
  outfilestring=""
  outfilestring= str(item) + "." + "txt"
  OUTFILE=open(outfilestring,'w')
  #OUTFILE.write("%s\n"%(TITLE))
  #OUTFILE.write("%s"%(SUBTITLE))


  splitsents=(splitter.split(text=TITLE))
  splitsents2=(splitter.split(text=SUBTITLE))



  for split in splitsents:
          segs1=[]
          #split2=re.sub(r'\|',' ',split)
          #split3=re.sub(r'\"',' ',split2)
          #if ":" in str(split3):
          #   segs1=re.split(pattern=r"[:]", string = str(split3))
          #   for seg in segs1:
          #       OUTFILE.write("%s\n"%(seg))

          #else:
          split1 = re.sub("\.$"," .",split)
          split2 = split1.replace(","," ,")
          split3 = split2.replace("?"," ?")
          split4 = split3.replace(";"," ;")
          split5 = split4.replace(":"," :")
          split6 = split5.replace("!"," !")
          split7 = split6.replace("(","( ")
          split8 = split7.replace(")"," )")
          split9 = re.sub("\"","", split8)
          split10 = re.sub("[ ]*\&[ ]*"," & ", split9)
          #split11 = re.sub("[ ]*-[ ]*"," - ", split10)

          OUTFILE.write("%s\n "%(split10))
          OUTTOTAL.write("%s\n"%(split10))


  for split in splitsents2:
          segs2=[]
          #split2=re.sub(r'\|',' ',split)
          #split3=re.sub(r'\"',' ',split2)
          #OUT.write("%s\n"%(split3))

          #if ":" in str(split3):
          #   segs2=re.split(pattern=r"[:]", string = str(split3))
          #   for seg in segs2:
          #       OUTFILE.write("%s\n"%(seg))

          #else:
          #split1 = re.sub('\.','. ',split)
          split1 = re.sub("\.$"," .",split)
          split2 = split1.replace(","," ,")
          split3 = split2.replace("?"," ?")
          split4 = split3.replace(";"," ;")
          split5 = split4.replace(":"," :")
          split6 = split5.replace("!"," !")
          split7 = split6.replace("(","( ")
          split8 = split7.replace(")"," )")
          split9 = re.sub("\"","", split8)
          split10 = re.sub("[ ]*\&[ ]*"," & ", split9)
          #split11 = re.sub("[ ]*-[ ]*"," - ", split10)

          OUTFILE.write("%s\n "%(split10))
          OUTTOTAL.write("%s\n"%(split10))



print("number of docs: " + str(counter))
