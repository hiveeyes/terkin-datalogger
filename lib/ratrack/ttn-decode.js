function Decoder(bytes, port) {

  var decoded = {};
  var str = '';
  var length = 0;
  for (var i = 0; i < bytes.length-1; i += 1)
    str += (bytes[i] + ',') ;
    length = i;
  str += bytes[length];

  decoded.raw = bytes;
  decoded.hexstring = str;
  decoded.latitude = (parseInt(bytes[0] + (bytes[1] << 8) + (bytes[2] << 16 )) / 10000) - 90;
  decoded.latitude = Math.round(decoded.latitude * 1000000) / 1000000;
  decoded.longitude = (parseInt(bytes[3] + (bytes[4] << 8) + (bytes[5] << 16 )) / 10000) - 180;
  decoded.longitude = Math.round(decoded.longitude * 1000000) / 1000000;
  //decoded.altitude = (bytes[6] + (bytes[7] << 8) )/ 10;
  //decoded.hdop = bytes[8] / 10;
  decoded.roll = (parseInt(bytes[6] + (bytes[7] << 8) + (bytes[8] << 16)) / 10000) - 360;
  decoded.roll = Math.round(decoded.roll * 1000000) / 1000000;
  decoded.pitch = (parseInt(bytes[9] + (bytes[10] << 8) + (bytes[11] << 16)) / 10000) - 360;
  decoded.pitch = Math.round(decoded.pitch * 1000000) / 1000000;
  decoded.battery = (parseInt(bytes[12]) + (bytes[13] << 8) + (bytes[14] << 16)) / 10000;
  decoded.cog = (parseInt(bytes[15] + (bytes[16] << 8) + (bytes[17] << 16)) / 1000) - 999;
  decoded.cog = Math.round(decoded.cog * 1000000) / 1000000;
  decoded.speed = (parseInt(bytes[18] + (bytes[19] << 8) + (bytes[20] << 16)) / 1000) - 999;
  decoded.speed = Math.round(decoded.speed * 1000000) / 1000000;
  decoded.temp = (parseInt(bytes[21] + (bytes[22] << 8) + (bytes[23] << 16)) / 1000) - 999;
  decoded.temp = Math.round(decoded.temp * 1000000) / 1000000;
  decoded.pressure = (parseInt(bytes[24] + (bytes[25] << 8) + (bytes[26] << 16)) / 1000) - 999;
  decoded.pressure = Math.round(decoded.pressure * 1000000) / 1000000;
  return decoded;
}