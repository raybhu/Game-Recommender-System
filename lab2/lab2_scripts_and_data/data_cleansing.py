# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:24:23 2019

"""
import json
import re

with open('example.json', 'r', encoding='utf-8') as f:
    x = json.load(f)
    output_text = ''
    for item in x:
        if item['caption'] is not None:
            # print('created_time: %s' % item['caption']['created_time'])
            # print('Caption: %s' % item['caption']['text'])
            
            context = item['caption']['text']
            # remove hyperlinks
            context = re.sub('http\S+', ' ', context)
            # remove punctuation, but keep space for english words splitting
            context = re.sub('[;:.,!?\-/+^\'_$%*()`~\"@#&={}\[\]|\\\\<>]', ' ', context)
            # Extract Traditional Chinese Characters
            # context = re.sub('[^\u4E00-\u9FA5]', ' ', context)
            # Extract English Characters
            context = re.sub('[^A-Za-z\s]', ' ', context)
            print(context)
            # Remove stopwords
            stopwords = ('a', 'an', 'the', 'he', 'she', 'it')
            if stopwords is not None:
                context = context.lower()  # Handle Uppercase and lowercase
                tokens = context.split()
                tokens = [w for w in tokens if w not in stopwords]
                context = ' '.join(tokens)
                # print(context)
            
            output_text += context + '\n'
    with open('result.txt', 'w') as text_file:
        text_file.write(output_text)
