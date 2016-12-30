# ad.finder

### dataset
[kaggle](https://www.kaggle.com/c/dato-native/data)

### tech
[scikit-learn](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
bs4


### scikit-learn

building a pipeline

###  ideas
* bag of words
* number of links

### running a pipeline example
> python ad_finder/scripts/run_pipeline.py --docs /home/chrirs/other/dato.native/text_extracted/0.zip --categories /home/chrirs/other/dato.native/train_v2.csv.zip --test_fraction 0.1 --max_doc_count 10000


### results
#####  baseline v0.1
12/30/2016 11:39:03 PM Average success rate 0.912.
             precision    recall  f1-score   support

          0       0.98      0.93      0.95      5296
          1       0.28      0.56      0.37       259

avg / total       0.94      0.91      0.93      5555

##### svm v0.1
12/30/2016 11:42:35 PM Average success rate 0.875.
             precision    recall  f1-score   support

          0       0.94      0.92      0.93      5120
          1       0.25      0.30      0.27       435

avg / total       0.89      0.88      0.88      5555