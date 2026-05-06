library(astsa)

# read data to R variable
birth.data<-read.csv("C:/Users/aymen/Downloads/daily-total-female-births.csv")

# pull out number of births column
number_of_births<-birth.data$Births

# use date format for dates
birth.data$Date <- as.Date(birth.data$Date, "%m/%d/%Y")
number_of_births = ts(log(number_of_births), start = 1959 , frequency =  365)
plot(number_of_births)
num = diff(number_of_births)
plot(num)
Box.test(number_of_births, lag = log(length(number_of_births)))
library(tseries)
kpss.test(num)
acf(num)
pacf(num)


model1<-arima(number_of_births, order=c(0,1,1))
SSE1<-sum(model1$residuals^2)
model1.test<-Box.test(model1$residuals, lag = log(length(model1$residuals)))


model2<-arima(number_of_births, order=c(0,1,2))
SSE2<-sum(model2$residuals^2)
model2.test<-Box.test(model2$residuals, lag = log(length(model2$residuals)))

model3<-arima(number_of_births, order=c(7,1,1))
SSE3<-sum(model3$residuals^2)
model3.test<-Box.test(model3$residuals, lag = log(length(model3$residuals)))

model4<-arima(number_of_births, order=c(7,1,2))
SSE4<-sum(model4$residuals^2)
model4.test<-Box.test(model4$residuals, lag = log(length(model4$residuals)))

df<-data.frame(row.names=c('AIC', 'SSE', 'p-value'), c(model1$aic, SSE1, model1.test$p.value), 
               c(model2$aic, SSE2, model2.test$p.value), c(model3$aic, SSE3, model3.test$p.value),
               c(model4$aic, SSE4, model4.test$p.value))
colnames(df)<-c('Arima(0,1,1)','Arima(0,1,2)', 'Arima(7,1,1)', 'Arima(7,1,2)')

df
library(forecast)
auto.arima(number_of_births)
model_fin = sarima(number_of_births, 0,1,2,0,0,0)

res = model_fin$fit$residuals


library(FinTS)

ArchTest(res)

# Installer si nécessaire
install.packages("rugarch")

library(rugarch)



# Exemple : rendements simulés
set.seed(123)
r <- rnorm(500, mean = 0, sd = 1)

# Spécification GARCH(1,1)
spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0)),
  distribution.model = "norm"
)

# Ajustement
fit <- ugarchfit(spec = spec, data = res)

# Résumé
fit

# Prévision de volatilité
fcst <- ugarchforecast(fit, n.ahead = 5)
sigma(fcst)
