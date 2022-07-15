import json
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import re
import fileinput
import argparse
import os.path

### SPLIT INTO SENTENCES, ONE SENTENCE PER LINE

from pathlib import Path
splitter = SentenceSplitter(language='nl')


iptc_template = """
TOPIC			medtop:01000000 	arts, culture, entertainment and media 		medtop:16000000 	conflict, war and peace 		medtop:02000000 	crime, law and justice 		medtop:03000000 	disaster, accident and emergency incident 		medtop:04000000 	economy, business and finance 		medtop:05000000 	education 		medtop:06000000 	environment 		medtop:07000000 	health 		medtop:08000000 	human interest 		medtop:09000000 	labour 		medtop:10000000 	lifestyle and leisure 		medtop:11000000 	politics 		medtop:12000000 	religion 		medtop:13000000 	science and technology 		medtop:14000000 	society 		medtop:15000000 	sport 		medtop:17000000 	weather 
																																																				
SUBTOPIC			medtop:20000002 	arts and entertainment 		medtop:20000053 	act of terror 		medtop:20000082 	crime 		medtop:20000139 	accident and emergency incident 		medtop:20000170 	business information 		medtop:20000412 	curriculum 		medtop:20000418 	climate change 		medtop:20000446 	diseases and conditions 		medtop:20000497 (retired) 	accomplishment (retired) 		medtop:20000509 	employment 		medtop:20000538 	leisure 		medtop:20000574 	election 		medtop:20000657 	belief systems 		medtop:20000710 	biomedical science 		medtop:20000768 	communities 		medtop:20000822 	competition discipline 		medtop:20001128 	weather forecast 
SUBTOPIC			medtop:20000038 	culture 		medtop:20000056 	armed conflict 		medtop:20000106 	judiciary 		medtop:20000148 	disaster 		medtop:20000209 	economic sector 		medtop:20001338 	education policy 		medtop:20000420 	conservation 		medtop:20000480 	government health care 		medtop:20000500 	animal 		medtop:20000521 	employment legislation 		medtop:20000565 	lifestyle 		medtop:20000587 	fundamental rights 		medtop:20000687 (retired) 	interreligious dialogue (retired) 		medtop:20000715 	mathematics 		medtop:20000770 	demographics 		medtop:20001103 	disciplinary action in sport 		medtop:20001129 	weather phenomena 
SUBTOPIC			medtop:20000045 	mass media 		medtop:20000065 	civil unrest 		medtop:20000119 	justice 		medtop:20000160 (retired) 	emergency incident (retired) 		medtop:20000344 	economy 		medtop:20001217 	educational grading 		medtop:20000424 	environmental pollution 		medtop:20000461 	health facility 		medtop:20001237 	anniversary 		medtop:20000523 	labour market 		medtop:20001339 	wellness 		medtop:20000593 	government 		medtop:20000702 	relations between religion and government 		medtop:20000717 	natural science 		medtop:20000775 	discrimination 		medtop:20001104 	drug use in sport 		medtop:20001130 	weather statistic 
SUBTOPIC						medtop:20000070 	coup d'etat 		medtop:20000121 	law 		medtop:20000167 (retired) 	emergency planning (retired) 		medtop:20000385 	market and exchange 		medtop:20000413 	educational testing and examinations 		medtop:20000430 	natural resources 		medtop:20000483 	health insurance 		medtop:20000498 	award and prize 		medtop:20000524 	labour relations 					medtop:20000621 	government policy 		medtop:20000688 	religious conflict 		medtop:20000741 	scientific institution 		medtop:20000772 	emigration 		medtop:20001301 	sport achievement 		medtop:20001131 	weather warning
SUBTOPIC						medtop:20000071 	massacre 		medtop:20000129 	law enforcement 		medtop:20000168 	emergency response 					medtop:20000414 	entrance examination 		medtop:20000441 	nature 		medtop:20000463 	health organisations 		medtop:20001238 	birthday 		medtop:20000531 	retirement 					medtop:20000638 	international relations 		medtop:20000689 (retired) 	religious event (retired) 		medtop:20000735 	scientific research 		medtop:20000780 	family 		medtop:20001108 	sport event 			
SUBTOPIC						medtop:20000073 	peace process 											medtop:20001337 	online and remote learning 					medtop:20000464 	health treatment 		medtop:20000505 	celebrity 		medtop:20000533 	unemployment 					medtop:20000646 	non-governmental organisation 		medtop:20000697 	religious facility 		medtop:20000755 	scientific standards 		medtop:20000771 	immigration 		medtop:20001124 	sport industry 			
SUBTOPIC						medtop:20000077 	post-war reconstruction 											medtop:20000398 	parents group 					medtop:20000485 	medical profession 		medtop:20000501 	ceremony 		medtop:20000536 	unions 					medtop:20000647 	political crisis 		medtop:20000690 	religious festival and holiday 		medtop:20000742 	social sciences 		medtop:20000788 	mankind 		medtop:20001125 	sport organisation 			
SUBTOPIC						medtop:20000080 	prisoners of war 											medtop:20000399 	religious education 					medtop:20000493 	non-human diseases 		medtop:20000507 	flowers and plants 								medtop:20000648 	political dissent 		medtop:20000703 	religious leader 		medtop:20000756 	technology and engineering 		medtop:20000799 	social condition 		medtop:20001126 	sport venue 			
SUBTOPIC																		medtop:20000400 	school 					medtop:20000484 	private health care 		medtop:20000504 	high society 								medtop:20000649 	political process 		medtop:20000696 	religious ritual 					medtop:20000802 	social problem 		medtop:20001323 	sports coaching 			
SUBTOPIC																		medtop:20000410 	social learning 								medtop:20000503 	human mishap 											medtop:20000705 	religious text 					medtop:20000808 	values 		medtop:20001324 	sports management and ownership 			
SUBTOPIC																		medtop:20000415 	students 								medtop:20000502 (retired) 	people (retired) 																	medtop:20000817 	welfare 		medtop:20001325 	sports officiating 			
SUBTOPIC																		medtop:20000416 	teachers 								medtop:20000499 	record and achievement 																				medtop:20001148 	sports transaction 			
SUBTOPIC																		medtop:20000411 (retired) 	teaching and learning (retired) 																																	
SUBTOPIC																		medtop:20001216 	vocational education 																																	
																																																															
"""




INFILE=open('sample.json','r')
data=json.load(INFILE)
OUTTOTAL=open('_ALLFILES_TITLE_LEAD_CONTENT.txt','w')
counter=0
for item in data:
  print(item)
  #WRITE ITEM
  OUTTOTAL.write("\n\n%s\n\n"%(item))
  OUTTOTAL.write(iptc_template)
  counter+=1
  TITLE=data[item]['title']
  SUBTITLE=data[item]['subtitle']
  CONTENT=data[item]['content']
  outfilestring=""
  outfilestring= str(item) + "." + "txt"
  #OUTFILE=open(outfilestring,'w')
  #OUTFILE.write("%s\n"%(TITLE))
  #OUTFILE.write("%s"%(SUBTITLE))


  splitsents=(splitter.split(text=TITLE))
  splitsents2=(splitter.split(text=SUBTITLE))
  splitsents3=(splitter.split(text=CONTENT))


  OUTTOTAL.write("\n\tTITLE\n")
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

          #OUTFILE.write("%s\n "%(split10))
          OUTTOTAL.write("\t\t%s\n"%(split10))

  OUTTOTAL.write("\n\tSUBTITLE\n")
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

          #OUTFILE.write("%s\n "%(split10))
          OUTTOTAL.write("\t\t%s\n"%(split10))

  OUTTOTAL.write("\n\tCONTENT\n")
  for split in splitsents3:
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

          #OUTFILE.write("%s\n "%(split10))
          OUTTOTAL.write("\t\t%s\n"%(split10))

print("number of docs: " + str(counter))
