#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 00:51:06 2021

@author: shubhashreedash
"""
"""
input_file = open("input.txt", 'r')
no_of_queries = input_file.readline().strip()
for _ in range(no_of_queries):
    input_file.readline().strip()

no_of_sentences = input_file.readline().strip()
for _ in range(no_of_sentences):
    input_file.readline().strip()
"""  
from copy import deepcopy 
import sys

IMPLICATION = "=>"
AND = "&"
NEGATION = "~"
NEGATIVE_POSITION = 0
PREDICATE_NAME = 1
ARGUMENTS = 2

  
class Knowlegde_term:
    predicate = ""
    arguments = []
    negative = False
    def __init__(self,term_tuple):
        negative,predicate,arguments = term_tuple
        self.predicate = predicate
        self.arguments = arguments
        self.negative = negative
        self.sentence = str(negative) + predicate + "(" + ",".join(arguments) + ")"
        self.resolve_search = str(1 if negative == -1 else -1) + predicate
        self.kb_key = str(negative) + predicate 
        
    def __str__(self):
        return self.sentence
    
    def __eq__(self, second_term):
        return self.sentence == second_term.sentence
    
    def __hash__(self):
        return hash(self.sentence)
        
    def update_arguments(self,i, new_arg):
        self.arguments[i] = new_arg
        self.sentence = str(self.negative) + self.predicate + "(" + ",".join(self.arguments) + ")"

    def update_negation(self, negative):
        self.negative = negative
        self.sentence = str(self.negative) + self.predicate + "(" + ",".join(self.arguments) + ")"
        self.resolve_search = str(1 if negative == -1 else -1) + self.predicate
        self.kb_key = str(negative) + self.predicate 


class Sentence:
    predicate_list = []
    sentence = ""
    def __init__(self,sentence_list):
        self.predicate_list = deepcopy(sentence_list)
        self.predicate_list.sort(key = lambda x: x.sentence)
        #for predicate in predicate_list:
        self.sentence = ",".join(list(map(str,[predicate.sentence for predicate in self.predicate_list])))
        
    def __eq__(self, second_statement):
        return self.sentence == second_statement.sentence
    
    def __hash__(self):
        return hash(self.sentence)
    
    def __str__(self):
        return self.sentence
    

def merge_kb(kb1, kb2):
    merged_kb = {**kb1, **kb2}
    for key in merged_kb:
        value = merged_kb[key]
        if key in kb1 and key in kb2:
            merged_kb[key] = list(set(value).union(kb1[key]))
    return merged_kb

def find_substitution(predicate_one, predicate_two, substitution):
    if(predicate_one.predicate  == predicate_two.predicate):
        for i in range(len(predicate_one.arguments)):        
            if( predicate_one.arguments[i] == predicate_two.arguments[i]):
                continue
                #return predicate_two, substitution
            elif( predicate_one.arguments[i] in substitution.keys() or predicate_two.arguments[i] in substitution.keys()):
                continue
            else:
                if(predicate_one.arguments[i][0].islower() and predicate_two.arguments[i][0].isupper()):
                    substitution[predicate_one.arguments[i]] = predicate_two.arguments[i]
                elif(predicate_two.arguments[i][0].islower() and predicate_one.arguments[i][0].isupper()):
                    substitution[predicate_two.arguments[i]] = predicate_one.arguments[i]
                elif(predicate_two.arguments[i][0].islower() and predicate_one.arguments[i][0].islower()):    
                    substitution[predicate_one.arguments[i]] = predicate_two.arguments[i]
                    
                    
    return substitution

def apply_substitution(sentence, substitution):
    for predicate in sentence:
        for i in range(len(predicate.arguments)):
            if predicate.arguments[i] in substitution.keys():
                predicate.update_arguments(i,substitution[predicate.arguments[i]])
    return sentence
 
def unify(predicate_one, sentence_two, sentence_one):
    #print('INSIDE OF UNIFY')
    sentence_two = deepcopy(sentence_two)
    sentence_one = deepcopy(sentence_one)
    
    new_unified_sentence = remove_duplicates(sentence_one,None,"OR")
    #print("SENT ONE OR ",Sentence(new_unified_sentence))
    if new_unified_sentence == []:
        return False, new_unified_sentence
    
    new_unified_sentence = remove_duplicates(sentence_two,None,"OR")
    #print("SENT TWO OR ",Sentence(new_unified_sentence))
    if new_unified_sentence == []:
        return False, new_unified_sentence
    
    unified_sentences = []

    predicate_subs = [x for x in sentence_two if x.kb_key == predicate_one.resolve_search]
    
    new_pred = []
    for predicate_sub in predicate_subs:
        flag = False
        for i in range(len(predicate_sub.arguments)):
            #print("ARGUMENTS :",predicate_one.arguments[i],predicate_sub.arguments[i])
            #print("CONDITION :",(predicate_one.arguments[i][0].isupper() and predicate_sub.arguments[i][0].isupper() and predicate_one.arguments[i] != predicate_sub.arguments[i]) or flag)
            if (predicate_one.arguments[i][0].isupper() and predicate_sub.arguments[i][0].isupper() and predicate_one.arguments[i] != predicate_sub.arguments[i]) or flag:
                flag = True
                continue
        if not flag:
            new_pred = new_pred + [predicate_sub]
    #find substitution 
    predicate_subs = deepcopy(new_pred)
    
    
    #print("PREDICATE SUBS :",list(map(str,predicate_subs)))
    
    for predicate_sub in predicate_subs:
        substitution = {}
        substitution = find_substitution(predicate_one, predicate_sub, substitution)
        #print("SUBSTITUTION :",substitution)
        sentence_complete = deepcopy(sentence_one + sentence_two)
        #print("COMPLETE SENTENCE : ",Sentence(sentence_complete))
        substituted_sentence = apply_substitution(sentence_complete, substitution)
        #print("SUBSTITUTED SENTENCE :",Sentence(sentence_complete))
        sub_predicate = apply_substitution([predicate_sub], substitution)
        new_unified_sentence = remove_duplicates(substituted_sentence,sub_predicate,"AND")

        #print("UNIFIED SENTENCE :",Sentence(new_unified_sentence))
        copy_sent = deepcopy(new_unified_sentence)
        if new_unified_sentence == []:
            return True, new_unified_sentence
        
        new_unified_sentence = remove_duplicates(new_unified_sentence,None,"OR")
        
        if new_unified_sentence == []:
            #print("SUB SENT :",Sentence(substituted_sentence))
            #print("RESOLVED :",Sentence(copy_sent))
            return False, new_unified_sentence
        
        #print("NEW UNIFIED :",Sentence(new_unified_sentence))
        unified_sentences = unified_sentences + deepcopy([new_unified_sentence])

    #print('OUT OF UNIFY')
    return None, unified_sentences
"""
def remove_duplicates(sentence, op):
    #print("DUPLICATE SENTENCE :",Sentence(sentence))
    
    sentence = set(deepcopy(sentence))
    sentence = list(sentence)
    #print("DUPLICATE SENTENCE :",Sentence(sentence))
    for i,predicate in enumerate(sentence):
        predicate_subs = [x for x in sentence[i:] if x.kb_key == predicate.resolve_search and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        #predicate_subs = predicate_subs + [x for x in sentence[i:] if x.kb_key == predicate.kb_key and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        
        if predicate_subs != [] and op =="AND":
            sentence.remove(predicate)
            
        elif predicate_subs != [] and op =="OR":
            return []
#            new_sentence = new_sentence + [predicate]
        #print("PREDICATE SUB :",Sentence(predicate_subs))     
        for sub in predicate_subs:
            sentence.remove(sub)
            
    #print("PREDICATE SENTENCE :",Sentence(sentence))   
    return sentence
"""
def remove_duplicates(sentence,predicate, op):
    #print("DUPLICATE SENTENCE :",op,Sentence(sentence))
    new_sentence = []
    sentence = set(deepcopy(sentence))
    sentence = list(sentence)

    #print("PREDICATE ",predicate)
    #print("DUPLICATE SENTENCE :",Sentence(sentence))
    if op =="AND":
        predicate = deepcopy(predicate[0])
        predicate_subs = [x for x in sentence if x.kb_key == predicate.resolve_search and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        #predicate_subs = predicate_subs + [x for x in sentence[i:] if x.kb_key == predicate.kb_key and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        
        if predicate_subs != [] and op =="AND":
            sentence.remove(predicate)
            
        for sub in predicate_subs:
            sentence.remove(sub)
            
    #print("PREDICATE SENTENCE :",Sentence(sentence)) 
    #print("PREDICATE NEW SENTENCE :",Sentence(new_sentence)) 
        return sentence

    for i,predicate in enumerate(sentence):
        predicate_subs = [x for x in sentence if x.kb_key == predicate.resolve_search and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        #predicate_subs = predicate_subs + [x for x in sentence[i:] if x.kb_key == predicate.kb_key and ",".join(x.arguments) == ",".join(predicate.arguments)] 
        
        if predicate_subs != [] and op =="OR":
            return []
#            new_sentence = new_sentence + [predicate]
        #print("PREDICATE SUB :",Sentence(predicate_subs)) 
        
        if predicate_subs == []:
            new_sentence = new_sentence + [predicate]
            
    #print("PREDICATE SENTENCE :",Sentence(sentence)) 
    #print("PREDICATE NEW SENTENCE :",Sentence(new_sentence)) 
    return sentence

def resolve(sentence_one, sentence_two):
    #combine sentence one and two
    resolved = []
    
    #print("SENTENCE ONE :",Sentence(sentence_one))
    #print("SENTENCE TWO :",Sentence(sentence_two))
    complete_sentences = [deepcopy(sentence_one)]
    for predicate_one in sentence_one:
        for complete_sentence in complete_sentences:
            unified_bool, unified_sentences = unify(predicate_one, sentence_two,complete_sentence)
        complete_sentence = unified_sentences
        resolved = resolved + deepcopy(unified_sentences)
        
        #for unified_sentence in unified_sentences:
        #    print("NEW RESOLVED IN RESOLVE:",Sentence(unified_sentence))
    
        if unified_bool == True:
            return unified_bool, resolved
        
        if unified_bool == False:
            #print("SENTENCE ONE :",Sentence(sentence_one))
            #print("SENTENCE TWO :",Sentence(sentence_two))
            return unified_bool, resolved
    
    #print("UNIFIED :",list(map(str,list(map(Sentence, resolved)))))    
    #major_sentence = []    
    #for x in resolved:
    #    major_sentence = major_sentence + x
    
    #print("MAJOR :",Sentence(major_sentence))
    #major_sentence = major_sentence + sentence_one
    #major_sentence = remove_duplicates(major_sentence)
    
    #print("MAJOR :",Sentence(major_sentence))
    """
    new_sentences = []
    resolved = set(map(Sentence,resolved))
    resolved = [x.predicate_list for x in resolved]

    implication = False
    #print(len(resolved))

    for x in resolved:
        implication = len([y.negative for y in x if y.negative == 1])>0
        negative_count = len([y.negative for y in x if y.negative == -1])
        #print("IMPLICATION :",implication)
        if implication:
            new_sentences = new_sentences + [x]
        elif negative_count > 1:
            for y in x:
                y.update_negation(1)
                new_sentences = new_sentences + [[y]]
        else:
            new_sentences = resolved
    """
    new_sentences = resolved
    return unified_bool, new_sentences

def resolve_with_statements(statement, kb):
    resolve_with_statements_list = []
    new_list = []
    for term in statement:
        for argument in term.arguments:
            if term.resolve_search in kb.keys() and argument in kb[term.resolve_search].keys():
                resolve_with_statements_list = resolve_with_statements_list + kb[term.resolve_search][argument] 
        if term.resolve_search in kb.keys() and resolve_with_statements_list == []:
            for x,val in kb[term.resolve_search].items():
                resolve_with_statements_list = resolve_with_statements_list + val
                
    resolve_with_statements_list = set(map(Sentence,resolve_with_statements_list))
    #print("RESOLVE : ",resolve_with_statements_list)
    #print("RESOLVE STATEMENTS :","|".join(list(map(str,resolve_with_statements_list))))
    
    resolve_with_statements_list = [x.predicate_list for x in resolve_with_statements_list] 
    resolve_with_statements_list.sort(key = lambda x:len(x))
    return resolve_with_statements_list

def prove(query, kb_set, kb_map):
    print("QUERY : ",query)
    kb_set_2 = set([])
    kb_set = deepcopy(kb_set)
    #print("\n".join(map(str,kb_set)))
    kb_map = deepcopy(kb_map)
    
    resolve_with_statements_list = []
    resolve_knowledge_base = set([])
    history_map = {}
    #query = Sentence(query)
    kb_set_2.add(query)
    kb_set.add(query)
    kb_map = add_to_kb(query.predicate_list, kb_map)
    history_map = {}    
    
    while True:
        resolve_with_statements_list = []
        resolve_knowledge_base = set([])

        for sentence_one in kb_set_2:
            #print("SENTENCE ONE ONE ",sentence_one)
            resolve_with_statements_list = resolve_with_statements(sentence_one.predicate_list,kb_map)
            for sentence_two in resolve_with_statements_list:                           
                sentence_two = Sentence(sentence_two)
                
                #print("SENTENCE ONE ",sentence_one)
                #print("SENTENCE TWO ",sentence_two)
                #check if two statements have been already resolved
                if sentence_one.sentence == sentence_two.sentence:
                    continue
                
                if sentence_two.sentence in history_map.keys():
                    if sentence_one.sentence in history_map[sentence_two.sentence]:
                        #print("SKIP")
                        continue 
                    else:
                        history_map[sentence_two.sentence] = history_map[sentence_two.sentence] + [sentence_one.sentence]
                        #print("HISTORY MAP : ",history_map[sentence_two.sentence])

                elif sentence_one.sentence in history_map.keys():
                    if sentence_two.sentence in history_map[sentence_one.sentence]:
                        #print("SKIP")
                        continue 
                    else:
                        history_map[sentence_one.sentence] = history_map[sentence_one.sentence] + [sentence_two.sentence]
                        #print("HISTORY MAP : ",history_map[sentence_one.sentence])
                else:
                    history_map[sentence_one.sentence] = [sentence_two.sentence]                
                
                #print("SENTENCE ONE ",sentence_one)
                #print("SENTENCE TWO ",sentence_two)
                #print("HISTORY MAP : ",history_map[sentence_two.sentence])
                #print("HISTORY MAP : ",history_map[sentence_one.sentence])
                boolean, resolved = resolve(sentence_one.predicate_list, sentence_two.predicate_list)
                #print("\n".join(map(str,kb_set)))
                #return 0
                if boolean == True:
                    print("Contradiction")
                    return True
                
                if boolean == False:
                    print("True")
                    print("SENTENCE ONE ",sentence_one)
                    print("SENTENCE TWO ",sentence_two)
                    return False
                #print("RESOLVED UNIFIED :",list(map(str,resolved)))
                #print("RESOLVED : ",end="")
                for resolved_sentence in resolved:
                    #for res in resolved_sentence:
                    #    print("SENTENCE KEY :",str(res),res.kb_key)
                    resolved_sentence = Sentence(resolved_sentence)
                    #print(resolved_sentence,end='|')
                    resolve_knowledge_base.add(resolved_sentence)
                #print()
                

        
        if resolve_knowledge_base.issubset(kb_set):
            print("Subset")
            return False
        
        resolve_knowledge_base = resolve_knowledge_base.difference(kb_set)
        
        for resolved_sentence in resolve_knowledge_base:
            kb_map = add_to_kb(resolved_sentence.predicate_list, kb_map)
            
        #print("KNOWLEDGE KB : ",end="")
        #for key in kb_map.keys():
        #    print(key,"|".join(list(map(str,list(map(Sentence,kb_map[key]))))))        
            
        #resolve_knowledge_base = list(resolve_knowledge_base)
        #resolve_knowledge_base.sort(key = lambda x: len(x.predicate_list))
        #resolve_knowledge_base = set(resolve_knowledge_base)
        
        #print("RESOLVED KNOWLEDGE BASE: ","\n".join(map(str,resolve_knowledge_base)))
        
        kb_set_2 = deepcopy(resolve_knowledge_base)
        #print("KNOWLEDGE KB : ","\n".join(map(str,kb_set_2)))
        #kb_set_2 = kb_set_2.union(resolve_knowledge_base)    
        kb_set = kb_set.union(resolve_knowledge_base)
        #print("HISTORY MAP : ",history_map)
        #print("RESOLVE KB : ","\n".join(map(str,resolve_knowledge_base)))
        #print("KNOWLEDGE KB : ","\n".join(map(str,kb_set)))
        #return 0
    return False    
"""
def add_to_kb(sentence, knowledge_base):
    for single_predicate in sentence:
        #print("SINGLE PREDICATE ",single_predicate)
        try:
            knowledge_base[single_predicate.kb_key] = knowledge_base[single_predicate.kb_key] + [sentence]
        except:
            knowledge_base[single_predicate.kb_key] = [sentence]
    return knowledge_base
"""
def add_to_kb(sentence, knowledge_base):
    for single_predicate in sentence:
        #print("SINGLE PREDICATE ",single_predicate)
        for argument in single_predicate.arguments:
            if single_predicate.kb_key not in knowledge_base.keys():
                knowledge_base[single_predicate.kb_key] = {argument : [sentence]}
            elif single_predicate.kb_key in knowledge_base.keys() and argument not in knowledge_base[single_predicate.kb_key].keys():
                knowledge_base[single_predicate.kb_key] = merge_kb(knowledge_base[single_predicate.kb_key], {argument : [sentence]})              
            else:
                knowledge_base[single_predicate.kb_key][argument] = knowledge_base[single_predicate.kb_key][argument] + [sentence]
    return knowledge_base

def create_kb(input_strings):
    knowledge_base = {}
    knowledge_base_set = set([])
    for input_string in input_strings:
        sentence = []
        implication_exists = IMPLICATION in input_string
        implicant = input_string.split(" "+IMPLICATION+" ")
        terms = implicant[0].split(" "+AND+" ")
        for term in terms:
            term_tuple = []
            if (implication_exists):
                if term[0] == NEGATION:
                    term_tuple.append(1) 
                    term = term[1:]
                else:
                    term_tuple.append(-1)
            else:
                if term[0] == NEGATION:
                    term_tuple.append(-1) 
                    term = term[1:]
                else:
                    term_tuple.append(1)
            
            predicate, arguments = term.split("(")
            arguments = arguments[:-1].split(",")
            term_tuple.append(predicate)
            term_tuple.append(arguments)
            
            term_object = Knowlegde_term(term_tuple)
            
            sentence.append(term_object)
        
        if implication_exists: 
            term_tuple = []
            implication_predicate, implication_argument = implicant[1].split("(")
            implication_argument = implication_argument[:-1].split(",")
            if implication_predicate == NEGATION:
                term_tuple.append(-1) 
                implication_predicate = implication_predicate[1:]
            else:
                term_tuple.append(1)   
            
            term_tuple.append(implication_predicate)
            term_tuple.append(implication_argument)
            
            term_object = Knowlegde_term(term_tuple)
            
            sentence.append(term_object)
    
        knowledge_base = add_to_kb(sentence, knowledge_base)
        sentence = Sentence(sentence)
        knowledge_base_set.add(sentence)
        
    return knowledge_base_set, knowledge_base
    

def read_input():
    input_file = open("input.txt",'r')
    no_of_queries = int(input_file.readline().strip())
    queries = [input_file.readline().strip() for i in range(no_of_queries)]
    no_of_statements = int(input_file.readline().strip())
    statements = [input_file.readline().strip() for i in range(no_of_statements)]
    
    return queries, statements
    
def create_queries(queries):
    query_base = []
    for input_string in queries:
        sentence = []

        #print("INPUT STRING ")
        implicant = input_string.split(" "+IMPLICATION+" ")
        terms = implicant[0].split(" "+AND+" ")
        #print("TERMS : ",terms)
        for term in terms:
            term_tuple = []
            if term[0] == NEGATION:
                term_tuple.append(1) 
                term = term[1:]
            else:
                term_tuple.append(-1)
            
            predicate, arguments = term.split("(")
            arguments = arguments[:-1].split(",")
            term_tuple.append(predicate)
            term_tuple.append(arguments)
            
            term_object = Knowlegde_term(term_tuple)
            
            sentence.append(term_object)
        
        sentence = Sentence(sentence)
        query_base = query_base + [sentence]

    return query_base

#sys.stdout = open("test.txt", "w")
queries , input_strings = read_input()   
 
knowledge_base_set, knowledge_base = create_kb(input_strings)   

#for x,val in knowledge_base.items():
#    print("KEY :",x)
#    for arg,val_arg in val.items():
#        print("ARG :",arg)
#        print(list(map(str,list(map(Sentence,val_arg)))))
    #print(val)

queries = create_queries(queries)

#kb_list = list(knowledge_base_set)
#resolve(kb_list[1].predicate_list,kb_list[0].predicate_list)

output_file = open("output.txt","w")
for query in queries:
    value = prove(query,knowledge_base_set, knowledge_base)
    output_file.write(str(value).upper()+"\n")
    print("RESULT :",str(value).upper())

output_file.close()
#sys.stdout.close()