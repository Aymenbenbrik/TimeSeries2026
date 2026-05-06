set.seed(47)
data = arima.sim(list(ar= c(0.7,-0.2), order= c(2,0,0)), n = 4000)
par(mfrow = c(2,1))
acf(data)
pacf(data)
summary(arima(data, order= c(2,0,0), include.mean = F))
aik = NULL
coef = matrix(0, 5 , 5)
coef
for (i in 1:5) {
  aik[i] = arima(data, order = c(i,0,0), include.mean = F)$aic
  for (j in 1:i){
    coef[i,j] = arima(data,order = c(i,0,0), include.mean= F)$coef[j]
  }
}
plot(aik) 
coef
