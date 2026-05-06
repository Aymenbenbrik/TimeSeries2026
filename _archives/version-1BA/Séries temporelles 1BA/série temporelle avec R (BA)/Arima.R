phi=c(.7, .2)
beta=0.5
sigma=3
m=100000
set.seed(5)
x=arima.sim(n = m, list(order = c(2,1,1), ar = phi, ma = beta))
plot(x)
acf(x)
y=diff(x)
acf(y)
pacf(y)
auto.arima(x, ic = "aic")
diffx = diff(x)
auto.arima(diffx)
