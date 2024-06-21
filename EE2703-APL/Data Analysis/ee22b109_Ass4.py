import numpy as np
from scipy.optimize import curve_fit

def poly_func(fdata, A1, A2, A3, A4, A5, A6, A7, P1, P2, P3, P4, P5, P6, P7):
    fgre = fdata[0] / 340
    ftoefl = fdata[1] / 120
    funi_rat = fdata[2] / 5
    fsop = fdata[3] / 5
    flor = fdata[4] / 5
    fcgpa = fdata[5] / 10
    frsch = fdata[6]
    return A1*fgre**P1 + A2*ftoefl**P2 + A3*funi_rat**P3 + A4*fsop**P4 + A5*flor**P5 + A6*fcgpa**P6 + A7*frsch**P7

def lin_func(fdata, C1, C2, C3, C4, C5, C6, C7):
    fgre = fdata[0] / 340
    ftoefl = fdata[1] / 120
    funi_rat = fdata[2] / 5
    fsop = fdata[3] / 5
    flor = fdata[4] / 5
    fcgpa = fdata[5] / 10
    frsch = fdata[6]
    return C1*fgre + C2*ftoefl + C3*funi_rat + C4*fsop + C5*flor + C6*fcgpa + C7*frsch

data = np.loadtxt('Admission_Predict_Ver1.1.csv', delimiter=',', skiprows=1, usecols=(1, 2, 3, 4, 5, 6, 7))
ch_ad = np.loadtxt('Admission_Predict_Ver1.1.csv', delimiter=',', skiprows=1, usecols=8)
data = np.transpose(data)

#Finding coefficients for Linear Model
(c1,c2,c3,c4,c5,c6,c7), _ = curve_fit(lin_func, data, ch_ad, bounds = ((0,0,0,0,0,0,0),(1,1,1,1,1,1,1)))

lin_chance = lin_func(data, c1, c2, c3, c4, c5, c6, c7)
lin_error = np.average(abs((ch_ad - lin_chance)*100/ch_ad))

print("c1 =", c1, ", c2 =", c2, ", c3 =", c3, ", c4 =", c4, ", c5 =", c5, ", c6 =", c6, ", c7 =", c7)
print("error = ", lin_error, "%")


#Finding coefficients for Polynomial Model
(a1,a2,a3,a4,a5,a6,a7,p1,p2,p3,p4,p5,p6,p7), _ = curve_fit(poly_func, data, ch_ad, bounds = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,1,1,1,1,1,1,10,10,10,10,10,10,10)))

poly_chance = poly_func(data, a1, a2, a3, a4, a5, a6, a7, p1, p2, p3, p4, p5, p6, p7)
poly_error = np.average(abs((ch_ad - poly_chance)*100/ch_ad))

print("a1 =", a1, ", a2 =", a2, ", a3 =", a3, ", a4 =", a4, ", a5 =", a5, ", a6 =", a6, ", a7 =", a7)
print("p1 =", p1, ", p2 =", p2, ", p3 =", p3, ", p4 =", p4, ", p5 =", p5, ", p6 =", p6, ", p7 =", p7)
print("error = ", poly_error, "%")
