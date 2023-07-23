#####################################################################
#                        REGEX EXPLANATION                          #
# ----------------------------------------------------------------- #
# [0-9]+: This part of the pattern matches one or more digits (0 to #
#        9). The square brackets [ ] denote a character class,      #
#        which means any digit within the range 0 to 9 will be      #
#        matched. The + quantifier specifies that there must be     #
#        one or more occurrences of digits.                        #
#                                                                 #
# (?:[,.][0-9]+)?: This is a non-capturing group in the regex      #
#                  pattern. The non-capturing group is denoted by   #
#                  (?: ), and it allows us to group parts of the    #
#                  pattern without capturing the matched text.     #
#                  Here's what this part means:                    #
#                                                                 #
# [,.]: This part matches either a comma , or a period .. The      #
#        square brackets [ ] define a character class containing   #
#        a comma and a period, which means either of these         #
#        characters will be matched.                              #
#                                                                 #
# [0-9]+: This part matches one or more digits (0 to 9), just like #
#         the previous [0-9]+ part.                               #
#                                                                 #
# ?: The question mark ? is a quantifier that makes the entire     #
#     non-capturing group optional. It means the pattern inside    #
#     the group (comma/period followed by digits) may occur        #
#     zero or one time.                                           #
#                                                                 #
#####################################################################

#####################################################################
#                           REGEX EXPLANATION                       #
# ----------------------------------------------------------------- #
# r: This prefix before the regular expression string indicates     #
#    that it's a raw string. Raw strings treat backslashes as       #
#    literal characters, which is often useful for writing          #
#    regular expressions because backslashes are commonly used.     #
# def: This part of the regular expression matches the literal      #
#    string "def". It's looking for the Python keyword used to      #
#    define functions.                                              #
# \s+: The \s is a special character that matches any whitespace    #
#    character (spaces, tabs, newlines, etc.). The + quantifier     #
#    means that it should match one or more occurrences of          #
#    whitespace.                                                    #
# ([\w_]+): The parentheses ( and ) create a capturing group,       #
#    which allows us to extract the content that matches this       #
#    part of the regular expression. Inside the capturing group,    #
#    [\w_]+ matches one or more word characters or underscores.     #
#    \w is a shorthand character class for alphanumeric             #
#    characters and underscores. The + quantifier means it should   #
#    match one or more occurrences.                                 #
# \s*: This part matches zero or more whitespace characters. The    #
#    * quantifier means it should match zero or more occurrences.   #
# \(: This part matches the literal open parenthesis "(" character. #
#    Since parentheses have special meanings in regular             #
#    expressions, we need to escape it with a backslash \ to match  #
#    the literal character.                                         #
#####################################################################
