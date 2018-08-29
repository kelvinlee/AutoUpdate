import sublime, sublime_plugin
import sys
import imp

import emmet.context

def getV8():
  emmet.context.import_pyv8()
  if 'PyV8' in sys.modules:
    if 'PyV8' not in globals():
      globals()['PyV8'] = __import__('PyV8')
  return globals()['PyV8']