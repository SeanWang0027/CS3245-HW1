# CS3245-HW1

## Python Version

I'm using Python Version <3.10.12 or replace version number> for
this assignment.

## General Notes about this assignment

I create a class named Language, and this defines an object for a specific language model.
For each object, they have three properties: language's name(label), language's total tokens and its token list.
Using the self-defined Produce_4grams function, the language model collect 4-gram for sentence.
Then they are selected and added to each object. The object also has function to do add_one smoothing.
Then during the process of testing the model, I first scan the input's 4 gram and check whether it has been seen by the language model during the train time.
And I set the threshold = 0.5, meaning that if the probability of a language's missing 4 gram tokens is higher than 0.5, it will be considered as alien language.
If the language is not alien ones, just carry out the process of calculating the probability for each language.
Since the possibility of each token in one language is so small, I use math.log to carry out the calculation. Also ignoring the alien tokens.
And then I compared the result and put the most likely ones as the output label and write in file.
Problem met:
calculating the result when encountering the alien tokens. Just skipped them.

## Files included with this submission

build_test_LM.py:
This is where I put all the source code about my project.
README.md:
This is the README file for my study.
ESSAY.txt:
The optional questiong answering document.
