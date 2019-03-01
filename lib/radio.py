def start_wifi(known_nets):
    print("setting up wifi")

    import machine
    import os

    # uart = machine.UART(0, 115200) # disable these two lines if you don't want serial access
    # os.dupterm(uart)

    if True or machine.reset_cause() != machine.SOFT_RESET: # needed to avoid losing connection after a soft reboot
        from network import WLAN
        wl = WLAN()

        # save the default ssid and auth
        original_ssid = wl.ssid()
        original_auth = wl.auth()

        wl.mode(WLAN.STA)

        available_nets = wl.scan()
        nets = frozenset([e.ssid for e in available_nets])

        known_nets_names = frozenset([e[0] for e in known_nets])
        net_to_use = list(nets & known_nets_names)

        try:
            net_to_use = net_to_use[0]
            pwd = dict(known_nets)[net_to_use]
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            print(net_to_use, sec, pwd)
            success = wl.connect(net_to_use, (sec, pwd), timeout=10000)
            while not wl.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            return success
        except:
            print("could not connect wifi, set AP mode on")
            wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
