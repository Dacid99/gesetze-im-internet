import re
import os
import sys
import time

def getFilepathFromCLI():
    try:
        file_path = sys.argv[1]
        print("Reducing file " + file_path)
        return file_path
    except:
        print("CLI argument missing!")
        sys.exit(1)

def getMinFilepath(file_path):
    file_min_path = "min_" + file_path
    return file_min_path

def getLawRegexFromFile():
    law_regex_text = r""
    with open(os.path.join(os.path.dirname(file_path), "law_regex")) as regex_file:
        while regex_line := regex_file.readline():
            law_regex_text += regex_line.strip()

    print("Using regex: " + law_regex_text)

    law_regex = re.compile(law_regex_text, re.IGNORECASE)
    return law_regex

def getLawContentRegexFromFile():
    lawcontent_regex_text = r""
    with open(os.path.join(os.path.dirname(file_path), "lawcontent_regex")) as regex_file:
        while regex_line := regex_file.readline():
            lawcontent_regex_text += regex_line.strip()

    print("Using regex: " + lawcontent_regex_text)

    lawcontent_regex = re.compile(lawcontent_regex_text, re.IGNORECASE)
    return lawcontent_regex

def regex_deleter(law_text, law_regex, lawcontent_regex):
    law_match = re.match(law_regex, law_text)
    if law_match:
        print("law matched")
        lawcontent_match = re.match(lawcontent_regex, str(law_match.group(1)))
        if lawcontent_match:
            print("lawcontent matched")
            law_text = re.sub(law_regex, "", law_text)
    return law_text


#main block
start = time.time()

file_path = getFilepathFromCLI()

file_min_path = getMinFilepath(file_path)

law_regex = getLawRegexFromFile()

lawcontent_regex = getLawContentRegexFromFile()

counter = 0
with open(file_path, "r") as law_file:
    with open(file_min_path, "w") as law_min_file:
        while law_text := law_file.readline():
            counter += 1
            print(counter)
            law_text = regex_deleter(law_text, law_regex, lawcontent_regex)
            law_min_file.write(law_text.strip())
            if len(law_text.strip()) != 0:
                law_min_file.write("\n")
            

end = time.time()

print("done in " + end - start + " after " + counter + " lines")

