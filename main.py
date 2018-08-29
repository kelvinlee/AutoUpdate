import sublime, sublime_plugin
import traceback
import codecs
import json
import os
import os.path
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
# ================================== #
#                                    #
# You can use the pyv8_loader module #
#    or implement your own module    #
#                                    #
#       import pyv8_loader           #
#                                    #
# ================================== #

import pyv8_loader

class AutoUpdateContentCommand(sublime_plugin.TextCommand):

  def run(self, edit):

    view = self.view
    sel = view.sel()[0]

    # Get the selected text #
    # str_selected = view.substr(sel).strip()

    # if not str_selected : 
    #   sublime.error_message("Plese select the text you want to evaluate with PyV8!")
    #   return

    try:

      # ======================================================== #
      # Here we call the "getV8()" method to get the PyV8 module #
      # ======================================================== #
      PyV8 = pyv8_loader.getV8()
      
      
      # Now you can use PyV8 #
      ctx = PyV8.JSContext()
      ctx.enter()
      # Set function to js
      ctx.locals.log = js_log
      ctx.locals.activeView = active_view
      ctx.locals.sublime = sublime
      ctx.locals.sublime_plugin = sublime_plugin
      ctx.locals.BASE_PATH = BASE_PATH
      ctx.locals.fileName = view.file_name()
      result_js = str(ctx.eval(self.read_js_file("edit.js",True)))

      # It will show the result of evaluation #
      # sublime.message_dialog("Result: "+result_js)
      print("callback:",result_js)

    except Exception as e:
      # Ops, you wrote bad JavaScript! :( #
      print("Error: "+traceback.format_exc())
      # sublime.error_message("Error: "+traceback.format_exc())
  
 

  def read_js_file(self, file_path, resolve_path=False):
    full_path = make_path(file_path) if resolve_path else file_path
    return self.js_file_reader(full_path, None)

  def js_file_reader(self, file_path, use_unicode=True):
    if use_unicode:
      f = codecs.open(file_path, 'r', 'utf-8')
    else:
      f = open(file_path, 'r')

    content = f.read()
    f.close()

    return content


def make_path(filename):
  return os.path.normpath(os.path.join(BASE_PATH, filename))
def js_log(message):
  print(message)
def active_view():
  return sublime.active_window().active_view()

'''
´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶
´´´´´´´´´´´´´´´´´´´´¶¶´´´´´´´´´´¶¶
´´´´´´¶¶¶¶¶´´´´´´´¶¶´´´´´´´´´´´´´´¶¶
´´´´´¶´´´´´¶´´´´¶¶´´´´´¶¶´´´´¶¶´´´´´¶¶
´´´´´¶´´´´´¶´´´¶¶´´´´´´¶¶´´´´¶¶´´´´´´´¶¶
´´´´´¶´´´´¶´´¶¶´´´´´´´´¶¶´´´´¶¶´´´´´´´´¶¶
´´´´´´¶´´´¶´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´¶¶
´´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´´´´´´¶¶
´´´¶´´´´´´´´´´´´¶´¶¶´´´´´´´´´´´´´¶¶´´´´´¶¶
´´¶¶´´´´´´´´´´´´¶´´¶¶´´´´´´´´´´´´¶¶´´´´´¶¶
´¶¶´´´¶¶¶¶¶¶¶¶¶¶¶´´´´¶¶´´´´´´´´¶¶´´´´´´´¶¶
´¶´´´´´´´´´´´´´´´¶´´´´´¶¶¶¶¶¶¶´´´´´´´´´¶¶
´¶¶´´´´´´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´¶¶
´´¶´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´¶¶
´´¶¶´´´´´´´´´´´¶´´¶¶´´´´´´´´´´´´´´´´¶¶
´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶´´´´´´´´´´´´¶¶
´´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶
'''