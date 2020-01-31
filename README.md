#Question 2
The Naive Bayes algorithm is implemented to calculate the probabilty for multiple classes. This can be implemented in the followin way
python NaiveBayes.py TRAIN TEST MODEL-FILE RESULT-FILE

#Question 3
The NLP question to generate words for a sentence has been implemented to run in the following manner
python MarkovChain.py "AUTH-DIR" PROB-FILE RESULT-FILE
Note: Kindly refrain from adding the "\" along with the author directory

The extra credit question can be called in the same manner as defined above in the following manner
python MarkovChain.py "AUTH-DIR-1" "AUTH-DIR-2" PROB-FILE-1 PROB-FILE-2 RESULT-FILE

#Explanation
For the comparison of sentences between two authors, instead of taking an alpha value of 0, i have considered a value of e-04 as the probablities of the unigrams in my list of words are much smaller than e-04 and my observations have been written in the attached pdf document