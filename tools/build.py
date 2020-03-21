# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
"""
About
=====
MicroPython firmware builder for humans.

Features
========
- Takes care of the whole firmware image building process.
- Supports different vendors of MicroPython.
- Can freeze modules.

References
==========
- https://docs.micropython.org/en/latest/reference/packages.html
- https://docs.micropython.org/en/latest/reference/constrained.html

Backlog
=======
- Add "--flash" option to automatically upload artefact to device.
- Integrate filesystem watcher through "hupper".
- Adjust "-j8" make parameter.
- Publish firmware images using rsync.
- Add "--release-dir" and "--application-dir" parameters.
- Build Pycom variants "BASE" and "PYBYTES".
- Add option for invoking "make clean".
- Add option to build for multiple boards at once.
- Add option "--install" to acquire the whole toolchain. Maybe use PlatformIO?
- Add machinery to manipulate files before starting build process, e.g.
  to set "SW_VERSION_NUMBER" within "esp32/pycom_version.h" and
  'mp_hal_stdout_tx_str("MicroPython" ...)' within "lib/utils/pyexec.c".
- Eventually include "MICROPY_BUILD_DATE" from "build/genhdr/mpversion.h".
- Read toolchain paths from configuration file.
- Use real logging module.
- Don't freeze Pycom's "frozen/LTE" to save space.

"""
from glob import glob

import os
import sys
import json
import click
from shell_utils import shell, cd, env, path
from tools.notify import notify_user

__VERSION__ = '0.1.0'

green = lambda text: click.style(text, fg='green')
yellow = lambda text: click.style(text, fg='yellow')
red = lambda text: click.style(text, fg='red')


class MicroPythonVendor:
    Genuine = 'genuine'
    Pycom = 'pycom'


class Artefact:

    def __init__(self, name=None, firmware=None, application=None):
        self.name = name
        self.firmware = firmware
        self.application = application

    @classmethod
    def make(cls, name=None, firmware=None, application=None):
        if os.path.exists(firmware):
            artefact = cls(name=name, firmware=firmware)
        else:
            return
        if os.path.exists(application):
            artefact.application = application
        return artefact

    def to_json(self):
        return json.dumps({'firmware': self.firmware, 'application': self.application})

    def save(self, release_path):
        if self.firmware:
            extension = os.path.splitext(self.firmware)[-1]
            shell(f'mkdir -p "{release_path}/firmware"', silent=True)
            shell(f'cp "{self.firmware}" "{release_path}/firmware/{self.name}{extension}"', silent=True)
        if self.application:
            extension = os.path.splitext(self.application)[-1]
            shell(f'mkdir -p "{release_path}/application"', silent=True)
            shell(f'cp "{self.application}" "{release_path}/application/{self.name}{extension}"', silent=True)


class MicroPythonBuilder:

    def __init__(self,
                 vendor=None, label=None,
                 micropython_path=None, toolchain_path=None, espidf_path=None,
                 architecture=None, board=None, manifest=None, sources=None, pycom_variant=None,
                 verbose=False):
        self.vendor = vendor
        self.label = label
        self.micropython_path = micropython_path
        self.toolchain_path = toolchain_path
        self.espidf_path = espidf_path
        self.architecture = architecture
        self.board = board
        self.manifest = manifest
        self.sources = sources
        self.pycom_variant = pycom_variant
        self.verbose = verbose

        self.pycom_frozen_path = f'{self.micropython_path}/esp32/frozen/Custom'

    def build_genuine(self, manifest):

        click.secho(f'Building {yellow(self.vendor.title())} MicroPython firmware '
                    f'for {yellow(self.architecture)} with manifest file {yellow(self.manifest)}.')

        with env(ESPIDF=self.espidf_path):

            # Build release.
            shell(f'make -j8 --directory=ports/{self.architecture} BOARD={self.board} FROZEN_MANIFEST={manifest}')

            # Find release artefact.
            try:

                # TODO: Put ESP-IDF version into the release name.
                release_board = f'{self.architecture.upper()}-{self.board.replace("_", "-")}'
                release_version = shell(f"""cat {self.micropython_path}/ports/{self.architecture}/build-{self.board}/genhdr/mpversion.h | grep MICROPY_GIT_TAG | cut -d'"' -f2""", capture=True, silent=True).stdout.strip()
                release_label = self.label

                firmware_path = f'{self.micropython_path}/ports/{self.architecture}/build-{self.board}/firmware.bin'
                application_path = f'{self.micropython_path}/ports/{self.architecture}/build-{self.board}/application.elf'
                return Artefact.make(name=f'{release_board}-{release_version}-{release_label}', firmware=firmware_path, application=application_path)
            except:
                pass

    def build_pycom(self):

        click.secho(f'Building {yellow(self.vendor.title())} MicroPython firmware '
                    f'for {yellow(self.architecture)} with frozen modules from {yellow(str(self.sources))}.')

        # Handle frozen modules.
        self.purge_frozen()
        if self.sources:
            self.sync_frozen()

        # Evaluate Pycom VARIANT.
        pycom_variant = 'BASE'
        build_dir = 'build'
        if pycom_variant == 'PYBYTES':
            build_dir = 'build-PYBYTES'

        with env(IDF_PATH=self.espidf_path):

            # Build release.
            shell(f'make -j8 --directory=esp32 BOARD={self.board} VARIANT={pycom_variant} FS=LFS release')

            # Find release artefact.
            try:
                release_board = shell(f"echo '{self.board}' | tr '[IOY]' '[ioy]'", capture=True, silent=True).stdout.strip()
                release_version = shell(f"""cat esp32/pycom_version.h | grep SW_VERSION_NUMBER | tail -n1 | cut -d'"' -f2""", capture=True, silent=True).stdout.strip()
                firmware_path = f'{self.micropython_path}/esp32/{build_dir}/{release_board}-{release_version}.tar.gz'
                application_path = f'{self.micropython_path}/esp32/{build_dir}/{self.board}/release/application.elf'
                return Artefact.make(name=f'{release_board}-{release_version}', firmware=firmware_path, application=application_path)
            except:
                pass

    def purge_frozen(self):

        frozen_path = self.pycom_frozen_path

        if not os.path.exists(frozen_path):
            click.secho(f'{red("ERROR")}: Frozen path {red(frozen_path)} does not exist.')
            sys.exit(2)

        click.secho(f'Purging contents of frozen path {frozen_path}.')
        pattern = f'{frozen_path}/*'
        if glob(pattern):
            shell(f'rm -r {frozen_path}/*')

    def sync_frozen(self):
        frozen_path = self.pycom_frozen_path
        click.secho(f'Copying sources from {yellow(str(self.sources))} to frozen path {frozen_path}.')
        shell(f'rsync -auv --delete --exclude=__pycache__ {" ".join(self.sources)} {frozen_path}')
        shell(f'rm -r {frozen_path}/MicroWebSrv2', check=False, silent=True)

    def build(self):

        if self.label:
            os.environ['MICROPY_LABEL'] = self.label

        if self.verbose:
            os.environ['BUILD_VERBOSE'] = '1'

        python_path = os.path.dirname(sys.executable)
        with path(self.toolchain_path, python_path, prepend=True):
            with cd(self.micropython_path):
                if self.vendor == MicroPythonVendor.Genuine:
                    return self.build_genuine(self.manifest)
                elif self.vendor == MicroPythonVendor.Pycom:
                    return self.build_pycom()
                else:
                    raise NotImplementedError(f'Building MicroPython vendor {yellow(self.vendor)} not implemented yet')


def notify(message):
    title = 'MicroPython Builder'
    notify_user(title, message)


@click.command()
@click.option('--vendor', help='MicroPython vendor (genuine, pycom)')
@click.option('--label', help='String to label this release, e.g. Foobar-42')
@click.option('--micropython', help='Path to MicroPython')
@click.option('--toolchain', help='Path to the compiler toolchain to be added to $PATH')
@click.option('--espidf', help='Path to the Espressif ESP-IDF')
@click.option('--architecture', help='Architecture identifier (esp32)')
@click.option('--board', help='Board identifier.\n'
                              '- genuine/esp32:\n'
                              'GENERIC, GENERIC_D2WD, GENERIC_SPIRAM, TINYPICO\n\n'
                              '- pycom/esp32:\n'
                              'WIPY, LOPY, SIPY, GPY, LOPY4, FIPY')
@click.option('--manifest', help='Path to the MicroPython manifest.py file (genuine)')
@click.option('--sources', help='Paths to copy into frozen folder, comma separated (pycom)')
@click.option('--pycom-variant', help='Pycom VARIANT (BASE, PYBYTES)')
@click.option('--release-path', help='Where to store release artefacts')
@click.option('--verbose', is_flag=True, help='Increase verbosity')
@click.version_option(version=__VERSION__)
@click.help_option()
def main(vendor, label, micropython, toolchain, espidf, architecture, board, manifest, sources, pycom_variant, release_path, verbose):

    notify('Starting build process')

    if manifest:
        manifest = os.path.abspath(manifest)

    if sources:
        sources = sources.split(',')
        here = os.path.abspath(os.path.curdir)
        sources = [os.path.join(here, source) for source in sources]

    builder = MicroPythonBuilder(
        vendor=vendor, label=label,
        micropython_path=micropython, toolchain_path=toolchain, espidf_path=espidf,
        architecture=architecture, board=board,
        manifest=manifest, sources=sources, pycom_variant=pycom_variant,
        verbose=verbose)

    artefact = builder.build()

    if artefact and artefact.firmware:
        notify('Build succeeded')
        click.secho(f'{green("SUCCESS")}: Firmware image building succeeded.')
        print(artefact.to_json())

        if release_path:
            release_path = os.path.abspath(release_path)
            artefact.save(release_path)
            click.secho(f'{green("SUCCESS")}: Artefacts have been saved into {release_path}.')

    else:
        notify('Build failed')
        click.secho(f'{red("WARNING")}: No release artefacts found.')


if __name__ == '__main__':
    main()
