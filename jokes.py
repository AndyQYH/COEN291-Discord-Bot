import openai
import markovify
import os
import random
import praw
from dotenv import load_dotenv

load_dotenv()


def get_jokes_raw(file = 'all_jokes.txt', path = "jokes/"):
    ### LOADING JOKES INTO LIST
    jokeList = []
    full_path = file
    if path != "":
        full_path = path + '/' + file
    with open(full_path,'r', encoding='utf-8') as originals:
        for line in originals.readlines():
            try:
                jokeList.append(line)
            except:
                pass
            
    return jokeList
        
        
### FUNCTIONS TO CLEAN UP JOKES
def replace_special_characters(jokeList):
    tmp_jokeList = []
    for joke in jokeList:
        tmp_jokeList.append(joke.replace('\r',' ').replace('\n', ' ').replace("'","").replace("|", ""))
    return tmp_jokeList

def lowercase(jokeList):
    tmp_jokeList = []
    for joke in jokeList:
        tmp_jokeList.append(joke.lower())
    return tmp_jokeList

def remove_long_jokes(jokeList, max_len):
    tmp_jokeList = []
    for joke in jokeList:
        if len(joke) <= max_len:
            tmp_jokeList.append(joke)
    return tmp_jokeList

def replace(jokeList, bef, aft):
    tmp_jokeList = []
    for joke in jokeList:
        tmp_jokeList.append(joke.replace(bef,aft))
    return tmp_jokeList

def remove_empty(jokeList):
    tmp_jokeList = []
    for joke in jokeList:
        if len(joke) > 0:
            tmp_jokeList.append(joke)
    return tmp_jokeList

def joke_preprocess(jokeList):
    ### PREPROCESSING
    tmp_jokeList = []
    for j in jokeList:
        joke = j
        while "..." in joke:
            joke = joke.replace("...","..")
        tmp_jokeList.append(joke)
    jokeList = tmp_jokeList
    jokeList = replace(jokeList, "."," DOT ")
    jokeList = replace(jokeList, "?"," QUESTIONMARK ")
    jokeList = replace_special_characters(jokeList)
    jokeList = lowercase(jokeList)
    jokeList = remove_long_jokes(jokeList, 200)
    jokeList = remove_empty(jokeList)
    
    return jokeList

def joke_generate(jokeList):
    ### Generate some original jokes
    text_model = markovify.NewlineText(jokeList)
    generated_jokes = []
    while len(generated_jokes) <= 100:
        joke = text_model.make_sentence()
        #print(joke)
        if not joke == None and joke not in generated_jokes:
            clean_joke = joke.replace(" dot",".").replace(" questionmark", "?")
            #print(clean_joke)
            #print("\n")
            generated_jokes.append(clean_joke)
            
    return generated_jokes

def joke_normalize_GPT(generated_jokes, genre, model_name = "gpt-3.5-turbo", prompt = ""):
    openai.api_key = os.getenv('OPENAI_API')

    messages = [ {"role": "system", "content": "You are an intelligent assistant and funny."} ]
    random_joke = generated_jokes[random.randint(0,len(generated_jokes))]
    print(random_joke)
    print("\n")

    message = "Here is a joke: {joke} .\n Edit this joke to be funnier. The rewritten joke must have a similar number of words to the original joke. The rewritten joke must also have a similar punchline to the original joke. It is okay to remove sentences if they do not make sense to the joke. If there is no punchline, please add an appropriate punchline. The response should only include the original joke and the rewritten joke. \n".format(joke = random_joke)
    #message = "Here is a joke: {joke} .\n Rewrite this joke to be funnier. The rewritten joke must to have a similar number of words to the original joke and should be a {genre}. The response have the original joke and the rewritten joke. \n".format(joke = random_joke, genre = genre)
    if prompt != "":
        #message = prompt.format(joke = random_joke)
        return random_joke
    print(message)
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model= model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    return reply

def joke_prompitize_GPT(generated_joke, model_name = "gpt-3.5-turbo", source = ""):
    openai.api_key = os.getenv('OPENAI_API')

    messages = [ {"role": "system", "content": "You are an intelligent assistant and funny."} ]
    
    if source == "Stability.ai Stable Diffusion SD XL":
        message = "\nBreak the joke {joke} down into a prompt for AI Art Generation.\n\n the prompt should include keywords such as\"cartoon style, simplistic design, 2k\". Make sure the prompt captures the details in the joke. Also make sure the prompt excludes bad anatomy, blurry layout, extra arms, extra fingers, poorly drawn hands, disfigured shape, tiling, deformation, and mutation in the art. \n\n The response should be the prompt only.".format(joke = generated_joke)
    else:
        message = "\nBreak the joke {joke} down into a prompt for AI Art Generation. \n\n The prompt should include keywords such as\"cartoon style, simplistic design\". Make sure the prompt captures the main subjects in the joke. \n\n The prompt should be a list of keywords, separated by commas. \n\n The response should be the prompt only".format(joke = generated_joke)
    #message = "\nTurn this joke into a prompt for AI Art Generation on {prompt}: \n\n {joke} \n\n the prompt should include keywords such as\"digital art, beautiful composition, detailed, elaborate, 2k\". Make sure the prompt captures the details in the joke. Also make sure the prompt excludes bad anatomy, blurry layout, extra arms, extra fingers, poorly drawn hands, disfigured shape, tiling, deformation, and mutation in the art. \n\n The response should be the prompt only.".format(joke = generated_joke, prompt = prompt)
    print(message)
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model= model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    return reply

def joke_from_GPT(description, model_name = "gpt-3.5-turbo", prompt = ""):
    openai.api_key = os.getenv('OPENAI_API')

    messages = [ {"role": "system", "content": "You are an intelligent assistant and funny."} ]
    random_joke = description
    print(random_joke)
    print("\n")

    message = "Write a funny joke that is related to {joke}. \n\n The joke should include the word {joke}.\n\nThe length of the joke shold not be too long. \n\n The response should be the joke only. \n".format(joke = random_joke)
    if prompt != "":
        #message = prompt.format(joke = random_joke)
        return random_joke
    print(message)
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model= model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    return reply


def generate_reddit_jokes(subReddit, txtFile):
    # Read-only instance
    reddit_read_only = praw.Reddit(client_id="Z0IvaMFtugE13nmPGSSXCw",         # your client id
                               client_secret="d5jKhTk81kIimY0WO_AapZjPlwWw8Q",      # your client secret
                               user_agent="Joke Parser")        # your user agent
    subreddit = reddit_read_only.subreddit(subReddit)
    jokeList = []
    for post in subreddit.top(limit=20000):  # limit will differ depending on the subreddit
        #print(post.title)
        #print(post.selftext)
        new_joke = post.title + ' ' + post.selftext
        if(len(new_joke) < 100): 
            jokeList.append(new_joke)

    file = open(txtFile,'w')
    for joke in jokeList:
        file.write(joke+"\n")
    file.close()
    return jokeList


    