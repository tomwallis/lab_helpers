% test PR670 under matlab.

PR670init('/dev/ttyACM0');
PR670getserialnumber()
res = PR670measspd();
res
PR670close();