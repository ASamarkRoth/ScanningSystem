import numpy as np
import matplotlib.pyplot as plt

#http://ijcps.org/admin/php/uploads/384_pdf.pdf
#http://dtic.mil/dtic/tr/fulltext/u2/a278139.pdf


#linear mass absorption coefficients
#0.6 MeV = 0.1 cm^2/g
mu_W = 18*0.1 # cm^1

#After distance of 50 mm, i.e. at the end of collimator, with 1.5 GBq source:

activity = 1.5e9*np.exp(-mu_W*5.7)

print("Activity = ", activity)
d = 25
RD = 2.5

Omega1 = 2*np.pi*(1 - 1/(np.sqrt(1+RD**2/d**2)))
print("Omega1 = ", Omega1)
Omega2 = RD**2/(4*d**2)
print("Omega2 = ", Omega2)


mu_Pb = 7.7602 #cm^-1
mu_Cu = 31.6936
#for second source at 0.6 MeV
mu_Pb = 0.12*11.34 #cm^-1
mu_Cu = 0.076*8.96

x = np.linspace(0,2)

IoverI0_Pb = np.exp(-mu_Pb*x)
IoverI0_Cu = np.exp(-mu_Cu*x)
plt.plot(x, IoverI0_Pb)
plt.plot(x, IoverI0_Cu)
plt.show()
plt.close()

#Intensity from 1 mm diameter circular hole
I_slit_Pb = np.divide(0.5**2, 4*x**2)*IoverI0_Pb
I_slit_Cu = np.divide(0.5**2, 4**x**2)*IoverI0_Cu

plt.plot(x, I_slit_Pb)
plt.plot(x, I_slit_Cu)
plt.show()
plt.close()

I_have = 1e3 #1 kHz :)

I0_Pb = np.divide(I_have, I_slit_Pb)
I0_Cu = np.divide(I_have, I_slit_Cu)

plt.plot(x, I0_Pb)
plt.plot(x, I0_Cu)
plt.show()
plt.close()

