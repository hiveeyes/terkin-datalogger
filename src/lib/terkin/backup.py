# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import uos
import time
import os_path
from shutil import copyfileobj
from terkin import logging
from terkin.util import file_remove, file_exists, ensure_directory


log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


def backup_file(filename, backup_path, backup_count):
    """Backup file using a rotation mechanism.

    :param filename: param backup_path:
    :param backup_count: return:
    :param backup_path: 

    """

    # Sanity checks.
    if not file_exists(filename):
        log.info('File {} does not exist, skipping backup'.format(filename))
        return

    #log.info('Preparing backup')
    # Running this here will crash the machine.
    #ensure_directory(backup_path)

    filepath = os_path.join(backup_path, os_path.basename(filename))
    outfile = RotatingFile(filepath, backup_count)

    log.info('Creating backup of {}'.format(filename))
    with open(filename, "r") as f:
        outfile.write(f)


class RotatingFile:
    """
    A rotating file handler like RotatingFileHandler.
    
    From logging.handlers.

    """

    def __init__(self, filename, backup_count=0):
        self.filename = filename
        self.backup_count = backup_count

    def write(self, buffer):
        """
        Remove oldest backup, rotate name and write buffer to file.

        :param buffer: buffer to write

        """
        if self.backup_count:

            # Remove the oldest backup file if it is there.
            old_backupfile = "{}.{}".format(self.filename, self.backup_count)
            #log.info('Removing backup file {}'.format(old_backupfile))
            file_remove(old_backupfile)

            # Rename backup files in between oldest and newest one.
            for i in range(self.backup_count - 1, 0, -1):
                if i < self.backup_count:
                    self.rename_file(
                        "{}.{}".format(self.filename, i),
                        "{}.{}".format(self.filename, i + 1))

            # Rename most recent backup file.
            self.rename_file(self.filename, "{}.{}".format(self.filename, 1))

        # Write new most recent backup file.
        log.info('Writing recent backup to {}'.format(self.filename))
        with open(self.filename, "w") as outfile:
            #log.info('copyfileobj: {} => {}'.format(buffer, outfile))
            copyfileobj(buffer, outfile)

        time.sleep_ms(150)
        uos.sync()

    def rename_file(self, oldfile, newfile):
        """
        Rename fila

        :param oldfile: old file name
        :param newfile: new file name

        """
        #log.info('Renaming backup file {} to {}'.format(oldfile, newfile))
        try:
            os.rename(oldfile, newfile)
        except OSError:
            pass
        time.sleep_ms(5)
        uos.sync()
        time.sleep_ms(5)
