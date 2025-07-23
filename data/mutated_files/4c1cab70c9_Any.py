import itertools
import ujson
import random
from typing import List, Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    with open("zerver/tests/fixtures/config.generate_data.json", "r") as infile:
        config = ujson.load(infile)

    return config

def get_stream_title(gens: Dict[str, Any]) -> str:

    return next(gens["adjectives"]) + " " + next(gens["nouns"]) + " " + \
        next(gens["connectors"]) + " " + next(gens["verbs"]) + " " + \
        next(gens["adverbs"])

def __tmp5(config: Dict[str, Any]) -> Dict[str, Any]:

    results = {}
    cfg = config["gen_fodder"]

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

def parse_file(config, gens: Dict[str, Any], __tmp3: str) -> List[str]:

    # First, load the entire file into a dictionary,
    # then apply our custom filters to it as needed.

    __tmp1 = []  # type: List[str]

    with open(__tmp3, "r") as infile:
        # OUR DATA: we need to separate the person talking and what they say
        __tmp1 = remove_line_breaks(infile)
        __tmp1 = add_flair(__tmp1, gens)

    return __tmp1

def __tmp7(__tmp4: int) :

    # Grab the percentages from the config file
    # create a list that we can consume that will guarantee the distribution
    result = []

    for k, v in config["dist_percentages"].items():
        result.extend([k] * int(v * __tmp4 / 100))

    result.extend(["None"] * (__tmp4 - len(result)))

    random.shuffle(result)
    return result

def add_flair(__tmp1: List[str], gens: Dict[str, Any]) -> List[str]:

    # roll the dice and see what kind of flair we should add, if any
    results = []

    flair = __tmp7(len(__tmp1))

    for i in range(len(__tmp1)):
        key = flair[i]
        if key == "None":
            txt = __tmp1[i]
        elif key == "italic":
            txt = add_md("*", __tmp1[i])
        elif key == "bold":
            txt = add_md("**", __tmp1[i])
        elif key == "strike-thru":
            txt = add_md("~~", __tmp1[i])
        elif key == "quoted":
            txt = ">" + __tmp1[i]
        elif key == "quote-block":
            txt = __tmp1[i] + "\n" + next(gens["quote-blocks"])
        elif key == "inline-code":
            txt = __tmp1[i] + "\n" + next(gens["inline-code"])
        elif key == "code-block":
            txt = __tmp1[i] + "\n" + next(gens["code-blocks"])
        elif key == "math":
            txt = __tmp1[i] + "\n" + next(gens["maths"])
        elif key == "list":
            txt = __tmp1[i] + "\n" + next(gens["lists"])
        elif key == "emoji":
            txt = add_emoji(__tmp1[i], next(gens["emojis"]))
        elif key == "link":
            txt = add_link(__tmp1[i], next(gens["links"]))
        elif key == "picture":
            txt = txt      # TODO: implement pictures

        results.append(txt)

    return results

def add_md(__tmp2: str, __tmp0: str) -> str:

    # mode means: bold, italic, etc.
    # to add a list at the end of a paragraph, * iterm one\n * item two

    # find out how long the line is, then insert the mode before the end

    vals = __tmp0.split()
    start = random.randrange(len(vals))
    end = random.randrange(len(vals) - start) + start
    vals[start] = __tmp2 + vals[start]
    vals[end] = vals[end] + __tmp2

    return " ".join(vals).strip()

def add_emoji(__tmp0: str, emoji: str) -> str:

    vals = __tmp0.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + emoji + " "
    return " ".join(vals)

def add_link(__tmp0: str, link: str) -> str:

    vals = __tmp0.split()
    start = random.randrange(len(vals))

    vals[start] = vals[start] + " " + link + " "

    return " ".join(vals)

def remove_line_breaks(fh: <FILL>) -> List[str]:

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

def __tmp6(__tmp1: List[str], filename: str) -> None:

    with open(filename, "w") as outfile:
        outfile.write(ujson.dumps(__tmp1))

def create_test_data() -> None:

    gens = __tmp5(config)   # returns a dictionary of generators

    __tmp1 = parse_file(config, gens, config["corpus"]["filename"])

    __tmp6(__tmp1, "var/test_messages.json")

config = load_config()  # type: Dict[str, Any]

if __name__ == "__main__":
    create_test_data()  # type: () -> ()
