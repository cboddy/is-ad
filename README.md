# ad.finder

### dataset
[kaggle](https://www.kaggle.com/c/dato-native/data)

### tech
[scikit-learn](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
bs4


### scikit-learn

building a pipeline
* [feature extraction](http://scikit-learn.org/stable/modules/feature_extraction.html)

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


##### svm v0.2
12/31/2016 10:12:16 AM Average success rate 0.814.
             precision    recall  f1-score   support

          0       0.84      0.95      0.89       878
          1       0.61      0.29      0.39       230

avg / total       0.79      0.81      0.79      1108


### svm v0.3
##### grid-search, text-extracted, 5000 docs
2/31/2016 10:37:54 AM Average success rate 0.850.
('best-score', 0.89499774673276256)
best-score-param clf__alpha : 0.01
best-score-param vect__ngram_range : (1, 2)
             precision    recall  f1-score   support


          0       0.90      0.93      0.91       481
          1       0.41      0.35      0.38        72

avg / total       0.84      0.85      0.84       553




**unicode html text-extraction helped!**

### svm v0.21 
01/03/2017 12:45:52 PM              precision    recall  f1-score   support

          0       0.99      0.98      0.99      6810
          1       0.85      0.94      0.89       686
         
avg / total       0.98      0.98      0.98      7496


### baseline v0.21
01/03/2017 12:52:09 PM Average success rate 0.963.
01/03/2017 12:52:09 PM              precision    recall  f1-score   support

          0       0.99      0.97      0.98      6917
          1       0.70      0.91      0.79       579

avg / total       0.97      0.96      0.97      7496






