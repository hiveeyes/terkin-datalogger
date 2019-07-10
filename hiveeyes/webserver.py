import machine
import time
import binascii

from microWebSrv import MicroWebSrv
from microDNSSrv import MicroDNSSrv

#import sensors
from hiveeyes.sensor_ds18x20 import DS18X20Sensor

from main import BobDatalogger

#from config import Config

#_config = Config()

# To not run into trouble with CORS while developing
_headers = {'Access-Control-Allow-Origin': '*'}

@MicroWebSrv.route('/restart')
def restart(httpClient, httpResponse):
    # log.info('In Route')
    # datalogger = BobDatalogger.getInstance()
    # log.info('Got DataLogger')
    # datalogger.read_sensors()
    # log.info('Read sensors')
    c = BobDatalogger.getInstance()
    c.read_sensors()
    machine.reset()


##############################################################################
# Routes for sensor readings                                                 #
##############################################################################

@MicroWebSrv.route('/api/sensors/<sensor>')
def measure_ds1820(httpClient, httpResponse, routeArgs):
    sensor = routeArgs['sensor']
    #if hasattr(sensors, sensor):

        # Read sensor DS1820
    if sensor == 'ds1820':
        c = BobDatalogger.getInstance()
        alldata = c.read_sensors()
        data = foodict = {k: v for k, v in alldata.items() if k.startswith('temperature')}



        ##############
        # ds = sensors.ds1820
        # for rom in ds.roms:
        #     ds.start_conversion(rom=rom)
        # time.sleep_ms(750)
        # data = {}
        # for rom in ds.roms:
        #     data[binascii.hexlify(rom).decode('utf-8')] = ds.read_temp_async(rom=rom)

    # # Read sensor HX711
    # elif sensor == 'hx711':
    #     hx = sensors.hx711
    #     data = {'weight': hx.read_average(times=5)}
    #
    # # Read sensor BME280
    # elif sensor == 'bme280':
    #     bme = sensors.bme280
    #     data = {}
    #     (data['t'],
    #     data['p'],
    #     data['h']) = bme.read_compensated_data()

    return httpResponse.WriteResponseJSONOk(obj=data, headers=_headers)
    #else:
    #    return httpResponse.WriteResponseJSONError(404)

#
# ##############################################################################
# # Routes for working with the config                                         #
# ##############################################################################
#
# @MicroWebSrv.route('/api/config')
# def get_config(httpClient, httpResponse):
#     return httpResponse.WriteResponseJSONOk(obj=_config.data, headers=_headers)
#
# @MicroWebSrv.route('/api/config/<section>/<subsection>', 'GET')
# def get_config_subsection(httpClient, httpResponse, routeArgs):
#     section = routeArgs['section']
#     subsection = routeArgs['subsection']
#
#     data = _config.get_subsection(section, subsection)
#     if data is None:
#         return httpResponse.WriteResponseJSONError(404)
#     else:
#         return httpResponse.WriteResponseJSONOk(
#             obj=data,
#             headers=_headers)
#
# @MicroWebSrv.route('/api/config/<section>/<subsection>', 'POST')
# def post_config_subsection(httpClient, httpResponse, routeArgs):
#     section = routeArgs['section']
#     subsection = routeArgs['subsection']
#     form_data = httpClient.ReadRequestContentAsJSON()
#     _config.set_subsection(section, subsection, form_data)
#     return httpResponse.WriteResponseJSONOk(
#         obj={'status': 'saved'},
#         headers=_headers)
#
# @MicroWebSrv.route('/api/config/<section>/<subsection>', 'OPTIONS')
# def options_config(httpClient, httpResponse, routeArgs):
#     headers = {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type'}
#     return httpResponse.WriteResponseOk(
#         headers = headers,
#         contentType = "text/plain",
#         contentCharset = "UTF-8",
#         content="")
#
# @MicroWebSrv.route('/api/log', 'GET')
# def get_logfile(httpClient, httpResponse):
#     reset_causes = {
#         machine.PWRON_RESET: 'PWRON', # Press reset button on FiPy
#         machine.HARD_RESET: 'HARD',
#         machine.WDT_RESET: 'WDT', # Upload and restart from USB or machine.reset()
#         machine.DEEPSLEEP_RESET: 'DEEPSLEEP',
#         machine.SOFT_RESET: 'SOFT',
#         machine.BROWN_OUT_RESET: 'BROWN_OUT'
#     }
#     data = {}
#     data['reset_cause'] = reset_causes[machine.reset_cause()]
#     try:
#         with open('/sd/hiverizelog/logging.csv') as f:
#             data['logfile'] = f.read()
#     except OSError as err:
#         data['logfile'] = "Could not open logfile: {}".format(err)
#     return httpResponse.WriteResponseJSONOk(
#         obj=data,
#         headers=_headers)


mws = MicroWebSrv()
mws.SetNotFoundPageUrl("http://hiverize.wifi")
MicroDNSSrv.Create({ '*' : '192.168.4.1' })
