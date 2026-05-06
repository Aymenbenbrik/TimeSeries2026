data= read.table("AvTempAtlanta.txt", header= T)
names(data)
View(data)

data= data[,-c(1,14)]
View(data)
help(as.vector)
data = as.vector(t(data))
View(data)
temp = ts(data, start = 1879, frequency = 12)
class(temp)
ts.plot(temp,ylab = 'temperature')

#estimation of the trend 

##create equally spaced time points for fitting trend 
time.pts = c(1:length(temp))
time.pts = c(time.pts - min(time.pts))/max(time.pts)
time.pts













##Fit a moving average 
help(ksmooth)
mav.fit = ksmooth(time.pts, temp, kernel= "box")
temp.fit.mav = ts(mav.fit$y, start = 1879,frequency = 12)











## Is there a trend ? 
ts.plot(temp, ylab= 'temperature')
lines(temp.fit.mav, lwd = 2, col = 'purple')
abline(temp.fit.mav[1], 0, lwd = 2, col = 'blue')
help(abline)

## fit a parametric quadratic polynomial 
x1 = time.pts
x2 = time.pts^2
lm.fit=lm(temp ~ x1 + x2)
summary(lm.fit)
## Is there a trend 
temp.fit.lm = ts(fitted(lm.fit), start = 1879, frequency = 12)
ts.plot(temp, ylab = 'temperature') 
lines(temp.fit.lm, lwd = 2, col= 'green')
abline(temp.fit.lm[1], 0, lwd = 2 , col = 'blue')

##Local polynomial trend estimation 
loc.fit = loess(temp~time.pts)
temp.loc.fit = ts(fitted(loc.fit), start = 1879, frequency = 12)
## Splines trend estimation 
library(mgcv)
gam.fit= gam(temp ~ s(time.pts))
temp.fit.gam = ts(fitted(gam.fit), start= 1879, frequency = 12)
#Is there a trend ? 
ts.plot(temp , ylab = "temperature")
lines(temp.loc.fit, lwd= 2 , col = "red")
lines(temp.fit.gam, lwd = 2 , col = 'yellow')
abline(temp.loc.fit[1], 0, lwd = 2, col = "blue")

#comparing all estimated trend 
all.val = c(temp.fit.mav, temp.fit.mav, temp.loc.fit, temp.fit.gam)
ylim = c(min(all.val), max(all.val))
ts.plot(temp.fit.mav, lwd = 2 , ylim = ylim , ylab = "temperature", col = 'blue')
lines(temp.fit.lm, lwd = 2 , col = "green")
lines(temp.loc.fit, lwd = 2, col = 'red')
lines(temp.fit.gam, lwd= 2, col = 'yellow')
#legend(x= 1900, y = 64 , legend=c('MAV',"LM", 'LOC', 'SPLINE'), lty = 1, col = c("blue",'green', 'red', 'yellow'))

##Is there a seasonality 

library(TSA)
##estimation seasonality with seasoanl means model 
month = season(temp)
model1 = lm(temp~month)
summary(model1)
model2 = lm(temp~month-1)
summary(model2)
##estimation of seasonality with cosine sin model 
har1 = harmonic(temp, 1)
model3 = lm(temp~har1)
summary(model3)
har2= harmonic(temp, 2)
model4 = lm(temp~har2)
summary(model4)
## Seasonal Means Model 
st1 = coef(model2)
st2 = fitted(model4)[1:12]
plot(1:12,st1, lwd = 2, type = "l", xlab = 'month', ylab='Seasonality')
lines(1:12, st2, lwd= 2 ,col = 'blue')


## Seasonality and trend estimation parametric estimation 
lm.fit2 = lm(temp~x1 + x2 + har2) 
summary(lm.fit2)
dif.fit.lm = ts(temp - fitted(lm.fit2), start = 1879, frequency = 12)
ts.plot(dif.fit.lm, ylab = 'Residual Process')
## fit a non parametric estimation for trend and linear model for seasonality 
gam.fit2 = gam(temp ~ s(time.pts)+har2)
dif.gam.fit2 = ts(temp - fitted(gam.fit2), start = 1879 , frequency = 12 ) 
lines(dif.gam.fit2, col= "blue")

## Acf 
par(mfrow = c(3,1))
acf(temp,lag.max = 4*12, main ='')
#Acf for the residual process 
acf(dif.fit.lm, lag.max = 4*12)
acf(dif.gam.fit2, lag.max = 4*12)
