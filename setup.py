# -*- coding:utf-8 -*-
from distutils.core import setup

setup(name = 'dconf-search',
      license='MIT',
      version = '0.1',
      description = 'A tool to search for dconf entries',
      author=u'André Ericson',
      author_email='de.ericson@gmail.com',
      url='https://github.com/aericson/dconf-search',
      packages=['dconf_search'],
      scripts=['bin/dconf-search'],
      long_description = open('README').read(),
      install_requires=[
          'tinydconf>=0.1',
      ],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Gtk Users',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: C/Python',
          'Topic :: Utilities', 
      ])
