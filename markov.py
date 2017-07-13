"""Generate Markov text from text files."""
import os
#import sys
import twitter
from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
 # body = ""

 #    for filename in filenames:
 #        text_file = open(filename)
 #        body = body + text_file.read()
 #        text_file.close()

    #return body
    # your code goes here
    contents = open(file_path).read()
    text = contents.split()
    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    # your code goes here
    # iterating the string to get tuples to be set as keys and the following word
    # to be set at its value.
    for i in range(len(text_string) - 2):
        key1 = (text_string[i], text_string[i + 1])
        value1 = i + 2
        # if the tuple key is not in dictionary, add key, value
        if key1 not in chains:
            chains[key1] = [text_string[value1]]
        # if in dictionary, append to value list
        else:
            chains[key1].append(text_string[value1])
    # grab last two words in filestring ane make = to 1 tuple (-2, -1): {[None]}
    last_key = (text_string[-2], text_string[-1])
    # if in dictionary, append
    if last_key in chains:
        chains[last_key].append(None)
    # if not, create
    else:
        chains[last_key] = [None]
    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    # your code goes here
    # pull random word from dictionary, add to list
    words.extend(choice(chains.keys()))
    # access tuple, find value (rand choose), add to list

    while True:
        # key = (words[-2], words[-1]))
        # possible_next = chains[key]
        # next_word = chosie(possible_next)
        next_word = choice(chains[(words[-2], words[-1])])
        if next_word is None:
            break
        elif (len(" ".join(words) + " " + next_word) > 140):
            break
                                # and (
                                # words[-1][-1] == "." or
                                # words[-1][-1] == "?" or
                                # words[-1][-1] == "!" or
                                # words[-1][-1] == "\"" or
                                # words[-1][-1] == ")" or
                                # words[-1][-1] == "*")):
        else:
            words.append(next_word)
    return " ".join(words)
    # make (y, z)
    # search dictionary for y, z
    # repeat until reach none.
    # change list into string


def tweet(chains):
  # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    # Note: you must run `source secrets.sh` before running
    # this file to set required environmental variables.

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure
    # they're correct
    print api.VerifyCredentials()

    # # Send a tweet
    # random_tweet = make_text(chains)
    status = api.PostUpdate(chains)
    print status.text

    # while in loop, if not q, stay in loop of asking for status + printing text
    # when q is entered, break
    #random_tweet = make_text(chains)

    while True:
        # make some funny text and print it out to the user, saying "You tweeted this!"
        tweet_again = raw_input('Enter to tweet again? [q to quit] >')
        if tweet_again == "q":
            break
        else:
            print random_tweet





# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt

input_path = "brothers-grim.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

tweet(random_text)
