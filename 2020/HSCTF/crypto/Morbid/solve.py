import itertools  # creates iterators for efficient looping

# dictionary of mapping as on
# https://en.wikipedia.org/wiki/Morse_code#Letters,_numbers,_punctuation,_prosigns_for_Morse_code_and_non-English_variants

morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    "\"": ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
    " ": ""
}

revMorse = {}  # Dictionary containing inverse mapping from morse code to its corresponding encoded character
for key, value in morse.items():
    revMorse[value] = key


def decrypt_morse(message):
    """
    Finds the decryption of `message` encoded in morse with individual
    letters separated by x and words separated by xx
    """
    words = message.split('x')
    return "".join(revMorse[word] for word in words)


# Checking the example given in the pdf
print(decrypt_morse("---x-.x-.-.x.xx..-x.--.x---x-.xx.-xx-x..x--x.x"))
ct = "118289293938434193849271464117429364476994241473157664969879696938145689474393647294392739247721652822414624317164228466"

substitution_token = ['..', '.-', '.x', '-.', '--', '-x', 'x.', 'x-', 'xx']
for perm in itertools.permutations(range(9)):
    # Iterate over permutations of substitution_tokens to find the
    # permutations which finds the valid decryption
    ct1 = ct
    for i in range(9):
        ct1 = ct1.replace(str(i + 1), substitution_token[perm[i]])
        # Replace digit in ciphertext with given permutation of substitutions
    try:
        if 'flag' in decrypt_morse(ct1):
            # if the decyrpted strings containts flag, we get our string
            print(decrypt_morse(ct1))
            break
    except KeyError:
        continue

substitution = [substitution_token[i] for i in perm]
frequency = [ct.count(str(digit + 1)) for digit in perm]
for i in range(9):
    print("digit {0}: {1} {2}".format(perm[i]+1, substitution[i], frequency[i]))
