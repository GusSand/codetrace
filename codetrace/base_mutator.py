import tree_sitter
from codetrace.parsing_utils import replace_between_bytes
from typing import List, Tuple, Union, Callable, TypeVar, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

class TreeSitterLocation:
    start_byte : int
    end_byte : int
    start_point : Tuple[int, int]
    end_point : Tuple[int, int]
    
    def __init__(self, tree_sitter_node: tree_sitter.Node):
        self.start_byte = tree_sitter_node.start_byte
        self.end_byte = tree_sitter_node.end_byte
        self.start_point = tree_sitter_node.start_point
        self.end_point = tree_sitter_node.end_point
        
    def __repr__(self):
        return f"""TreeSitterLocation(
            start_byte={self.start_byte},
            end_byte={self.end_byte},
            start_point={self.start_point},
            end_point={self.end_point})"""

@dataclass
class Mutation:
    location : TreeSitterLocation
    byte_replacement : bytes
    prefix : Union[bytes, None] = None
    _text_label : Union[bytes, None] = None

    def __repr__(self):
        prefix = "None"
        if self.prefix is not None:
            prefix = str(self.prefix)
            
        return f"""Mutation(
                {self.location.__repr__()},
                replacement={str(self.byte_replacement)},
                prefix={prefix})"""

MutationFn = TypeVar("MutationFn", bound=Callable[[List[tree_sitter.Node]], List[Mutation]])
tree_sitter_fim = "_CodetraceSpecialPlaceholder_"
fim_placeholder = "<FILL>"

class AbstractMutator(ABC):

    @abstractmethod
    def add_aliases_to_program(self, program: bytes, aliases: List[bytes]) -> bytes:
        pass

    @abstractmethod
    def format_type_alias(self, type_capture: tree_sitter.Node, aliased_name: bytes, **kwargs) -> bytes:
        pass
    
    @abstractmethod
    def extract_type_from_annotation(self, node_capture: tree_sitter.Node) -> tree_sitter.Node:
        pass
    
    @abstractmethod    
    def random_mutate(
        program: str,
        fim_type: str,
        mutations: List[str], 
        **kwargs
    ) -> Optional[str]:
        pass
    
    @abstractmethod
    def find_all_other_locations_of_captures(
        self,
        program:str,
        fim_type:str,
        var_rename_captures: List[tree_sitter.Node],
        type_rename_captures: List[tree_sitter.Node],
        remove_annotations_captures: List[tree_sitter.Node]
    ) -> Tuple[tree_sitter.Node]:
        pass

    @property
    def tree_sitter_placeholder(self) -> str:
        return tree_sitter_fim
    
    def replace_placeholder(self, program:str) -> str:
        if not fim_placeholder in program:
            raise ValueError(f"Program does not contain {fim_placeholder}!")
        return program.replace(fim_placeholder, tree_sitter_fim)
    
    def revert_placeholder(self, program:str) -> str:
        if not tree_sitter_fim in program:
            raise ValueError(f"Program does not contain {tree_sitter_fim}!")
        return program.replace(tree_sitter_fim, fim_placeholder)

    def rename_vars(self, var_captures : List[tree_sitter.Node]) -> List[Mutation]:
        """
        Make mutations for renaming vraiables in VAR_CAPTURES.
        NOTE: new name cannot exist elsewhere in the program, must be different in format from type names.
        The format for vars this function uses is: __tmp{var_index}
        We assume the program does not naturally contain variables with this format
        """
        # map names to captures
        all_names = set([x.text for x in var_captures])
        # map name to new name
        name_to_new_name = {name : bytes(f"__tmp{i}","utf-8") for i, name in enumerate(all_names)}
        mutations = []
        for capture in var_captures:
            location = TreeSitterLocation(capture)
            replacement = name_to_new_name[capture.text]
            mutation = Mutation(location, replacement, _text_label=capture.text)
            mutations.append(mutation)
        return mutations
    
    def rename_types(self, type_captures: List[tree_sitter.Node], **kwargs) -> List[Mutation]:
        """
        Make mutations for renaming types. Assign a new name to each type in type_captures.
        If a type needs it, we create a new type alias for its renamed version.
        
        NOTE: new name cannot exist elsewhere in the program, must be different in format from variable names.
        We assume the program does not naturally contain types with format __typ{type_index}
        """
        # map names to captures
        all_names = set([x.text for x in type_captures])
        # map names to new names
        name_to_new_name = {name : bytes(f"__typ{i}","utf-8") for i, name in enumerate(all_names)}
        
        mutations = []
        for capture in type_captures:
            location = TreeSitterLocation(capture)
            replacement = name_to_new_name[capture.text]
            
            prefix = self.format_type_alias(capture, replacement, **kwargs)
            mutation = Mutation(location, replacement, prefix, _text_label=capture.text)
            mutations.append(mutation)
        return mutations

    def delete_annotations(self, annotation_captures : List[tree_sitter.Node]) -> List[Mutation]:
        """
        Delete the type annotations from captures
        """
        mutations = []
        for capture in annotation_captures:
            location = TreeSitterLocation(capture)
            mutation = Mutation(location, b"", _text_label=capture.text)
            mutations.append(mutation)
        return mutations

    def apply_mutations(self, program: str, mutations: List[Mutation], **test_kargs) -> str:
        """
        Apply mutations to the program.
        NOTE: 
        - applies from bottom up in order to not disturb the byte offsets of other mutations
        - there's the issue that type rename mutations may be nested inside remove annotation mutations
            therefore, if a mutation is nested inside another mutation, keep only the parent mutation
        """
        assert self.tree_sitter_placeholder in program
        # take care of nested mutations
        mutations = self.merge_nested_mutation(mutations)
        mutations.sort(key=lambda x: x.location.start_byte, reverse=True)
        byte_program = program.encode("utf-8")
        prefixes = []
        for mutation in mutations:
            byte_program = replace_between_bytes(byte_program, mutation.location.start_byte,
                                            mutation.location.end_byte, mutation.byte_replacement)
            if mutation.prefix is not None:
                prefixes.append(mutation.prefix)

        if len(prefixes) > 0:
            byte_program = self.add_aliases_to_program(byte_program, prefixes, **test_kargs)
        return byte_program.decode("utf-8")
    
    def random_mutate_ordered_by_type(
        self, 
        program: str, 
        fim_type: str, 
        mutations: List[str]
    ) -> Optional[str]:
        """
        Apply random combination of mutations to the program.
        NOTE: does rename variables first, then rename types, then delete
        """
        new_program = program
        if "rename_vars" in mutations:
            p = self.random_mutate(new_program, fim_type, ["rename_vars"])
            if p:
                new_program = p
        
        if "rename_types" in mutations:
            p = self.random_mutate(new_program, fim_type, ["rename_types"])
            if p:
                new_program = p
                
        if "delete_annotations" in mutations:
            p = self.random_mutate(new_program, fim_type, ["delete_annotations"])
            if p:
                new_program = p
        
        if new_program == program:
            return None
        return new_program
    
    def mutate_captures(
        self,
        program:str,
        mutations:List[MutationFn],
        var_rename_captures: List[tree_sitter.Node],
        type_rename_captures: List[tree_sitter.Node],
        remove_captures: List[tree_sitter.Node],
        **kwargs
    )-> Tuple[Optional[str], List[Mutation]]:
        """
        Given a program, a list of mutations to apply and the target nodes
        for each mutation, return the mutated program and list of actually
        applied mutations.
        """
        assert self.tree_sitter_placeholder in program
        
        # if any out of the selected mutations has no captures, return None
        for (fn, captures) in [
            (self.rename_vars, var_rename_captures),
            (self.rename_types, type_rename_captures),
            (self.delete_annotations, remove_captures)
        ]:
            if fn in mutations and len(captures) == 0:

                return None, []

        # collects mutations
        all_mutations = []
        if self.rename_vars in mutations:
            all_mutations += self.rename_vars(var_rename_captures)
        if self.rename_types in mutations:
            all_mutations += self.rename_types(type_rename_captures, **kwargs)
        if self.delete_annotations in mutations:
            all_mutations += self.delete_annotations(remove_captures)

        # actually modify the program
        new_program = self.apply_mutations(program, all_mutations, **kwargs)
        if new_program == program:
            # no mods applied, return None
            return None, []

        # sometimes the placeholder can be deleted, for example in nested type annotations,
        # so here's a safety check
        try:
            new_program = self.revert_placeholder(new_program)
        except ValueError:
            return None, []
        
        return new_program, all_mutations

    def merge_nested_mutation(self, mutations : List[Mutation]) -> List[Mutation]:
        """
        Merge nested annotation mutations. Recursive
        """
        mutations.sort(key=lambda x: (x.location.start_byte, -x.location.end_byte))
        reduced = []
        
        for current in mutations:
            if reduced and reduced[-1].location.start_byte <= current.location.start_byte and \
                reduced[-1].location.end_byte >= current.location.end_byte:
                continue
            reduced.append(current)

        return reduced
    