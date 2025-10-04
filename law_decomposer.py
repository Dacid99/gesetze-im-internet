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

def getContentFilepath(file_path):
    file_content_path = "content_" + file_path
    return file_content_path

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

def getLawTopicRegexFromFile():
    lawtopic_regex_text = r""
    with open(os.path.join(os.path.dirname(file_path), "lawtopic_regex")) as regex_file:
        while regex_line := regex_file.readline():
            lawtopic_regex_text += regex_line.strip()

    print("Using regex: " + lawtopic_regex_text)

    lawtopic_regex = re.compile(lawtopic_regex_text, re.IGNORECASE)
    return lawtopic_regex

def regex_deleter(law_text, regex):
    law_text = re.sub(regex, "", law_text)
    return law_text

def regex_matcher(law_text, regex):
    law_match = re.match(regex, law_text)
    if law_match:
        print("law matched")
    return law_match

#main block
start = time.time()

file_path = getFilepathFromCLI()

file_min_path = getMinFilepath(file_path)

file_content_path = getContentFilepath(file_path)

law_regex = getLawRegexFromFile()

lawcontent_regex = getLawContentRegexFromFile()

lawtopic_regex = getLawTopicRegexFromFile()

counter = 0
with open(file_path, "r") as law_file:
    with open(file_min_path, "w") as law_min_file:
        with open(file_content_path, "w") as law_content_file:
            while law_text := law_file.readline():
                counter += 1
                print(counter)
                contentmatch = regex_matcher(law_text, law_regex)
                if contentmatch:
                    law_content_file.write(contentmatch.group(1) + "\n")
                
                law_text = regex_deleter(law_text, law_regex)
                law_text = regex_deleter(law_text, lawtopic_regex)
                law_min_file.write(law_text.strip())
                if len(law_text.strip()) != 0:
                    law_min_file.write("\n")
            
            

end = time.time()

print("done in " + str(end - start) + " after " + str(counter) + " lines")

