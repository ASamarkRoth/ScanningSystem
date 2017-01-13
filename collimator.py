import numpy as np
import matplotlib.pyplot as plt

#http://ijcps.org/admin/php/uploads/384_pdf.pdf
#http://dtic.mil/dtic/tr/fulltext/u2/a278139.pdf

#linear mass absorption coefficients
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

