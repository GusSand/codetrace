import itertools as it
from codetrace.py_mutator import (
    PyMutator,
    PY_TYPE_ANNOTATIONS_QUERY,
    RETURN_TYPES as PY_RETURN_TYPES,
    PY_IDENTIFIER_QUERY,
    get_toplevel_parent,
    IMPORT_STATEMENT_QUERY,
    DummyTreeSitterNode
)
from codetrace.base_mutator import Mutation, TreeSitterLocation
from codetrace.ts_mutator import TsMutator
import os
from codetrace.parsing_utils import get_captures

CWD = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(CWD, "test_programs")

def read(path: str) -> str:
    with open(path, "r") as fp:
        return fp.read()

def byte_encode(s: str, encoding="utf-8") -> bytes:
    return bytes(s, encoding)

def read_bytes(path: str) -> bytes:
    return byte_encode(read(path))

def test_py_add_aliases():
    mutator = PyMutator()
    code = read(f"{PROG}/before_add_alias.py")
    code = mutator.replace_placeholder(code)
    code_bytes = byte_encode(code)
    output = mutator.add_type_aliases(
        code_bytes, [
            b'__tmp0 : TypeAlias = "TestUserRedirectView"', 
            b'__tmp1 : TypeAlias = "settings.AUTH_USER_MODEL"',
            b'__tmp2 : TypeAlias = "RequestFactory"']
    )
    expected = byte_encode(
        mutator.replace_placeholder(
        read(f"{PROG}/after_add_alias.py")
    ))
    assert output == expected

def test_py_postproc_annotation():
    mutator = PyMutator()
    node = get_captures("def palindrome(s : List[int]):\n\tpass", PY_TYPE_ANNOTATIONS_QUERY, "py", 
                        "annotation")
    assert len(node) == 1
    node = node[0]
    full_annotation = mutator.postprocess_type_annotation(node, target_char=b":", shift_amt=0)
    type_only = mutator.postprocess_type_annotation(node, target_char=b":", shift_amt=1)
    assert type_only.text == b" List[int]"
    assert full_annotation.text == b": List[int]"

def test_py_postproc_return_types():
    mutator = PyMutator()
    prog = """
def palindrome(s : List[int], **kwargs) -> Union[List[Request], Dict]:
    pass
"""
    program = bytes(prog, "utf-8")
    node = get_captures(program, PY_RETURN_TYPES, "py", "id")
    assert len(node) == 1
    node = node[0]
    assert node.text == b"Union[List[Request], Dict]"
    output = mutator.postprocess_return_type(node, program)
    assert output.text == b"-> Union[List[Request], Dict]"

def test_py_rename_vars():
    mutator = PyMutator()

    # testing rename vars
    program = mutator.replace_placeholder(read(f"{PROG}/before_var_rename.py"))
    var_captures = get_captures(program, PY_IDENTIFIER_QUERY, "py", "id")
    var_captures = [v for v in var_captures if b"forces" in v.text]
    var_all_captures,_,_ = mutator.find_all_other_locations_of_captures(
        program, "float", var_captures, [], []
    )
    output, _ = mutator.mutate_captures(
        program,
        [mutator.rename_vars],
        var_rename_captures=var_all_captures,
        type_rename_captures=[],
        remove_captures=[]
    )
    assert len(var_all_captures) == 8
    assert output
    expected = read(f"{PROG}/after_var_rename.py")
    assert output == expected

def test_py_rename_types():
    mutator = PyMutator()

    # testing rename types
    program = mutator.replace_placeholder(read(f"{PROG}/before_type_rename.py"))
    type_captures = get_captures(program, PY_TYPE_ANNOTATIONS_QUERY, "py", "annotation")
    type_captures = [mutator.postprocess_type_annotation(c, b":", 1) 
                     for c in type_captures if b"Derp" in c.text or b"UserProfile" in c.text]
    assert len(type_captures) >= 2
    _,type_all_captures,_ = mutator.find_all_other_locations_of_captures(
        program, "int", [], type_captures, []
    )
    assert len(type_all_captures) >= 2
    import_statements = (b"\n".join([imp.text for imp in
        get_captures(program, IMPORT_STATEMENT_QUERY, "py", "import_statement")]))
    output, muts = mutator.mutate_captures(
        program,
        [mutator.rename_types],
        var_rename_captures=[],
        type_rename_captures=type_all_captures,
        remove_captures=[],
        import_statements=import_statements
    )
    assert any([mutator.needs_alias(c,import_statements=import_statements) for c in type_all_captures])
    derp_rename = [m.byte_replacement.decode("utf-8")
                   for m in muts if b"Derp" in m._text_label][0]
    user_profile_rename = [m.byte_replacement.decode("utf-8")
                           for m in muts if b"UserProfile" in m._text_label][0]
    assert output
    
    expected = read(f"{PROG}/after_type_rename.py").replace("__typ1", "__typ2").replace(
        "__typ0", user_profile_rename).replace("__typ2", derp_rename)
    assert output == expected

    _,output,_ = mutator.find_all_other_locations_of_captures(
        program, "Derp", [], type_all_captures, [])
    # cannot rename fim
    assert not b"Derp" in [o.text for o in output]

def test_py_delete():
    mutator = PyMutator()
    # testing rename vars
    program = mutator.replace_placeholder(read(f"{PROG}/before_delete.py"))
    del_captures = get_captures(program, PY_TYPE_ANNOTATIONS_QUERY, "py", "annotation")
    del_captures = [mutator.postprocess_type_annotation(c, b":", 0) 
                     for c in del_captures if b": str" in c.text]
    assert len(del_captures) > 0
    _,_,delete_captures = mutator.find_all_other_locations_of_captures(
        program, "Realm", [], [], del_captures
    )
    output, _ = mutator.mutate_captures(
        program,
        [mutator.delete_annotations],
        var_rename_captures=[],
        type_rename_captures=[],
        remove_captures=delete_captures
    )
    assert len(delete_captures) > 1
    assert output
    
    expected = read(f"{PROG}/after_delete.py")
    assert output == expected

def test_py_all_muts():
    mutator = PyMutator()
    program = read(f"{PROG}/before_all_muts.py")
    program = mutator.replace_placeholder(program)
    import_statements = (b"\n".join([imp.text for imp in
        get_captures(program, IMPORT_STATEMENT_QUERY, "py", "import_statement")]))

    # delete all UserProfile
    rename_type_muts = [
            mutator.postprocess_type_annotation(n, b":", 1) for n in
            get_captures(program, PY_TYPE_ANNOTATIONS_QUERY, "py", "annotation") if
             b": Addressee" in n.text
        ] + [
            mutator.postprocess_type_annotation(n, b":", 1) for n in
            get_captures(program, PY_TYPE_ANNOTATIONS_QUERY, "py", "annotation") if
             b": str" in n.text
        ]
    
    mutations = mutator.find_all_other_locations_of_captures(
        program,
        "Realm",
        # rename msg_type
        [
            n for n in
            get_captures(program, "((identifier) @id)", "py", "id") if
             b"msg_type" in n.text
        ],
        rename_type_muts,
        [
            mutator.postprocess_type_annotation(n, b":", 0) for n in
            get_captures(program, PY_TYPE_ANNOTATIONS_QUERY, "py", "annotation") if
             b": UserProfile" in n.text
        ]
    )
    output,_ = mutator.mutate_captures(
        program, [mutator.rename_types, mutator.rename_vars, mutator.delete_annotations], *mutations,
        import_statements=import_statements
    )
    # output = mutator.revert_placeholder(output)
    expected = read(f"{PROG}/after_all_muts.py")
    expected_switched = expected.replace("__typ0", "__typ2").replace("__typ1","__typ0").replace(
        "__typ2","__typ1"
    )
    assert output == expected or output == expected_switched

def test_py_is_import():
    mutator = PyMutator()
    # import statement does needs alias
    prog = '''
    from math.hulu import (
	call as p,
    s, t
)
'''
    cap = get_captures(prog, "((identifier) @s)", "py", "s")
    cap = [c for c in cap if c.text == b"p"]
    assert len(cap) == 1
    cap = cap[0]
    assert mutator.is_import_statement(cap)

    prog = '''
    from math.hulu.tru import (
	call.terry as p,
    s, t
)
'''
    cap = get_captures(prog, "((identifier) @s)", "py", "s")
    cap = [c for c in cap if c.text == b"p"]
    assert len(cap) == 1
    cap = cap[0]
    assert mutator.is_import_statement(cap)


def test_get_toplevel_parent():
    prog = """
import math
from torch.utils import (
	data.DataLoader as dl
)

def outer_function(x, y):
    import boo
    def inner_function(a, b):
        return a * b
    result = inner_function(x, y)
    return result + math.sqrt(x)
"""
    captures = get_captures(prog, "((identifier) @s)", "py", "s")
    cap = [c for c in captures if c.text == b"dl"]
    assert len(cap) == 1
    cap = cap[0]
    parent = get_toplevel_parent(cap)
    assert parent.type == "import_from_statement"
    assert parent.text == b"""from torch.utils import (
	data.DataLoader as dl
)"""

    cap = [c for c in captures if c.text == b"sqrt"]
    assert len(cap) == 1
    cap = cap[0]
    parent = get_toplevel_parent(cap)
    assert parent.type == "return_statement"
    assert parent.text == b"return result + math.sqrt(x)"

    captures = get_captures(prog, "((identifier) @s)", "py", "s")
    cap = [c for c in captures if c.text == b"boo"]
    assert len(cap) == 1
    cap = cap[0]
    parent = get_toplevel_parent(cap)
    assert parent.type == "import_statement"
    assert parent.text == b"import boo"

def test_merge_nested_mutations():
    mutator = PyMutator()
    prompt = """def for_stream(
    stream_name: str, 
    topic: str
) -> 'Addressee':"""
    nodes = get_captures(prompt, "((typed_parameter) @s) ((identifier) @s)", "py","s")
    mutations = [
        Mutation(TreeSitterLocation(n), None, None, None) for n in nodes
    ]
    expected = [
        Mutation(TreeSitterLocation(n), None, None, None) for n in nodes
        if n.type == "typed_parameter" or n.text == b"for_stream"
    ]
    output = mutator.merge_nested_mutation(mutations)
    with open("actual.md","w") as fp:
        fp.write(str(output) + "\n" + "="*1000 + "\n" + str(expected))
    assert set([str(o) for o in output]) == set([str(e) for e in expected])

if __name__ == "__main__":
    import pytest
    pytest.main([os.path.abspath(__file__), "-vv"])