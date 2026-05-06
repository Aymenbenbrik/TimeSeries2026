n = 10000
sigma = 4 
phi1 = 1/3
phi2 = 1/2
phi3 = 7/100
set.seed(2017)
r= NULL
ar.process = arima.sim(n , model = list(ar = c(phi1,phi2,phi3)), sd =sigma)
plot(ar.process)
ar.process[1:5]
r[1:3]=acf(ar.process, plot=F)$acf[2:4]
R = NULL
R = matrix(1,3,3)
R[1,2]= r[1]
R[2,1]= r[1]
R[1,3] = r[2]
R[3,1]= r[2]
R[2,3]= r[1]
R[3,2] = r[1]
b = matrix(r, 3,1)
phi.hat = matrix(solve(R,b),3,1)
c0 = acf(ar.process, type = "covariance", plot = F)$acf[1]
var.hat = c0 * (1 - sum(phi.hat*r))
par(mfrow=c(3,1))
plot(ar.process, main = "AR 2 simulated")
acf(ar.process, main = 'ACF')
pacf(ar.process, main= "PACF")
