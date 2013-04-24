#
#   Copyright (C) 2013 Ash (Tuxdude) <tuxdude.github@gmail.com>
#
#   This file is part of repobuddy.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation; either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this program.  If not, see
#   <http://www.gnu.org/licenses/>.
#

import sys as _sys

if _sys.version_info >= (3, 0):
    import configparser as _configparser    # pylint: disable=F0401
else:
    import ConfigParser as _configparser    # pylint: disable=F0401

from repobuddy.utils import RepoBuddyBaseException


class ClientInfoError(RepoBuddyBaseException):
    def __init__(self, error_str):
        super(ClientInfoError, self).__init__(error_str)
        return


class ClientInfo(object):
    def _validate_config(self):
        # Verify client_spec and manifest options exist
        self.get_client_spec()
        self.get_manifest()
        return

    def _get_config(self, section, option):
        try:
            return self._config.get(section, option)
        except (_configparser.NoOptionError,
                _configparser.NoSectionError) as err:
            raise ClientInfoError('Error: ' + str(err))
        return

    def _set_config(self, section, option, value):
        try:
            self._config.set(section, option, value)
        except _configparser.NoSectionError as err:
            raise ClientInfoError('Error: ' + str(err))
        return

    def __init__(self, config_file_name=None):
        if not config_file_name is None:
            try:
                with open(config_file_name, 'r') as file_handle:
                    self._config = _configparser.RawConfigParser()
                    try:
                        self._config.readfp(file_handle)
                    except _configparser.ParsingError as err:
                        raise ClientInfoError(
                            'Error: Parsing config failed => ' + str(err))
            except IOError as err:
                raise ClientInfoError('Error: ' + str(err))

            self._validate_config()
            self._config_file_name = config_file_name
        else:
            self._config = _configparser.RawConfigParser()
            self._config.add_section('RepoBuddyClientInfo')
            self._config_file_name = None
        return

    def set_client_spec(self, client_spec_name):
        self._set_config('RepoBuddyClientInfo',
                         'client_spec',
                         client_spec_name)
        return

    def set_manifest(self, manifest_xml):
        self._set_config('RepoBuddyClientInfo', 'manifest', manifest_xml)
        return

    def get_client_spec(self):
        return self._get_config('RepoBuddyClientInfo', 'client_spec')

    def get_manifest(self):
        return self._get_config('RepoBuddyClientInfo', 'manifest')

    def write(self, file_name=None):
        # If file_name parameter is empty, check if the file name was
        # specified in the constructor
        if file_name is None:
            if self._config_file_name is None:
                raise ClientInfoError(
                    'Error: file_name parameter cannot be empty')
            else:
                file_name = self._config_file_name

        # Verify that the config is valid
        try:
            self._validate_config()
        except ClientInfoError as err:
            raise ClientInfoError(
                'Error: Missing options. ' + str(err).split('Error: ')[1])

        try:
            with open(file_name, 'w') as config_file:
                self._config.write(config_file)
        except IOError as err:
            raise ClientInfoError('Error: ' + str(err))
        return
