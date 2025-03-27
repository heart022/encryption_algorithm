import random
# made my own encryption method :)
# (i am very proud of this and this is my biggest coding project yet)

# precondition: only encrypts letters and basic symbols (such as , . ? ! etc.)
# so heres my logic:
# im gonna first assign each letter to its final position counterpart
# ex) a -> z
# ex) b -> y
# ex) c -> x etc.
# (not modifying symbols or spaces)

# i am then going to split the string by spaces and reverse the resulting list order

# then i'm going to put the position of the letter right next to the letter (to the right)
# but use consecutive prime numbers in order to denote the respective position of the letter in the word
# i will then shuffle the order of the letters in each word randomly (will do this before the prime number thing)

# Note: for numbers, i will use this symbol representation on the keyboard as a substitute( <@#$%^&*() ) <- the following symbols correspond to digits 0-9

# then the encrypted text should look absolutely insane
# and (most importantly), not human readable :D

def encrypt(text_file: str) -> str:
  # first we do the funky letter shift (& account for numbers)
  symbols = ['<', '@', '#', '$', '%', '^', '&', '*', '(', ')']
  encrypted_text = ""
  for char in text_file:
    if char.isalpha():
      if char.upper() == char:
        encrypted_text += chr(155-ord(char))
      elif char.lower() == char:
        encrypted_text += chr(219-ord(char))
    elif char.isdigit(): # digit check (using symbols list)
      index = int(char)
      symbol = symbols[index]
      encrypted_text += symbol
    else:
      encrypted_text += char # don't worry about symbols

  # then we do the split stuff
  # not exactly the most efficient way to do it, but it should work
  final_text = ""
  encrypted_list = encrypted_text.split(" ")[::-1] # reverse the list
  for count, word in enumerate(encrypted_list):
    list_of_letters = []

    for i, char in enumerate(word):
      if not char.isalpha():
        list_of_letters.append(char)
      else:
        list_of_letters.append([str(prime_number(i+1)), char]) # associate prime number representation of index w/ char
        # list of lists (2d array basically)

    scrambled_letters = scrambler(list_of_letters) # scrambles letters, does not touch symbols (intentional)
    for i, elements in enumerate(scrambled_letters):
      scrambled_letters[i] = "".join(elements) # removes the nested lists and turns it into simple list of strings
    encrypted_list[count] = "".join(scrambled_letters) # goes from list -> string for each word

  return " ".join(encrypted_list) # add back the spaces and the text is successfully encrypted!

def decrypt(encrypted_text: str) -> str:
    symbols = ['<', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    words = encrypted_text.split(" ")[::-1] # reverse the word order
    decrypted_words = [] # list of decrypted words go here

    for word in words:
        # each segment is either:
        #  - A letter segment: a sequence of digits (the prime number) followed by one letter.
        #  - A non-letter segment: a single character
        segments = []
        i = 0
        while i < len(word):
            if word[i].isdigit():
                num_str = ""
                # captures the whole prime num while
                while i < len(word) and word[i].isdigit():
                    num_str += word[i]
                    i += 1
                if i < len(word):
                    # next character must be the encrypted letter
                    letter = word[i]
                    i += 1
                    # mark True for letter segment
                    segments.append((int(num_str), letter, True))
                else:
                    # in case the number runs to the end (should not happen normally)
                    segments.append((None, num_str, False))
            else:
                # non-letter characters (punctuation/symbols) remain as-is
                segments.append((None, word[i], False))
                i += 1

        # Unscramble the letter segments using their prime numbers

        # extract the indices of segments that are letter segments
        letter_positions = [j for j, seg in enumerate(segments) if seg[2] == True]
        # extract those letter segments
        letter_segments = [segments[j] for j in letter_positions]
        # sort letter_segments by prime num
        sorted_letter_segments = sorted(letter_segments, key=lambda seg: seg[0])
        # replace the letter segments in the original positions with the sorted (unscrambled) ones
        for pos, seg in zip(letter_positions, sorted_letter_segments):
            enc_letter = seg[1]
            if enc_letter.isalpha():
                if enc_letter.upper() == enc_letter:
                    orig_letter = chr(155 - ord(enc_letter))
                else:
                    orig_letter = chr(219 - ord(enc_letter))
            else:
                orig_letter = enc_letter
            segments[pos] = orig_letter

        # process non-letter segments: convert symbols back to digits if necessary
        for j, seg in enumerate(segments):

            if not isinstance(seg, str): # if the segment is still a tuple, it is non-letter
                char = seg[1]
                if char in symbols:
                    segments[j] = str(symbols.index(char))
                else:
                    segments[j] = char

        # reassemble the unscrambled word
        decrypted_words.append("".join(segments))
    # put back together entire text
    return " ".join(decrypted_words)


# helper functions down here (had to do excessive searching to figure out how to do some of these functions)

def is_prime(n): # thanks internet
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# what i want to do here: as n increases consecutively, the function prime_number should
# consecutively generate prime numbers (but should also be flexible)

def prime_number(n):
  # start from 2
  cache=[2] # so this function uses a caching system so that its flexible w/ inputs
  if n <= len(cache):
    return cache[n-1]

  num = cache[-1] + 1 # last prime number + 1
  while len(cache) < n:
      if is_prime(num): # brute force method, runs until the function detects that num is prime
          cache.append(num)
      num += 1
  return cache[n-1] # n-1 relates to the index requested of the prime number

def scrambler(listyboy):  # Very specific scrambler function used for encryption
    returnListyboy = list(listyboy)  # Make sure that it does not modify the original list

    # some weird iterating stuff
    alpha_indices = [i for i, char in enumerate(returnListyboy) if "".join(char)[-1].isalpha()]
    # logic of alpha_indices: get indices of the alphabetic characters if char.isalpha
    # but i make sure to do char[-1] due to the prime number indexing thing
    # (since i know that the letter will always be at the end and the prime number comes first)
    alpha_chars = [returnListyboy[i] for i in alpha_indices]

    # Shuffle only the alphabetic characters
    for i in range(len(alpha_chars)):
        randNum = random.randint(0, len(alpha_chars) - 1)  # Get random index
        alpha_chars[i], alpha_chars[randNum] = alpha_chars[randNum], alpha_chars[i]  # a cool pythonic way of swapping stuff 

    # Put shuffled alphabetic characters back in place
    for i, new_char in zip(alpha_indices, alpha_chars):
        returnListyboy[i] = new_char

    return returnListyboy




text = 'This is a test sentence used to test out my custom encryption function! It includes symbols, commas, capital letters, and other COOL stuff. '
encrypted_text = encrypt(text)
print(encrypted_text)

decrypted_text = decrypt(encrypted_text)
print("*" + decrypted_text + "*")
