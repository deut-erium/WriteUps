
ct = [62, 158, 132, 25, 169, 135, 182, 104, 65, 140, 102, 163, 156, 8, 57, 129, 125, 95, 129, 67, 171, 169, 146, 100, 50, 100, 32, 67, 140, 175, 158, 55, 139, 89, 162, 15, 77, 19, 165, 87, 36, 29, 43, 185, 79, 129, 32]

com = ['R', 'D', 'T', 'L', 'F', 'V', 'J', 'I', 'P', 'B', 'T', 'V', 'T', 'S', 'V', 'L', 'S', 'T', 'E', 'R', 'Y', 'T', 'Y', 'R', 'J', 'G', 'T', 'A', 'A', 'N', 'A', 'F', 'G', 'V', 'F', 'C', 'W', 'N', 'L', 282, 'T', 'K', 'R', 260, 'M', 'S', 'J', 274, 'C', 'F', 'R', 288, 'R', 'L', 'O', 278, 'G', 'Y', 'J', 'Y', 'O', 290, 'R', 'V', 'Y', 'S', 'R', 'W', 'B', 278, 280, 262, 'C', 268, 'X', 257, 'Y', 'Y', 'F', 321, 307, 304, 315, 'F', 286, 307, 'G', 'L', 294, 'A', 296, 298, 'V', 264, 266, 268, 267, 'S', 317, 319, 'T', 312, 'J', 'W', 'U', 'F', 'Z', 'Y', 319, 'O', 277, 'F', 'D', 275, 'O', 'B', 259, 'T', 'D', 'J', 'B', 312, 261, 'I', 'A', 308, 310, 356, 'C', 314, 316, 'S', 272, 'C', 'R', 277, 279, 341, 'Z', 367, 356, 'N', 349, 352, 352, 'F', 274, 'V', 322, 286, 'W', 'F', 'O', 306, 'C', 344, 346, 260, 338, 'R', 'S', 380, 309, 'Y', 'D', 'B', 319, 'M', 266, 364, 301, 371, 310, 'O', 'J', 289, 306, 333, 'S', 'E', 287, 306, 343, 295, 297, 260, 280, 338, 'H', 'T', 'N', 313, 421, 'H', 'F', 'X', 'G', 'J', 'H', 'I', 301, 'D', 259, 'G', 334, 282, 353, 345, 278, 274, 'Y', 446, 316, 'J', 'S', 467, 277, 338, 331, 433, 306, 396, 411, 'K', 'N', 'W', 385, 452, 'S', 257, 345, 'G', 'C', 328, 'S', 330, 472, 334, 406, 487, 'V', 'V', 423, 394, 278, 'D', 'F', 315, 277, 494, 389, 342, 389, 319, 469, 363, 414, 257, 259, 262, 396, 398, 268, 'H', 429, 289, 417, 310, 423, 496, 413, 'O', 426, 309, 258, 439, 'N', 306, 257, 'G', 'N', 'Z', 266, 526, 318, 340, 403, 342, 537, 421, 260, 289, 435, 272, 380, 513, 441, 'I', 338, 267, 501, 517, 'S', 313, 'T', 'M', 'M', 'F', 268, 306, 375, 558, 339, 260, 'Z', 'J', 562, 'V', 537, 353, 'I', 'B', 'A', 501, 266, 'B', 353, 501, 377, 262, 338, 'W', 321, 418, 459, 496, 585, 316, 389, 'I', 'I', 334, 287, 500, 258, 552, 338, 557, 'L', 'R', 435, 408, 377, 'T', 481, 324, 338, 508, 320, 322, 324, 392, 592, 395, 332, 334, 432, 316, 478, 'N', 542, 499, 316, 474, 621, 459, 'T', 'Z', 'O', 423, 558, 618, 624, 337, 334, 368, 590, 338, 373, 375, 357, 'I', 505, 437, 262, 497, 632, 502, 256, 305, 312, 365, 'Y', 635, 313, 553, 623, 531, 586, 588, 310, 590, 378, 512, 600, 319, 339, 'A', 'V', 421, 429, 'H', 629, 'S', 481, 315, 483, 485, 383, 489, 'X', 318, 613, 321, 323, 333, 384, 'M', 278, 537, 578, 563, 674, 582, 598, 542, 'I', 469, 257, 319, 301, 452, 501, 269, 519, 597, 338, 682, 282, 678, 318, 338, 536, 356, 712, 545, 664, 381, 'Y', 667, 618, 420, 'A', 278, 'M', 286, 557, 256, 670, 313, 320, 652, 375, 332, 593, 329, 678]

def encrypt(text, key):
  return ''.join([ chr((( key[0]*(ord(t) - ord('A')) + key[1] ) % 26) + ord('A')) for t in text.upper().replace(' ', '') ])


def compress(uncompressed):
    _size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = _size
            #print(wc,_size)
            _size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def decompress(compressed):
    decompressed_data=""
    string = ""
    dictionary_size = 256
    next_code=256
    compressed = [ord(i) if isinstance(i,(str)) else i for i in compressed]
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
    for code in compressed:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]
    return decompressed_data,dictionary

decompressed,dictionary = decompress(com)
S = encrypt(decompressed,[9,11])


wordlets = [encrypt(dictionary[256+i],[9,11]) for i in range(len(dictionary)-256)]

import wordninja

#for offset in range(256,max(dictionary)-max(ct)):
#    print()
#    sent = encrypt("".join( dictionary[offset+i] for i in ct),[9,11])
#    print(wordninja.split(sent.lower()))

s = ['images', 'of', 'quasars', 'gravitationally', 'lensed', 'by', 'galaxies', 'provide', 'insight', 'into', 'the', 'distribution', 'of', 'dark', 'matter', 'inside', 'the', 'lensing', 'galaxies', 'quasars', 'are', 'distant', 'objects', 'that', 'emit', 'huge', 'amounts', 'of', 'light', 'and', 'other', 'radiation', 'since', 'many', 'quasars', 'are', 'visible', 'behind', 'galaxies', 'their', 'light', 'must', 'pass', 'through', 'those', 'intervening', 'galaxies', 'on', 'the', 'way', 'to', 'us', 'we', 'know', 'from', 'general', 'relativity', 'theory', 'that', 'the', 'matter', 'in', 'any', 'galaxy', 'both', 'normal', 'and', 'dark', 'matter', 'bends', 'space', 'time', 'that', 'bending', 'distorts', 'the', 'image', 'of', 'any', 'quasar', 'whose', 'light', 'passes', 'through', 'a', 'galaxy', 'in', 'many', 'cases', 'this', 'lensing', 'causes', 'several', 'images', 'of', 'the', 'same', 'quasar', 'to', 'appear', 'in', 'our', 'telescopes', 'careful', 'measurements', 'of', 'the', 'brightness', 'of', 'the', 'different', 'images', 'of', 'the', 'quasar', 'give', 'hints', 'about', 'the', 'distribution', 'of', 'the', 'matter', 'in', 'the', 'galaxy', 'since', 'the', 'matter', 'in', 'each', 'part', 'of', 'the', 'galaxy', 'determines', 'the', 'amount', 'of', 'bending', 'of', 'space', 'time', 'in', 'that', 'part', 'of', 'the', 'galaxy', 'the', 'brightness', 'of', 'the', 'images', 'tells', 'us', 'how', 'matter', 'both', 'normal', 'and', 'dark', 'is', 'distributed', 'optical', 'measurements', 'inform', 'astronomers', 'where', 'the', 'normal', 'matter', 'is', 'they', 'can', 'then', 'use', 'the', 'brightness', 'of', 'the', 'multiple', 'quasar', 'images', 'to', 'trace', 'out', 'the', 'dark', 'matter']

dec1 = "_".join([s[i].lower() for i in ct])
s2 = wordninja.split(S.lower())
dec2 = "_".join([s2[i].lower() for i in ct])

print(dec1)
print(dec2)



#images_of_quasars_gravitationally_lensed_by_galaxies_provide_insight_into_the_distribution_of_dark_matter_inside_the_lensing_galaxies_quasars_are_distant_objects_that_emit_huge_amounts_of_light_and_other_radiation_since_many_quasars_are_visible_behind_galaxies_their_light_must_pass_through_those_intervening_galaxies_on_the_way_to_us_we_know_from_general_relativity_theory_that_the_matter_in_any_galaxy_both_normal_and_dark_matter_bends_space_time_that_bending_distorts_the_image_of_any_quasar_whose_light_passes_through_a_galaxy_in_many_cases_this_lensing_causes_several_images_of_the_same_quasar_to_appear_in_our_telescopes_careful_measurements_of_the_brightness_of_the_different_images_of_the_quasar_give_hints_about_the_distribution_of_the_matter_in_the_galaxy_since_the_matter_in_each_part_of_the_galaxy_determines_the_amount_of_bending_of_space_time_in_that_part_of_the_galaxy_the_brightness_of_the_images_tells_us_how_matter_both_normal_and_dark_is_distributed_optical_measurements_inform_astronomers_where_the_normal_matter_is_they_can_then_use_the_brightness_of_the_multiple_quasar_images_to_trace_out_the_dark_matter
