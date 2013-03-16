import sublime, sublime_plugin
import os
import re

DEBUG=False

class JavaCreateClassCommand(sublime_plugin.TextCommand):

	def getClassName(self, edit):
		self.className = ""
		try:
			classLine = self.view.substr(self.view.find('class\s+\w+',0))
			m = re.search('class\s+(\w+)',classLine)
			if(m):
				self.className = m.groups()[0]
		except Exception, ex:
			if DEBUG:
				print ex

	def getFolders(self, path):
		# Credit:
		#  http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
		folders=[]
		while 1:
		    path,folder=os.path.split(path)

		    if folder!="":
		        folders.append(folder)
		    else:
		        if path!="":
		            folders.append(path)

		        break
		folders.reverse()
		return folders

	def getPackageName(self, path):
		folders = self.getFolders(path)

		package = ''
		folder = folders.pop()
		packageFolders = []
		while True:
			if self.re_jpath.search(folder):
				break
			packageFolders.append(folder)
			# package = "%s.%s" % (package,folder)
			if len(folders)==0:
				break
			folder = folders.pop()
		packageFolders.reverse()
		return '.'.join(packageFolders)

	def run(self, edit):
		self.re_jpath = re.compile('java',re.IGNORECASE)
		path, filename = os.path.split(self.view.file_name())

		if not filename.endswith('.java'):
			if DEBUG:
				print "Error: filename must end in .java"

		classTemplate = """package {0};

public class {1} {{
	
	public {1}() {{

	}}
}}
"""

		className = filename[0:filename.find('.java')]
		packageName = self.getPackageName(path)

		self.view.insert(edit, 0, classTemplate.format(packageName,className))
