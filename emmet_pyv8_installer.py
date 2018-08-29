import sublime
import sublime_plugin

import re
import imp
import json
import sys
import os.path
import traceback

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
sys.path += [BASE_PATH] + [os.path.join(BASE_PATH, f) for f in ['emmet_completions', 'emmet']]


# Make sure all dependencies are reloaded on upgrade
if 'emmet.reloader' in sys.modules:
	imp.reload(sys.modules['emmet.reloader'])
import emmet.reloader

# import completions as cmpl
import emmet.pyv8loader as pyv8loader
from emmet.context import Context
from emmet.context import js_file_reader as _js_file_reader
from emmet.pyv8loader import LoaderDelegate

is_python3 = sys.version_info[0] > 2

# JS context
ctx = None

def is_st3():
	return sublime.version()[0] == '3'

def init():
	"Init PyV8 Emmet Loader plugin"

	# setup environment for PyV8 loading
	pyv8_paths = [
		os.path.join(PACKAGES_PATH, 'PyV8'),
		os.path.join(PACKAGES_PATH, 'PyV8', pyv8loader.get_arch()),
		os.path.join(PACKAGES_PATH, 'PyV8', 'pyv8-%s' % pyv8loader.get_arch())
	]

	sys.path += pyv8_paths

	# unpack recently loaded binary, is exists
	for p in pyv8_paths:
		pyv8loader.unpack_pyv8(p)

	# create JS environment
	delegate = SublimeLoaderDelegate()

	pyv8loader.load(pyv8_paths[1], delegate) 

class SublimeLoaderDelegate(LoaderDelegate):
	def __init__(self, settings=None):

		LoaderDelegate.__init__(self, {})
		self.state = None
		self.message = 'Loading PyV8 binary, please wait'
		self.i = 0
		self.addend = 1
		self.size = 8

	def on_start(self, *args, **kwargs):
		self.state = 'loading'

	def on_progress(self, *args, **kwargs):
		if kwargs['progress'].is_background:
			return

		before = self.i % self.size
		after = (self.size - 1) - before
		msg = '%s [%s=%s]' % (self.message, ' ' * before, ' ' * after)
		if not after:
			self.addend = -1
		if not before:
			self.addend = 1
		self.i += self.addend

		sublime.set_timeout(lambda: sublime.status_message(msg), 0)

	def on_complete(self, *args, **kwargs):
		self.state = 'complete'

		if kwargs['progress'].is_background:
			return

		sublime.set_timeout(lambda: sublime.status_message('PyV8 binary successfully loaded'), 0)

	def on_error(self, exit_code=-1, progress=None):
		self.state = 'error'
		sublime.set_timeout(lambda: show_pyv8_error(exit_code), 0)

	def setting(self, name, default=None):
		"Returns specified setting name"
		return self.settings.get(name, default)

	def log(self, message):
		print('PyV8 Emmet Loader: %s' % message)

def show_pyv8_error(exit_code):
	if 'PyV8 Emmet Loader' not in sys.modules:
		sublime.error_message('Error while loading PyV8 binary: exit code %s \nTry to manually install PyV8 from\nhttps://github.com/emmetio/pyv8-binaries' % exit_code)

def plugin_loaded():
	sublime.set_timeout(init, 200)

##################
# Init plugin
if not is_python3:
	init()

