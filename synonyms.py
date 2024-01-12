"""
From: Michael Guerzhoy
By: Sarah Zhao and Christine Lee

Note: Download text.txt in order to check for synonyms.
"""

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

# a

def cosine_similarity(vec1, vec2):
    uv = 0
    u_2 = 0
    v_2 = 0
    for key1 in vec1:
        for key2 in vec2:
            if key1 == key2:
                uv += vec1[key1] * vec2[key2]
    u_2 = norm(vec1)
    v_2 = norm(vec2)
    sim = uv / (u_2 * v_2)
    return sim

# b

def build_semantic_descriptors(sentences):
    semantic_descriptor = {}

    for i in range(len(sentences)):
        checked_keys = []
        for word in sentences[i]:
            each_dic = {}
            if word not in checked_keys:
                checked_keys.append(word)

                cur_word = word.lower()
                if cur_word not in semantic_descriptor:
                    for j in range(len(sentences[i])):

                        other_word = sentences[i][j].lower()
                        if other_word != cur_word and sentences[i].index(other_word) == j:
                            if other_word in each_dic:
                                each_dic[other_word] += 1
                            else:
                                each_dic[other_word] = 1
                    semantic_descriptor[cur_word] = each_dic

                else:
                    for j in range(len(sentences[i])):

                        other_word = sentences[i][j].lower()
                        if other_word != cur_word and sentences[i].index(other_word) == j:
                            if other_word in semantic_descriptor[cur_word]:
                                semantic_descriptor[cur_word][other_word] += 1
                            else:
                                semantic_descriptor[cur_word][other_word] = 1

    return semantic_descriptor

# c

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for i in range(len(filenames)):
        text = open(filenames[i], "r", encoding="latin1").read()
        text = text.lower()
        text = text.replace(",", "")
        text = text.replace("-", " ")
        text = text.replace("--", " ")
        text = text.replace(":", "")
        text = text.replace(";", "")
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        text = text.replace('"', "")
        text = text.replace("'", "")
        text_split = text.split(".") # split the text into a list separated by sentences
        for sentence in text_split:
            #cur_sentence.append(sentence.split())
            sentences.append(sentence.split())
        #sentences.append(cur_sentence)
        #print(sentences)
    return build_semantic_descriptors(sentences)

# d

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    word = word.lower()
    max_sim = -1
    max_word = choices[0]
    for i in range(len(choices)):
        cur_choice = choices[i].lower()
        if word in semantic_descriptors and cur_choice in semantic_descriptors:
            cur_sim = similarity_fn(semantic_descriptors[word], semantic_descriptors[cur_choice])
            if cur_sim > max_sim:
                max_sim = cur_sim
                max_word = cur_choice
        else:
            cur_sim = -1
    return max_word

# e

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct_num = 0.0
    text = open(filename, "r", encoding="latin1").read()
    text_list = text.split("\n")
    #print(text_list)
    for i in range(len(text_list)):
        line = text_list[i].split(" ")
        choices = []
        for j in range(2, len(line)):
            choices.append(line[j])
        answer = most_similar_word(line[0], choices, semantic_descriptors, similarity_fn)
        if answer == line[1]:
            correct_num += 1.0
    return (correct_num / float(len(text_list)))*100
