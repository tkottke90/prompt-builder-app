import importlib
import pkgutil
import sys
import os

PLUGIN_DIR = os.path.abspath('./plugins');

def discovered_plugins(prefix: str = ''): 
    for finder, name, ispkg in pkgutil.iter_modules([ PLUGIN_DIR ], prefix=prefix):
      if (ispkg is False): continue

      print('Module: ' + name)
      print('        ' + str(ispkg))


if __name__ == "__main__":
  print(PLUGIN_DIR)
  discovered_plugins('ai_plugin.')