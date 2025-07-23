from typing import TypeAlias
__typ0 : TypeAlias = "int"
import itertools
import ujson
import random
from typing import List, Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    with open("zerver/tests/fixtures/config.generate_data.json", "r") as infile:
        __tmp10 = ujson.load(infile)

    return __tmp10

def __tmp6(__tmp4: Dict[str, Any]) -> str:

    return next(__tmp4["adjectives"]) + " " + next(__tmp4["nouns"]) + " " + \
        next(__tmp4["connectors"]) + " " + next(__tmp4["verbs"]) + " " + \
        next(__tmp4["adverbs"])

def load_generators(__tmp10: Dict[str, Any]) -> Dict[str, Any]:

    results = {}
    cfg = __tmp10["gen_fodder"]

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

def __tmp11(__tmp10: Dict[str, Any], __tmp4: Dict[str, Any], corpus_file: str) -> List[str]:

    # First, load the entire file into a dictionary,
    # then apply our custom filters to it as needed.

    __tmp2 = []  # type: List[str]

    with open(corpus_file, "r") as infile:
        # OUR DATA: we need to separate the person talking and what they say
        __tmp2 = remove_line_breaks(infile)
        __tmp2 = add_flair(__tmp2, __tmp4)

    return __tmp2

def __tmp13(__tmp8: __typ0) -> List[str]:

    # Grab the percentages from the config file
    # create a list that we can consume that will guarantee the distribution
    result = []

    for k, v in __tmp10["dist_percentages"].items():
        result.extend([k] * __typ0(v * __tmp8 / 100))

    result.extend(["None"] * (__tmp8 - len(result)))

    random.shuffle(result)
    return result

def add_flair(__tmp2, __tmp4: Dict[str, Any]) :

    # roll the dice and see what kind of flair we should add, if any
    results = []

    flair = __tmp13(len(__tmp2))

    for i in range(len(__tmp2)):
        key = flair[i]
        if key == "None":
            txt = __tmp2[i]
        elif key == "italic":
            txt = add_md("*", __tmp2[i])
        elif key == "bold":
            txt = add_md("**", __tmp2[i])
        elif key == "strike-thru":
            txt = add_md("~~", __tmp2[i])
        elif key == "quoted":
            txt = ">" + __tmp2[i]
        elif key == "quote-block":
            txt = __tmp2[i] + "\n" + next(__tmp4["quote-blocks"])
        elif key == "inline-code":
            txt = __tmp2[i] + "\n" + next(__tmp4["inline-code"])
        elif key == "code-block":
            txt = __tmp2[i] + "\n" + next(__tmp4["code-blocks"])
        elif key == "math":
            txt = __tmp2[i] + "\n" + next(__tmp4["maths"])
        elif key == "list":
            txt = __tmp2[i] + "\n" + next(__tmp4["lists"])
        elif key == "emoji":
            txt = __tmp1(__tmp2[i], next(__tmp4["emojis"]))
        elif key == "link":
            txt = __tmp3(__tmp2[i], next(__tmp4["links"]))
        elif key == "picture":
            txt = txt      # TODO: implement pictures

        results.append(txt)

    return results

def add_md(__tmp5: <FILL>, __tmp0: str) -> str:

    # mode means: bold, italic, etc.
    # to add a list at the end of a paragraph, * iterm one\n * item two

    # find out how long the line is, then insert the mode before the end

    vals = __tmp0.split()
    start = random.randrange(len(vals))
    end = random.randrange(len(vals) - start) + start
    vals[start] = __tmp5 + vals[start]
    vals[end] = vals[end] + __tmp5

    return " ".join(vals).strip()

def __tmp1(__tmp0: str, __tmp7: str) -> str:

    vals = __tmp0.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + __tmp7 + " "
    return " ".join(vals)

def __tmp3(__tmp0: str, __tmp12: str) -> str:

    vals = __tmp0.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + __tmp12 + " "

    return " ".join(vals)

def remove_line_breaks(fh: Any) -> List[str]:

    # We're going to remove line breaks from paragraphs
    results = []    # save the dialogs as tuples with (author, dialog)

    para = []   # we'll store the lines here to form a paragraph

    for line in fh:
        __tmp0 = line.strip()
        if __tmp0 != "":
            para.append(__tmp0)
        else:
            if para:
                results.append(" ".join(para))
            # reset the paragraph
            para = []
    if para:
        results.append(" ".join(para))

    return results

def write_file(__tmp2, __tmp9) -> None:

    with open(__tmp9, "w") as outfile:
        outfile.write(ujson.dumps(__tmp2))

def create_test_data() -> None:

    __tmp4 = load_generators(__tmp10)   # returns a dictionary of generators

    __tmp2 = __tmp11(__tmp10, __tmp4, __tmp10["corpus"]["filename"])

    write_file(__tmp2, "var/test_messages.json")

__tmp10 = load_config()  # type: Dict[str, Any]

if __name__ == "__main__":
    create_test_data()  # type: () -> ()
