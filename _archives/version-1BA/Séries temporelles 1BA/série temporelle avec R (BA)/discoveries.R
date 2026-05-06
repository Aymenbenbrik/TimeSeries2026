library(astsa)
?discoveries
par(mfrow= c(1,1))
hist(discoveries)
plot(discoveries)
stripchart(discoveries, method = "stack", offset =  0.25, at=0.2)

stripchart(discoveries, method = "stack", offset =0.25, pch = 3, at = 0.15)
plot(discoveries)
disc = discoveries - mean(discoveries)
plot(disc)
acf(disc)
pacf(disc)

aik = NULL
aik = matrix(1,6,6)
for (i in 0:5) {
  for (j in 0:5){
    aik[i+1,j+1] = arima(disc, order = c(i,0,j), include.mean = F)$aic
    }
}
aik 
plot(aik)
min(aik)
library(forecast)
auto.arima(disc,d=0, , ic= "aic", approximation = T)
auto.arima(disc,d=0, , ic= "bic", approximation = T)
auto.arima(disc,d=0, , ic= "aic", approximation = F)
