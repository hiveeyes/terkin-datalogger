# -*- coding: utf-8 -*-
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys


def notify_user(title, text):

    if sys.platform == 'linux':
        # https://pypi.org/project/py-notifier/#description
        # https://github.com/YuriyLisovskiy/pynotifier
        try:
            from pynotifier import Notification
            Notification(
                title=title,
                description=text,
                duration=5,  # Duration in seconds
                urgency=Notification.URGENCY_NORMAL
            ).send()
        except:
            pass

    elif sys.platform == 'darwin':
        try:
            # https://pypi.org/project/pync/
            import pync
            pync.notify(text, title=title)
        except:
            try:
                # https://stackoverflow.com/questions/17651017/python-post-osx-notification/41318195#41318195
                os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))
            except:
                pass

    elif sys.platform.startswith('win'):
        # https://github.com/malja/zroya
        # https://malja.github.io/zroya/
        # https://www.devdungeon.com/content/windows-desktop-notifications-python
        try:
            import zroya
            zroya.init(title, "a", "b", "c", "d")
            t = zroya.Template(zroya.TemplateType.Text1)
            t.setFirstLine(text)
            zroya.show(t)
        except:
            pass


if __name__ == '__main__':

    message = sys.argv[1]
    status = ''
    try:
        status = sys.argv[2]
    except:
        pass

    title = 'Terkin Pinocchio'
    # title = '{} {}'.format(title, status)
    message = '{}: {}'.format(status, message)

    # Send desktop notification.
    notify_user(title, message)
    sys.exit(0)
