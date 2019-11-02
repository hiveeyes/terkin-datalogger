# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3


class BluetoothUuid:
    """

    *****
    About
    *****
    Work around the 128-bit UUID byte swap problem in Android's Bluetooth stack "Bluedroid".

    - https://forum.pycom.io/topic/5335/ble-decoding-service-uuid
    - https://community.hiveeyes.org/t/ble-gatt-auf-esp32-mit-micropython/2371/23


    ************
    Introduction
    ************

    UUID RFC-4122
    =============

    UUIDs are documented in RFC 4122. Here is an extract from that RFC:

    In the absence of explicit application or presentation protocol
    specification to the contrary, a UUID is encoded as a 128-bit object,
    as follows:

    The fields are encoded as 16 octets, with the sizes and order of the
    fields defined above, and with each field encoded with the Most
    Significant Byte first (known as network byte order aka big-endian).
    Note that the field names, particularly for multiplexed fields,
    follow historical practice.

    -- http://howtowriteaprogram.blogspot.com/2009/03/uuid-and-byte-order.html


    Bluetooth
    =========

    However, it looks like the "Supplement to Bluetooth Core Specification page 9 of 37" says:

    > All numerical multi-byte entities and values associated with the
      following data types shall use little-endian byte order.

    -- https://github.com/google/eddystone/issues/138#issuecomment-212332184


    ********
    And now?
    ********

    Testimonials
    ============

    While the "standard" UUID representation is little endian,
    the Android Bluetooth stack "Bluedroid" apparently isn't
    converting from little endian appropriately.
    -- https://stackoverflow.com/questions/35339982/strange-uuid-reversal-from-fetchuuidswithsdp
    -- https://devzone.nordicsemi.com/f/nordic-q-a/5844/why-is-uuid-in-wrong-order
    -- https://devzone.nordicsemi.com/f/nordic-q-a/7306/128-bit-uuid-byte-swap-problem


    If you are on a little-endian system and receive the UUID as per RFC-4122 standard
    (big-endian representation) then yes you'll have to swap bytes on ``time_low``, ``time_mid``,
    and ``time_high_and_version`` in order to use them properly.
    -- https://stackoverflow.com/questions/37711358/how-to-convert-uuid-to-big-endian#comment62896909_37711358


    RFC 4122 may be perfectly clear, but I believe the freedom it permits could cause confusion.
    Here is an example where the default encoding described in RFC 4122 was not adopted:

        Although RFC 4122 recommends network byte order (big-endian) for all fields,
        the PC industry (including the ACPI, UEFI, and Microsoft specifications) has
        consistently used little-endian byte encoding for the first three fields:
        ``time_low``, ``time_mid``, ``time_hi_and_version``. The same encoding,
        also known as wire format, should also be used for the SMBIOS representation
        of the UUID.

    -- http://howtowriteaprogram.blogspot.com/2009/03/uuid-and-byte-order.html


    Background I
    ============
    From Android 4.2, google use Bluedroid stack as its default Bluetooth host stack,
    before android 4.2, its default Bluetooth host stack was Bluez, which is also the
    Linux distribution’s default stack.

    Espressif also incorporated the Bluedroid stack into its ESP-IDF SDK.
    -- https://www.espressif.com/sites/default/files/documentation/esp32_bluetooth_architecture_en.pdf


    Background II
    =============
    Even though Android is the world’s most popular mobile platform, it still
    runs into peculiar problems of non-discoverability of Bluetooth service
    when connected to servers other than the Android server.

    Consider a scenario where a Bluetooth device is configured as a service by
    SDP and Universally Unique Identifier (UUID) is advertised in some order.
    Now, when you start discovering this service on Windows as a discovery
    agent, it will read the configuration in the correct order.

    However, the same action will not happen if the discovery agent is run from
    Android as the discovered UUID gets reversed to what has been advertised.
    For example, Bluetooth service registered on Linux OS with
    UUID as e8e10f95-1a70-4b27-9ccf-02010264e9c8 will be discovered on
    Android OS as c8e96402-0102-cf9c-274b-701a950fe1e8.

    This reversal is done at the hardware level or by the Android Bluetooth SDK—BlueDroid.
    -- https://www.kelltontech.com/kellton-tech-blog/bluetooth-and-its-intricacies-android


    Mitigations
    ===========
    Others also do appropriate workaround by byte-swapping the UUIDs.
    https://gist.github.com/masterjefferson/10922165432ec016a823e46c6eb382e6
    """

    @staticmethod
    def to_bytes_le(uuid):
        """
        uuid2bytes

        Taken from the Pycom user forum. By @jmarcelino.
        https://forum.pycom.io/topic/530/working-with-uuid/2
        """
        import ubinascii
        uuid = uuid.encode().replace(b'-', b'')
        tmp = ubinascii.unhexlify(uuid)
        return bytes(reversed(tmp))

    @staticmethod
    def from_bytes_le(thing):
        """
        Taken from Pycopy's UUID class. By Paul Sokolovsky.

        https://github.com/pfalcon/pycopy-lib/blob/master/uuid/uuid.py#L5-L20
        """
        import ubinascii
        if len(thing) != 16:
            raise ValueError('bytes arg must be 16 bytes long')
        hex = ubinascii.hexlify(bytes(reversed(thing))).decode()
        uuid = '-'.join((hex[0:8], hex[8:12], hex[12:16], hex[16:20], hex[20:32]))
        return uuid
