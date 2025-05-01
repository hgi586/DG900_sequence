import time

import pyvisa
# Python program for the Rigol DG900 series to load a waveform created in software into the 2**24 ( about 16 million)
# locations of that waveform generator . One channel is provided, the other channel can be added
# the program was tested with the DG972 . other Rigol models of that series may need changes
# Each location is 16 bit , 2's complement : max positive value is 32767 , minimum
# negative value is 32768
# A test waveform is provided to be observed with an oscilloscope for accuracy. That waveform can also be visualised
# with a logic analyzer
# the library PyVISA is used : https://pyvisa.readthedocs.io on github : https://github.com/pyvisa/pyvisa
# the command details were found in DG900 series Function/arb waveform Generator programming guide Aug. 2018
rm = pyvisa.ResourceManager()
rigol972 = rm.open_resource('USB0::0x1AB1::0x0643::DG9A241800103::INSTR')
rigol972.write(":SOURce1:APPLy:SEQuence 60000000,3.3,1.65,0")  # 3.3vpp , 1.65 dc offset, 60e6 Samples/s
arbList = []
n = 2**24    # number of samples
# creation of test waveform
for index in range(n):
    if index < 10:
        arbList.append(32768)  # most negative (10)
    elif 10 <= index < 20:
        arbList.append(32767)  # most positive (10)
    elif  index == n-1:
        arbList.append(32767)  # most positive (1)
    else:
        arbList.append(32768)  # most negative
ByteCount = ['#833554432']    # number of bytes total if  n = 2**24 . for smaller numbers see Rigol programming manual
rigol972.write_ascii_values(":SOUR1:TRAC:DATA:DAC16 VOLATILE,END,",
                            ByteCount[:], converter='s')
end = (len(arbList))// 8192    #writes in groups of 8192 samples
for i in range(0, end - 1):
    rigol972.write_binary_values(":SOUR1:TRAC:DATA:DAC16 VOLATILE,CON,",
                             arbList[i*8192:(i+1)*8192], datatype='H', is_big_endian=False)
    time.sleep(0.05)            #prevent io timeout
rigol972.write_binary_values(":SOUR1:TRAC:DATA:DAC16 VOLATILE,END,",
                             arbList[(end-1)*8192:end*8192], datatype='H', is_big_endian=False)





