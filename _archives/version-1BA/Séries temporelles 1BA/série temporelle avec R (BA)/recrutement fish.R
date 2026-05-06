library(astsa)
help(rec)
par(mfrow = c(1,1))
plot(rec)
acf(rec)
pacf(rec)
mean(rec)
ar.process = rec - mean(rec)
mean(ar.process)
p = 2 
sigma0 = acf(ar.process, type= "covariance",plot= F)$acf[1]
r = NULL
r= matrix(acf(ar.process,plot= F)$acf[2:3], 2, 1) 
R = NULL
R = matrix(1,2,2)
for (i in 1:p) {
  for(j in 1: p) {
    if(i !=j)
      R[i,j] = r[abs(i-j)]
  }
}
phi.hat = matrix(solve(R,r), p,1)
phi_0 = mean(rec) *(1 - sum(phi.hat))
sigmaz = sqrt(sigma0*(1 - sum(phi.hat * r)))
