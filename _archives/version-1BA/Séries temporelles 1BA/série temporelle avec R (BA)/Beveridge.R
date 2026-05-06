library(tseries)
data(bev)
bev
class(bev)
plot(bev)
beveridge = bev 
beveridge
?bev
plot(bev)
beveridge.ma = filter(beveridge, rep(1/31, 31), sides = 2)
lines(beveridge.ma, col = 'red')
par(mfrow = c(3,1))
Y = beveridge / beveridge.ma
plot(Y, ylab = 'Scaled price')
acf(na.omit(Y) )
pacf(na.omit(Y))
ar(na.omit(Y), order.max = 5)