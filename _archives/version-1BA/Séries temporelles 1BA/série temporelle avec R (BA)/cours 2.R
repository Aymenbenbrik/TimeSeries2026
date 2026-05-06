##Simulation normal/exponential white noise
w1= rnorm(1000,0,1)
w2 = rexp(1000,1)
mean(w1)
mean(w2)
sd(w1)
sd(w2)
w1 = (w1- mean(w1))/sd(w1)
w1 = (w1- mean(w1))/sqrt(var(w1))
mean(w1)
sd(w1)
w2 = (w2- mean(w2))/sqrt(var(w2))
mean(w2)
sd(w2)
w1 = ts(w1,start = 1, deltat = 1)
w2= ts(w2, start = 1 , deltat = 1)
par(mfrow = c(2,2))
ts.plot(w1, main ='Normal')
ts.plot(w2, main = 'Exponential')
(acf(w1,main = 'Autocorrelation1'))
(acf(w2,main = 'Autocorrelation 2'))

## simulation of ma 2 
w1 = rnorm(502)
w2 = rexp(502)-1
a = c(1, -.5, .2)
a1 = c(1,.5,.2)
ma2.11= filter(w1, filter= a , side =1 ) 
ma2.11 = ma2.11[3:502]
ma2.12= filter(w1, filter= a1 , side =1 ) 
ma2.12 = ma2.12[3:502]
ma2.21= filter(w2, filter= a , side =1 ) 
ma2.21 = ma2.21[3:502]
ma2.22= filter(w2, filter= a1 , side =1 ) 
ma2.22 = ma2.22[3:502]
par(mfrow= c(2,2))
acf(ma2.11, main= "Normal 1")
acf(ma2.12, main= "Normal 2")
acf(ma2.11, main= "Exponential 1")
acf(ma2.11, main= "Exponential 2")

#ma non stationnary 
w1 = rnorm(502)
a4 = c(1, -.2, .8, 1.2)
ma3.4= filter(w1*(2*(1:502)+.5), filter= a4 , side =1 ) 
ma3.4 = ma3.4[4:502]
par(mfrow = c(1,1))
ts.plot(ma3.4, start = 1 )
acf(ma3.4, main= " ")

## Ar(2) non stationnary 
w2 = rnorm(1500)
a2 = c(0.8,0.2)
ar2 = filter(w2,filter = a2, method= 'recursive')
plot(ar2)
acf(ar2)

## Ar(1) stationnary 
w2 = rnorm(1500)
a1 = 0.5
ar1= filter(w2, filter = a1, method = 'recursive')
par(mfrow = c(2,2))
plot(ar1)
acf(ar1)
