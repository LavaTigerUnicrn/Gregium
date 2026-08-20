"""
Custom schema loader
"""
import json
from typing import Any

# TODO:
# Add enum support
# Add support for list items

class NoSchemaError(Exception):
    pass
class SchemaLoadError(Exception):
    pass

class Matcher:
    """
    Loads from JSON

    This allows for custom settings loaders or JSON matching

    :param json_path: The path to the JSON
    :type json_path: str
    :param schema_path: The path to the JSON schema

        This is required for fix and reset
    :type schema_path: str, optional               

    The schema keys must all have "type", "default", and "description"
    """

    loaded:dict[Any,Any]
    schema:dict[str,Any]

    def __init__(self,json_path:str,schema_path:str|None=None):

        # Set paths
        self.json_path:str = json_path
        self.schema_path:str|None = schema_path

        # Load
        self.load()

        # Load schema
        self.schema = {}
        if schema_path is not None:

            self.load_schema()

    def load(self):
        """
        Loads the JSON from path
        
        This will revert all from file
        """

        # Load JSON
        try:

            with open(self.json_path,"r") as r:

                self.loaded = json.load(r)

        except (FileNotFoundError,json.JSONDecodeError):
            with open(self.json_path,"w") as w:

                w.write("{}")
                self.loaded = {}

    def load_schema(self):
        """
        Loads the schema from JSON path
        """

        if self.schema_path is None:
            raise NoSchemaError("No schema path specified")

        # load JSON
        with open(self.schema_path,"r") as r:

            default:dict = json.load(r)

        # Recurse scan for default values
        read_keys = ["",]
        assembled_keys = {}

        # Read and assemble defaults
        while len(read_keys) > 0:

            # Get next key
            key = read_keys[-1]
            value = read_dict_from_path(default,key)
            read_keys.pop()

            # Only continue if key is correct
            if type(value) is not dict:
                continue

            # Ensure type is present
            if "type" not in value:
                raise SchemaLoadError(f"key 'type' not supplied for schema found at {key}")

            # Get type
            key_type = value["type"]

            # Check if value contains required items
            if key_type != "object" and "default" not in value:

                raise SchemaLoadError(f"key 'default' not supplied for schema found at {key}")

            if key_type == "object":

                # Get properties
                new_keys = [(key+".properties."+x).lstrip(".") for x in value["properties"]]
                read_keys = read_keys + new_keys

                value_setter = value.copy()
                value_setter.pop("properties")

                # Add to key assembly
                assembled_keys[key.replace("properties.","")] = value_setter

            else:

                # Add to key assembly
                assembled_keys[key.replace("properties.","")] = value

        self.schema = assembled_keys

    def fix(self):
        """
        Fills in all unknown values to JSON based on schema
        """

        # Raise error if no schema
        if not self.schema_path:

            raise NoSchemaError("No schema has been set")

        # Scan the created json
        for key in self.schema:

            # Get value
            value = self.schema[key]
            default = {}
            if "default" in value:
                default = value["default"]

            # Check if key exists
            try:

                read_dict_from_path(self.loaded,key)

            except KeyError:

                # If it doesn't, set value
                key_parent = ".".join(key.split(".")[:-1])
                key_root = key.split(".")[-1]

                read_dict_from_path(self.loaded,key_parent)[key_root] = default

    def reset(self):
        """
        Resets all values to JSON based on schema
        """

        # Raise error if no schema
        if not self.schema_path:

            raise NoSchemaError("No schema has been set")

        # Scan the created json
        for key in self.schema:

            # Get value
            value = self.schema[key]
            default = {}
            if "default" in value:
                default = value["default"]

            # Cancel for blank
            if key == "":

                continue

            # Set value
            key_parent = ".".join(key.split(".")[:-1])
            key_root = key.split(".")[-1]

            read_dict_from_path(self.loaded,key_parent)[key_root] = default

    def save(self):
        """
        Saves all stored JSON
        """

        # Load settings to JSON
        with open(self.json_path,"w") as w:

            json.dump(self.loaded,w,indent=4)

    def __str__(self):
        """
        Prints out all loaded settings
        """

        schema_def = "SCHEMA NOT LOADED"
        if self.schema is not None:
            schema_def = json.dumps(self.schema,indent=4)

        return f"Loaded Settings: \n{json.dumps(self.loaded,indent=4)}\n\nSchema Defaults: \n{schema_def}"

    def get(self,path:str) -> Any|None:
        """
        Gets a value at path
        
        `This will only work on dictionaries, attempting to traverse a list key wont work (Must do get("partial.path")[index])`
        
        :param path: The path where the value is found at
        
            This must be in dot notation
            `foo.baz.bar`
        
            This is equivalent to
            {"foo":{"baz":{"bar":"value"}}}
        :type path: str
                
        Will return None if no setting is present
        If schema was defined will instead return default value (but using `.fix_settings` is recommended)

        :return: The data at the given path (or None if it can't be found)
        :rtype: Any | None
        """

        try:
            return read_dict_from_path(self.loaded,path)
        except KeyError:
            if path in self.schema:
                value = self.schema[path]
                if "default" in value:
                    return value["default"]
            return None

    def set(self,path:str,value:Any) -> bool:
        """
        Sets a setting at path
        
        `This will only work on dictionaries, attempting to traverse a list key wont work (Must do get("partial.path")[index] = value)`
        
        :param path: The path where the value is found at
                
            This must be in dot notation
            `foo.baz.bar`
            
            This is equivalent to
            {"foo":{"baz":{"bar":"value"}}}
        :type path: str
        :param value: The value to set
        :type value: Any
         
        :return: Returns False on failure
        :rtype: boo
        """

        try:
            read_dict_from_path(self.loaded, ".".join(path.split(".")[:-1]))[
                path.split(".")[-1]
            ] = value
            return True
        except KeyError:
            return False

    def __setitem__(self,path:str,value:Any) -> bool:
        """
        Sets a setting at path
        
        `This will only work on dictionaries, attempting to traverse a list key wont work (Must do get("partial.path")[index] = value)`
        
        :param path: The path where the value is found at
        
            This must be in dot notation
            `foo.baz.bar`
        
            This is equivalent to
            {"foo":{"baz":{"bar":"value"}}}
        :type path: str
        :param value: The value to set
        :type value: Any
        
        :return: Returns False on failure
        :rtype: boo
        """
        
        try:
            read_dict_from_path(self.loaded, ".".join(path.split(".")[:-1]))[
                path.split(".")[-1]
            ] = value
            return True
        except KeyError:
            return False

    def __getitem__(self,key:str):
        """
        Gets a value at path
        
        `This will only work on dictionaries, attempting to traverse a list key wont work (Must do get("partial.path")[index])`
        
        :param path: The path where the value is found at
        
            This must be in dot notation
            `foo.baz.bar`
        
            This is equivalent to
            {"foo":{"baz":{"bar":"value"}}}
        :type path: str
        
        Will return None if no setting is present
        If schema was defined will instead return default value (but using `.fix_settings` is recommended)
        
        :return: The data at the given path (or None if it can't be found)
        :rtype: Any | None
        """

        try:
            return self.loaded[key]
        except KeyError:
            if key in self.schema:
                value = self.schema[key]
                if "default" in value:
                    return value["default"]
            return None

def read_dict_from_path(read:dict[str,Any],path:str) -> Any:
    """
    Reads a place in a dictionary from a path

    :param read: The dictionary to read
    :type read: dict
    :param path: The path to read (format of foo.baz.bar)
    :type path: str

    :return: The data at the path
    :rtype: Any
    """

    # Edge case of blank path
    if path == "":
        return read

    # Split path by dots
    paths:list = path.split(".")

    # Go through path
    while len(paths) > 0:
        section = paths[0]
        paths = paths[1:]
        read = read[section]

    return read
