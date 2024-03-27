#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
import string
import math

# tool functions
'''
Function Name: Produce_Sentence
Input Parametres:
    @str: input string
Output Parametres:
    @label: The label of the sentence
    @ngrams: The 4_gram result for each sentence
'''
def Produce_Sentence(str):
    words = str.split()
    label = words[0]
    new_str = re.sub(r'^\w+\s+', '', str)
    tokens = []
    for char in new_str:
        if char=='\n':
            continue
        if char not in string.whitespace:
            tokens.append(char)
        else:
            tokens.append(char)
    ngrams = []
    for i in range(len(tokens)-3):
        ngrams.append(tuple(tokens[i:i+4]))
    return label,ngrams

'''
Function Name: Produce_4grams
Input Parameters:
    @new_str: the string needed to be processed as 4 grams
Output Parameters:
    @ngrams: the processed 4 gram token lists
'''
def Produce_4grams(new_str):
    tokens = []
    for char in new_str:
        if char=='\n':
            continue
        if char not in string.whitespace:
            tokens.append(char)
        else:
            tokens.append(char)
    ngrams = []
    for i in range(len(tokens)-3):
        ngrams.append(tokens[i:i+4])
    ngrams = []
    for i in range(len(tokens)-3):
        ngrams.append(tuple(tokens[i:i+4]))
    return ngrams

'''
Function Name: check_miss
Function Purpose: to check the ngram tuples that is not shown in the training set
Input Parameter:
    @languages: the language model generate from the training set
    @ngrams: the 4 gram tuple list generated
    @threshold: the missing threshold to determine whether it is an alien language
Output Parameter:
    True or False: whether it is an alien language
'''
def check_miss(languages,ngrams,threshold):
    miss_count = 0
    mark = False
    for ngram in ngrams:
        for language in languages:
            for token in language.token_list:
                if token==ngram:
                    mark = True
                    break
            if mark==True:
                break
        if mark==False:
            miss_count+=1
        mark = False
    return (miss_count/len(ngrams))>threshold
                
'''
This is a structure that determines the language model itself.
Parameters:
    @label: what is the language, the name of it.
    @total_tokens: How many tokens(4 gram) does the language contains
    @token_dict: the key is the token(4 gram), and the value is the time that token appears
'''          
class Language:
    def __init__(self,label,total_tokens,token_dict):
        self.label = label
        self.total_tokens = total_tokens
        self.token_list = token_dict
    
    '''
    Function Name: Language.add_token
    Parameters:
        @new_token: the new 4 gram needed to be added into the token list
    '''
    def add_token(self,new_token):
        if new_token in self.token_list:
            self.token_list[new_token]+=1
        else:
            self.token_list[new_token] = 1
        self.total_tokens += 1
    
    '''
    Function Name: Language.add_one_smooth
    Function Purpose: to add the other language's 4 gram to generate better result
    Parameters:
        @whole_tokens: the tokens of whole three languages
    '''
    def add_one_smooth(self,whole_tokens):
        mark = False
        for token in whole_tokens:
            if token in self.token_list:
                pass
            else:
                self.token_list[token] = 0
                mark = True
        if mark == True:
            for token in self.token_list:
                self.token_list[token]+=1 
                self.total_tokens+=1    
    
    '''
    Function Name: Language.compute_frequency
    Function Purpose: to transfer the count of it into the probability of it
    '''
    def compute_frequency(self):
        for token in self.token_list:
            self.token_list[token] /= self.total_tokens
    
    '''
    Function Name: Language.compute_possibility
    Function Purpose: given a sentence , calculate the possibility of it contained in the language
    Parameters:
        @ngrams: the 4 gram token list of the input
    '''
    def compute_possibility(self,ngrams):
        res = 0
        for gram in ngrams:
            if gram in self.token_list:
                res += math.log(self.token_list[gram])
            else: 
                pass
        return res

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    # This is an empty method
    # Pls implement your code below
    file = open(in_file,'r')
    label = [] # this is to store the label for each sentence
    malaysian = Language('malaysian',0,{}) # the malaysian model
    indonesian = Language('indonesian',0,{}) # the indonesian model
    tamil = Language('tamil',0,{}) # the tamil model
    whole_tokens =  set()
    for line in file: # to get the label for each word and the ngram format
        label,new_line = Produce_Sentence(line)
        if label=='malaysian':
            language = malaysian
        elif label=='indonesian':
            language = indonesian
        else:
            language = tamil
        for gram in new_line:
            whole_tokens.add(gram)
            language.add_token(gram)
    
    # add one smoothing for each language
    malaysian.add_one_smooth(whole_tokens)
    indonesian.add_one_smooth(whole_tokens)
    tamil.add_one_smooth(whole_tokens) 
    
    # compute the frequency for each language 
    malaysian.compute_frequency()
    indonesian.compute_frequency()
    tamil.compute_frequency()  
    
    # this is to return a tuple that contains a language model for each language.
    return (malaysian,indonesian,tamil)


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code below
    threshold = 0.5 # to judge alien language
    malaysian,indonesian,tamil = LM 
    input_file = open(in_file,'r')
    output_file = open(out_file,'w')
    for line in input_file: 
        ngrams = Produce_4grams(line)
        if check_miss(LM,ngrams,threshold):# just to check if the sentence is a so-called 'alien sentence'
            output_file.write('other '+line)
            continue
        # calculate the probability of different language
        pro_malaysian= malaysian.compute_possibility(ngrams)
        pro_indonesian = indonesian.compute_possibility(ngrams)
        pro_tamil = tamil.compute_possibility(ngrams)
        if pro_malaysian>=pro_indonesian and pro_malaysian >= pro_tamil:
            output_file.write('malaysian '+line)
        elif pro_indonesian> pro_malaysian and pro_indonesian> pro_tamil:
            output_file.write('indonesian '+line)
        else:
            output_file.write('tamil '+line)
    
def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
