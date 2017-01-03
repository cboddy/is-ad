# is-ad
Is it an ad?

### install 
> pip install -r requirements.txt

### web
Run the web-service
> python -m is_ad/scripts/run_web -h

### running a pipeline example
> python ad_finder/scripts/run_pipeline.py --docs /home/chrirs/other/dato.native/text_extracted/0.zip --categories /home/chrirs/other/dato.native/train_v2.csv.zip --test_fraction 0.1 --max_doc_count 10000


### results

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






