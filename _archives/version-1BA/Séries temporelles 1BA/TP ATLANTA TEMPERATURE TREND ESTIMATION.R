#entrainement exercice Atlanta temperature 
data = read.table('AvTempAtlanta.txt', header = T)
names(data)
data = data[,-c(1, 14)]
data = as.vector(t(data))
temp = ts(data, start = 1879, frequency = 12)
plot(temp, main = 'Les températures Atlanta', xlab = "Les années", ylab= 'Les températures en Fahreineit' )

#Is there a trend ? 
t = 1:length(temp)
t = (t-min(t))/max(t)
## 1ere méthode Regression linéaire 
temp.lin = lm(temp ~ t)
summary(temp.lin)
lin.fit = ts(temp.lin$fitted.values, start= 1879 , frequency = 12)
lines(lin.fit, lwd = 2 , col = 'yellow')
abline(lin.fit[1],0, lwd = 2 , col = "blue" ) 
## 2eme méthode  moving average 
temp.mvav= ksmooth(t,temp,kernel = 'box' )
temp.fit.mvav = ts(temp.mvav$y , start = 1879, frequency = 12 )
lines(temp.fit.mvav, lwd = 2 , col= 'red') 
abline(temp.mvav$y[1], 0 , lwd = 2 , col = "blue") 

## 3eme méthode Regréssion Polynomiale (quadratique)
t1 = t
t2 = t^2
temp.quad = lm(temp ~ t1 + t2)
summary(temp.quad)
quad.fit = ts(temp.quad$fitted.values, start= 1879 , frequency = 12)
lines(quad.fit, lwd = 2 , col = 'green')
abline(quad.fit[1],0, lwd = 2 , col = "blue" ) 

## 4eme méthode : Local polynomial regression 
temp.loc = loess(temp~t)
temp.loc.fit = ts(fitted(temp.loc), start = 1879 , frequency = 12)
lines(temp.loc.fit, lwd = 2 , col= 'purple') 
abline(temp.loc.fit[1], 0 , lwd = 2 , col = "blue") 

## 5eme méthode : splines regression 
library(mgcv)
gam.spl= gam(temp ~ s(t))
gam.spl.fit = ts(gam.spl$fitted.values,start = 1879, frequency = 12)
lines(gam.spl.fit, lwd = 2 , col = 'orange')
abline(gam.spl.fit[1],0, lwd = 2 , col = "blue" )

##comparaison entre toutes les méthodes. 
all.values = c(lin.fit, temp.fit.mvav, quad.fit, temp.loc.fit, gam.spl.fit)
ylim = c(min(all.values), max(all.values))
ts.plot(lin.fit, lwd = 2 , ylim = ylim , ylab = "temperature", col = 'yellow')
lines(temp.fit.mvav, lwd = 2 , col = "red")
lines(quad.fit, lwd = 2, col = 'green')
lines(temp.loc.fit, lwd= 2, col = 'purple')
lines(gam.spl.fit, lwd= 2 , col = "orange")
legend(x= 1880, y = 64 , legend=c('Linear',"Moving average", 'Quadratique', 'Local poly', 'Splines'), lty = 1, col = c("yellow",'red', 'green', 'purple', "orange"))

#Is there seasonality on Atlanta Temperature 
library(TSA)
##1ere méthode Seasonal mean model
?season()
month = season(temp)
model1 = lm(temp~month)
summary(model1)
model2 = lm(temp~month-1)
summary(model2)
## 2éme méthode sin - cos estimation 
?harmonic
har1 = harmonic(temp,1)
model3 = lm(temp~har1)
summary(model3)
har2 = harmonic(temp,2)
model4 = lm(temp~har2)
summary(model4)
har3 =harmonic(temp,3)
model5 = lm(temp~har3)
summary(model5)
har4 =harmonic(temp,4)
model6 = lm(temp~har4)
summary(model6)
st1 = coef(model2)
st2 = fitted(model4)
st2=fitted(model4)[1:12]
plot(1:12, st1, lwd =2 , col = 'blue', ylab = 'seasonality', xlab = 'month', type= 'l')
lines(1:12, st2, lwd=2, col = 'red')

##  both trend and seasonality 
#1ere méthode parametric estimation
lm.fit= lm(temp~ t1 +t2+ har2)
summary(lm.fit)
residuals = ts(temp- fitted(lm.fit), start = 1879, frequency = 12)
plot(residuals, main = 'residual process')
acf(residuals)
library(tseries)
kpss.test(residuals)
#2eme methode non parametric estimation 
gam.trs.fit = gam(temp ~ s(t)+har2)
diff.gam = ts(temp - fitted(gam.trs.fit), start = 1879, frequency = 12)
plot(diff.gam, col ="red")
(acf(diff.gam))
kpss.test(diff.gam)
