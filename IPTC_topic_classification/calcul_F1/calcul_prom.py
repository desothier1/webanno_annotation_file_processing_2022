from evalutils import f1_score_func
from evalutils import precision_recall_fscore_support_func
from evalutils import classification_report_func
from evalutils import cnf_matrix_func
from evalutils import plot_confusion_matrix

#REFFILE=open('ref.txt','r')
#HYPFILE=open('hyp.txt','r')

REFFILE=open('REF_out.txt','r')
HYPFILE=open('HYP_out.txt','r')

true_heldouttest=[]
predictionsheldouttest=[]

for line in REFFILE:
	line=line.strip()
	true_heldouttest.append(line)

for line in HYPFILE:
	line=line.strip()
	predictionsheldouttest.append(line)

print(true_heldouttest)

#print("---HELDOUTTTEST EVALUATION---")

#accuracy_per_class(predictionsheldouttest, true_heldouttest)
f1_score_func(predictionsheldouttest, true_heldouttest)

#accuracy_score_func(predictions, true_vals)

#print("Precision, Recall, F-score weighted, micro, macro")
print(precision_recall_fscore_support_func(true_heldouttest, predictionsheldouttest) )


print(classification_report_func(true_heldouttest, predictionsheldouttest))

#label_dict = {'Negative': 0, 'Neutral': 1, 'Positive': 2}

#cnf_matrix_func(true_heldouttest, predictionsheldouttest,label_dict)

