"""
    by oPromessa, 2017
    Published on https://github.com/oPromessa/flickr-uploader/

    Helper class and functions to load, process and verify INI configuration.


    MyConfiguration = Helper class and functions to load, process and
                      verify INI configuration.

    processconfig   = Helper function ...
    verifyconfig    = Helper function ...
"""

# -----------------------------------------------------------------------------
# Import section for Python 2 and 3 compatible code
# from __future__ import absolute_import, division, print_function,
#    unicode_literals
from __future__ import division    # This way: 3 / 2 == 1.5; 3 // 2 == 1

# -----------------------------------------------------------------------------
# Import section
#
import sys
import os
import logging
import re
try:
    import ConfigParser as ConfigParser  # Python 2
except ImportError:
    import configparser as ConfigParser  # Python 3
from . import niceprint

# =============================================================================
# Functions aliases
#
#   StrUnicodeOut       = from niceprint module
# -----------------------------------------------------------------------------
np = niceprint.niceprint()
StrUnicodeOut = np.StrUnicodeOut


# -----------------------------------------------------------------------------
# class MyConfiguration to hangle Config file uploadr.ini for flickr-uploadr.
#
class MyConfig(object):
    """ MyConfig

        Loads default configuration files. Overwrites with any specific values
        found on INI config file.
    """
    # Config section ----------------------------------------------------------
    INISections = ['Config']
    # Default configuration keys/values pairs ---------------------------------
    INIkeys = [
        'FILES_DIR',
        'FLICKR',
        'SLEEP_TIME',
        'DRIP_TIME',
        'DB_PATH',
        'LOCK_PATH',
        'TOKEN_CACHE',
        'TOKEN_PATH',
        'EXCLUDED_FOLDERS',
        'IGNORED_REGEX',
        'ALLOWED_EXT',
        'CONVERT_RAW_FILES',
        'RAW_EXT',
        'RAW_TOOL_PATH',
        'FILE_MAX_SIZE',
        'MANAGE_CHANGES',
        'FULL_SET_NAME',
        'MAX_SQL_ATTEMPTS',
        'MAX_UPLOAD_ATTEMPTS',
        'LOGGING_LEVEL'
    ]
    # Default configuration keys/values pairs ---------------------------------
    INIvalues = [
        # FILES_DIR
        "'photos'",
        # FLICKR
        "{ 'title'       : '',\
           'description' : '',\
           'tags'        : 'auto-upload',\
           'is_public'   : '0',\
           'is_friend'   : '0',\
           'is_family'   : '0',\
           'api_key'     : 'api_key_not_defined',\
           'secret'      : 'secret_not_defined'\
        }",
        # SLEEP_TIME
        "1 * 60",
        # DRIP_TIME
        "1 * 60",
        #  DB_PATH
        "os.path.join(os.path.dirname(sys.argv[0]), 'flickrdb')",
        # LOCK_PATH
        "os.path.join(os.path.dirname(sys.argv[0]), '.flickrlock')",
        # TOKEN_CACHE
        "os.path.join(os.path.dirname(sys.argv[0]), 'token')",
        # TOKEN_PATH
        "os.path.join(os.path.dirname(sys.argv[0]), '.flickrToken')",
        # EXCLUDED_FOLDERS (need to process for unicode support)
        "['@eaDir','#recycle','.picasaoriginals','_ExcludeSync',\
          'Corel Auto-Preserve','Originals',\
          'Automatisch beibehalten von Corel']",
        # IGNORED_REGEX
        "[ ]",
        # "['IMG_[0-8]', '.+Ignore.+']",
        # ALLOWED_EXT
        "['jpg','png','avi','mov','mpg','mp4','3gp']",
        # CONVERT_RAW_FILES
        "False",
        # RAW_EXT
        "['3fr', 'ari', 'arw', 'bay', 'crw', 'cr2', 'cap', 'dcs',\
          'dcr', 'dng', 'drf', 'eip', 'erf', 'fff', 'iiq', 'k25',\
          'kdc', 'mdc', 'mef', 'mos', 'mrw', 'nef', 'nrw', 'obm',\
          'orf', 'pef', 'ptx', 'pxn', 'r3d', 'raf', 'raw', 'rwl',\
          'rw2', 'rwz', 'sr2', 'srf', 'srw', 'x3f' ]",
        # RAW_TOOL_PATH
        "'/volume1/photo/Image-ExifTool-9.69'",
        # FILE_MAX_SIZE
        "50000000",
        # MANAGE_CHANGES
        "True",
        # FULL_SET_NAME
        "False",
        #  MAX_SQL_ATTEMPTS
        "3",
        # MAX_UPLOAD_ATTEMPTS
        "10",
        # LOGGING_LEVEL
        "40"
    ]

    # -------------------------------------------------------------------------
    # MyConfig.__init__
    #
    # Obtain configuration from uploadr.ini
    # Refer to contents of uploadr.ini for explanation on configuration
    # parameters.
    # Obtain configuration LOGGING_LEVEL from Configuration file.
    # If not available or not valid assume WARNING level and notify.
    # Look for [Config] section file uploadr.ini file
    #
    def __init__(self, cfg_filename, cfg_Sections=INISections):
        """__init__
        """

        # Assume default values into class dictionary of values ---------------
        self.__dict__ = dict(zip(self.INIkeys, self.INIvalues))
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            logging.debug('\t\t\t\tDefault INI key/values pairs...')
            for item in sorted(self.__dict__):
                logging.debug('[{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                              .format(item,
                                      type(self.__dict__[item]),
                                      StrUnicodeOut(self.__dict__[item])))
        # Look for Configuration INI file -------------------------------------
        config = ConfigParser.ConfigParser()
        config.optionxform = str  # make option names case sensitive
        try:
            INIFile = None
            INIFile = config.read(cfg_filename)
            for name in cfg_Sections:
                self.__dict__.update(config.items(name))
        except Exception as err:
            logging.critical('INI file: [{!s}] not found or '
                             'incorrect format: [{!s}]! Will attempt to use '
                             'default INI values.'
                             .format(cfg_filename, str(err)))
        finally:
            # Allow to continue with default values...
            if not INIFile:
                raise ValueError('No config file or unrecoverable error!')

        # Parse Configuration file and overwrite any values -------------------
        # pprint.pprint(config.items(cfg_Sections[0]))

        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            logging.info('\t\t\t\tActive INI key/values pairs...')
            for item in sorted(self.__dict__):
                logging.info('[{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                             .format(item,
                                     type(self.__dict__[item]),
                                     StrUnicodeOut(self.__dict__[item])))

    # -------------------------------------------------------------------------
    # MyConfig.processconfig
    #
    def processconfig(self):
        """ process
        """
        # Default types for keys/values pairs ---------------------------------
        INItypes = [
            'str',   # 'FILES_DIR',
            'dict',  # 'FLICKR',
            'int',   # 'SLEEP_TIME',
            'int',   # 'DRIP_TIME',
            'str',   # 'DB_PATH',
            'str',   # 'LOCK_PATH',
            'str',   # 'TOKEN_CACHE',
            'str',   # 'TOKEN_PATH',
            'list',  # 'EXCLUDED_FOLDERS',
            'list',  # 'IGNORED_REGEX',
            'list',  # 'ALLOWED_EXT',
            'bool',  # 'CONVERT_RAW_FILES',
            'list',  # 'RAW_EXT',
            'str',   # 'RAW_TOOL_PATH',
            'int',   # 'FILE_MAX_SIZE',
            'bool',  # 'MANAGE_CHANGES',
            'bool',  # 'FULL_SET_NAME',
            'int',   # 'MAX_SQL_ATTEMPTS',
            'int',   # 'MAX_UPLOAD_ATTEMPTS',
            'int'    # 'LOGGING_LEVEL'
        ]
        INIcheck = dict(zip(self.INIkeys, INItypes))
        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            logging.debug('\t\t\t\tDefault INI key/type pairs...')
            for item in sorted(INIcheck):
                logging.debug('[{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                              .format(item,
                                      type(INIcheck[item]),
                                      StrUnicodeOut(INIcheck[item])))
        # Evaluate values
        for item in sorted(self.__dict__):
            logging.debug('Eval for : [{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                          .format(item,
                                  type(self.__dict__[item]),
                                  StrUnicodeOut(self.__dict__[item])))

            try:
                if INIcheck[item] in ('list', 'int', 'bool', 'str', 'dict'):
                    logging.debug('isinstance={!s}'
                                  .format(
                                      isinstance(eval(self.__dict__[item]),
                                                 eval(INIcheck[item]))))
                    if not(isinstance(eval(self.__dict__[item]),
                                      eval(INIcheck[item]))):
                        raise
                else:
                    raise
            except BaseException:
                logging.critical('Invalid INI value for:[{!s}] '
                                 'Using default value:[{!s}]'
                                 .format(item,
                                         self.INIvalues[
                                             self.INIkeys.index(str(item))]))
                # Use default value or exit...
                self.__dict__.update(dict(zip(
                    [item],
                    [self.INIvalues[self.INIkeys.index(str(item))]])))
            finally:
                self.__dict__[item] = eval(self.__dict__[item])
                logging.debug('Eval done: [{!s:20s}]/type:[{!s:13s}] '
                              '= [{!s:10s}]'
                              .format(item,
                                      type(self.__dict__[item]),
                                      StrUnicodeOut(self.__dict__[item])))

        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            logging.info('\t\t\t\tProcessed INI key/values pairs...')
            for item in sorted(self.__dict__):
                logging.info('[{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                             .format(item,
                                     type(self.__dict__[item]),
                                     StrUnicodeOut(self.__dict__[item])))

        return True

    # -------------------------------------------------------------------------
    # MyConfig.verifyconfig
    #
    def verifyconfig(self):
        """ readconfig
        """

        # Further specific processing... LOGGING_LEVEL
        if self.__dict__['LOGGING_LEVEL'] not in\
                [logging.NOTSET,
                 logging.DEBUG,
                 logging.INFO,
                 logging.WARNING,
                 logging.ERROR,
                 logging.CRITICAL]:
            self.__dict__['LOGGING_LEVEL'] = logging.WARNING
        # Convert LOGGING_LEVEL into int() for later use in conditionals
        self.__dict__['LOGGING_LEVEL'] = int(str(
            self.__dict__['LOGGING_LEVEL']))

        # Further specific processing... FILES_DIR
        for item in ['FILES_DIR']:  # Check if dir exists. Unicode Support
            logging.debug('verifyconfig for [{!s}]'.format(item))
            self.__dict__[item] = unicode(  # noqa
                                      self.__dict__[item],
                                      'utf-8') \
                                  if sys.version_info < (3, ) \
                                  else str(self.__dict__[item])
            if not os.path.isdir(self.__dict__[item]):
                logging.critical('{!s}: [{!s}] is not a valid folder.'
                                 .format(item,
                                         StrUnicodeOut(self.__dict__[item])))

        # Further specific processing...
        #       DB_PATH
        #       LOCK_PATH
        #       TOKEN_CACHE
        #       TOKEN_PATH
        #       RAW_TOOL_PATH  # Not used for now!
        for item in ['DB_PATH',  # Check if basedir exists. Unicode Support
                     'LOCK_PATH',
                     'TOKEN_CACHE',
                     'TOKEN_PATH']:
            logging.debug('verifyconfig for [{!s}]'.format(item))
            self.__dict__[item] = unicode(  # noqa
                                      self.__dict__[item],
                                      'utf-8') \
                                  if sys.version_info < (3, ) \
                                  else str(self.__dict__[item])
            if not os.path.isdir(os.path.dirname(self.__dict__[item])):
                logging.critical('{!s}: [{!s}] is not in a valid folder.'
                                 .format(item,
                                         StrUnicodeOut(self.__dict__[item])))

        # Further specific processing... EXCLUDED_FOLDERS
        #     Read EXCLUDED_FOLDERS and convert them into Unicode folders
        logging.debug('verifyconfig for [{!s}]'.format('EXCLUDED_FOLDERS'))
        inEXCLUDED_FOLDERS = self.__dict__['EXCLUDED_FOLDERS']
        logging.debug('inEXCLUDED_FOLDERS=[{!s}]'
                      .format(inEXCLUDED_FOLDERS))
        outEXCLUDED_FOLDERS = []
        for folder in inEXCLUDED_FOLDERS:
            outEXCLUDED_FOLDERS.append(unicode(folder, 'utf-8')  # noqa
                                       if sys.version_info < (3, )
                                       else str(folder))
            logging.debug('folder from EXCLUDED_FOLDERS:[{!s}] '
                          'type:[{!s}]\n'
                          .format(
                              StrUnicodeOut(outEXCLUDED_FOLDERS[
                                  len(outEXCLUDED_FOLDERS) - 1]),
                              type(outEXCLUDED_FOLDERS[
                                  len(outEXCLUDED_FOLDERS) - 1])))
        logging.info('outEXCLUDED_FOLDERS=[{!s}]'
                     .format(outEXCLUDED_FOLDERS))
        self.__dict__.update(dict(zip(
            ['EXCLUDED_FOLDERS'],
            [outEXCLUDED_FOLDERS])))

        # Further specific processing... IGNORED_REGEX
        # Consider Unicode Regular expressions
        for item in ['IGNORED_REGEX']:
            logging.debug('verifyconfig for [{!s}]'.format(item))
            self.__dict__[item] = [re.compile(regex, re.UNICODE)
                                   for regex in self.__dict__[item]]
            logging.info('Number of IGNORED_REGEX entries:[{!s}]\n'
                         .format(len(self.__dict__[item])))

        # ---------------------------------------------------------------------
        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            logging.info('\t\t\t\tVerified INI key/values pairs...')
            for item in sorted(self.__dict__):
                logging.info('[{!s:20s}]/type:[{!s:13s}] = [{!s:10s}]'
                             .format(item,
                                     type(self.__dict__[item]),
                                     StrUnicodeOut(self.__dict__[item])))

        return True


# -----------------------------------------------------------------------------
# If called directly run doctests
#
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s]:[%(processName)-11s]' +
                               '[%(levelname)-8s]:[%(name)s] %(message)s')

    import doctest
    doctest.testmod()

    # Comment following line to allow further debugging/testing
    sys.exit(0)