set.seed(2016)
z = rnorm(1000)
phi = 1
x = NULL
x[1]= z[1]
for ( t in 2:1000){ x[t] = z[t] + phi*x[t-1]}
x.ts = ts(x)
par(mfrow = c(2,1))
plot(x.ts, main = 'AR(1) time series on white noise phi = 1')
x.acf= acf(x.ts, main = 'AR(1) time series on white noise phi = 0.4')
