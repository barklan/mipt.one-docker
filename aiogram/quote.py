import vkapi
import markovify
import re
import spacy

import os
vktoken = os.environ.get('VKTOKEN', 'none')
target_id = os.environ.get('TARGER_COMMUNITY_ID', 'none')


def cleaner(posts):
    cleaned_posts = posts.copy()

    '''
    Remove non-quote posts (usually long posts) and Dialog qoutes:
    'П: Здравствуйте, вы меня слышите? \nС: Да\nП: Жаль. Значит придётся провести семинар. \n\n#Тумайкин_mipt'
    '''

    for post in cleaned_posts:
        if (len(post) > 300):
            cleaned_posts.remove(post)

    # for post in cleaned_posts:
    #     if (':' in post):
    #         cleaned_posts.remove(post)


    '''
    TODO
    Ideal qoute (to split by '#', select first, remove newline characters):
    'Это нельзя не решить, это статья уже\n\n#Бурмистров_mipt'
    '''
    for i in range(len(cleaned_posts)):
        segmentlist = list(map(str, cleaned_posts[i].split('#')))
        post = segmentlist[0]
        post = post[:-1]
        cleaned_posts[i] = post


    for i in range(len(cleaned_posts)):
        try:
            if cleaned_posts[i][-1] == '.' or cleaned_posts[i][-1] == '!' or cleaned_posts[i][-1] == '?' or cleaned_posts[i][-1] == '*':
                cleaned_posts[i] = cleaned_posts[i] + '\n'
        except:
            continue


    return cleaned_posts

        
def write_list_to_file(posts):

    '''
    Writes list of strings into file - each string on it's own line
    to subsequently use markovify.NewlineText class instead of markovify.Text

    TODO
    Need to make a permanent file to add quotes to
    and write a function that adds to this file only non-existent quotes form newly got ones
    '''

    with open('corpus.txt', 'w', encoding='utf8') as file:
        file.writelines(posts)


def fit_model():
    
    posts = vkapi.get_wall_posts(vktoken, target_id)
    posts = cleaner(posts)
    write_list_to_file(posts)
    
    # Get raw text as string.
    with open("corpus.txt", encoding='utf8') as file:
        text = file.read()

    # Build the model.
    # text_model = markovify.Text(text, state_size=2)
    
    nlp = spacy.load("en_core_web_sm")

    # class POSifiedText(markovify.Text):
    #     def word_split(self, sentence):
    #         return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    #     def word_join(self, words):
    #         sentence = " ".join(word.split("::")[0] for word in words)
    #         return sentence


    # text_model = POSifiedText(text, state_size=2)
    text_model = markovify.NewlineText(text, state_size=2)

    return text_model


def get_quote(model):
    lng = 65
    q = model.make_short_sentence(lng)
    while q is None :
        q = model.make_short_sentence(lng)

    while len(q) < 15:
        q = model.make_short_sentence(lng)

    if q[0] == '.':
        q = q[1:]

    if q[-1:-2] == '..':
        q = q[:-1]
    return q

