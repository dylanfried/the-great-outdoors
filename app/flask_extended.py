import os
import yaml
 
from flask import Flask as BaseFlask, Config as BaseConfig
 
class Config(BaseConfig):
    """Flask config enhanced with a `from_yaml` method."""
    
    def from_yaml(self, config_file):
        with open(config_file) as f:
            c = yaml.load(f)
            
        for key in c.iterkeys():
            if key.isupper():
                # AWS likes to wrap booleans in quotes, so let's make sure that they're
                # evaluated to be a boolean
                if type(c[key]) == str and c[key] == 'True':
                    self[key] = True
                elif type(c[key]) == str and c[key] == 'False':
                    self[key] = False
                else:
                    self[key] = c[key]
                
class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class"""
    
    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

