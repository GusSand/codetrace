import itertools
import ujson
import random
from typing import List, Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    with open("zerver/tests/fixtures/config.generate_data.json", "r") as infile:
        __tmp11 = ujson.load(infile)

    return __tmp11

def __tmp4(__tmp6: Dict[str, Any]) -> str:

    return next(__tmp6["adjectives"]) + " " + next(__tmp6["nouns"]) + " " + \
        next(__tmp6["connectors"]) + " " + next(__tmp6["verbs"]) + " " + \
        next(__tmp6["adverbs"])

def __tmp13(__tmp11: Dict[str, Any]) -> Dict[str, Any]:

    results = {}
    cfg = __tmp11["gen_fodder"]

    results["nouns"] = itertools.cycle(cfg["nouns"])
    results["adjectives"] = itertools.cycle(cfg["adjectives"])
    results["connectors"] = itertools.cycle(cfg["connectors"])
    results["verbs"] = itertools.cycle(cfg["verbs"])
    results["adverbs"] = itertools.cycle(cfg["adverbs"])
    results["emojis"] = itertools.cycle(cfg["emoji"])
    results["links"] = itertools.cycle(cfg["links"])

    results["maths"] = itertools.cycle(cfg["maths"])
    results["inline-code"] = itertools.cycle(cfg["inline-code"])
    results["code-blocks"] = itertools.cycle(cfg["code-blocks"])
    results["quote-blocks"] = itertools.cycle(cfg["quote-blocks"])

    results["lists"] = itertools.cycle(cfg["lists"])

    return results

def parse_file(__tmp11: Dict[str, Any], __tmp6: Dict[str, Any], __tmp8: str) -> List[str]:

    # First, load the entire file into a dictionary,
    # then apply our custom filters to it as needed.

    paragraphs = []  # type: List[str]

    with open(__tmp8, "r") as infile:
        # OUR DATA: we need to separate the person talking and what they say
        paragraphs = remove_line_breaks(infile)
        paragraphs = __tmp3(paragraphs, __tmp6)

    return paragraphs

def __tmp15(length: int) -> List[str]:

    # Grab the percentages from the config file
    # create a list that we can consume that will guarantee the distribution
    result = []

    for k, v in __tmp11["dist_percentages"].items():
        result.extend([k] * int(v * length / 100))

    result.extend(["None"] * (length - len(result)))

    random.shuffle(result)
    return result

def __tmp3(paragraphs: List[str], __tmp6: Dict[str, Any]) -> List[str]:

    # roll the dice and see what kind of flair we should add, if any
    results = []

    flair = __tmp15(len(paragraphs))

    for i in range(len(paragraphs)):
        key = flair[i]
        if key == "None":
            txt = paragraphs[i]
        elif key == "italic":
            txt = __tmp0("*", paragraphs[i])
        elif key == "bold":
            txt = __tmp0("**", paragraphs[i])
        elif key == "strike-thru":
            txt = __tmp0("~~", paragraphs[i])
        elif key == "quoted":
            txt = ">" + paragraphs[i]
        elif key == "quote-block":
            txt = paragraphs[i] + "\n" + next(__tmp6["quote-blocks"])
        elif key == "inline-code":
            txt = paragraphs[i] + "\n" + next(__tmp6["inline-code"])
        elif key == "code-block":
            txt = paragraphs[i] + "\n" + next(__tmp6["code-blocks"])
        elif key == "math":
            txt = paragraphs[i] + "\n" + next(__tmp6["maths"])
        elif key == "list":
            txt = paragraphs[i] + "\n" + next(__tmp6["lists"])
        elif key == "emoji":
            txt = add_emoji(paragraphs[i], next(__tmp6["emojis"]))
        elif key == "link":
            txt = __tmp7(paragraphs[i], next(__tmp6["links"]))
        elif key == "picture":
            txt = txt      # TODO: implement pictures

        results.append(txt)

    return results

def __tmp0(__tmp5: str, __tmp1: str) -> str:

    # mode means: bold, italic, etc.
    # to add a list at the end of a paragraph, * iterm one\n * item two

    # find out how long the line is, then insert the mode before the end

    vals = __tmp1.split()
    start = random.randrange(len(vals))
    end = random.randrange(len(vals) - start) + start
    vals[start] = __tmp5 + vals[start]
    vals[end] = vals[end] + __tmp5

    return " ".join(vals).strip()

def add_emoji(__tmp1, __tmp9: <FILL>) -> str:

    vals = __tmp1.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + __tmp9 + " "
    return " ".join(vals)

def __tmp7(__tmp1: str, __tmp12: str) -> str:

    vals = __tmp1.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + __tmp12 + " "

    return " ".join(vals)

def remove_line_breaks(fh: Any) -> List[str]:

    # We're going to remove line breaks from paragraphs
    results = []    # save the dialogs as tuples with (author, dialog)

    para = []   # we'll store the lines here to form a paragraph

    for line in fh:
        __tmp1 = line.strip()
        if __tmp1 != "":
            para.append(__tmp1)
        else:
            if para:
                results.append(" ".join(para))
            # reset the paragraph
            para = []
    if para:
        results.append(" ".join(para))

    return results

def __tmp14(paragraphs: List[str], __tmp10: str) -> None:

    with open(__tmp10, "w") as outfile:
        outfile.write(ujson.dumps(paragraphs))

def __tmp2() :

    __tmp6 = __tmp13(__tmp11)   # returns a dictionary of generators

    paragraphs = parse_file(__tmp11, __tmp6, __tmp11["corpus"]["filename"])

    __tmp14(paragraphs, "var/test_messages.json")

__tmp11 = load_config()  # type: Dict[str, Any]

if __name__ == "__main__":
    __tmp2()  # type: () -> ()
