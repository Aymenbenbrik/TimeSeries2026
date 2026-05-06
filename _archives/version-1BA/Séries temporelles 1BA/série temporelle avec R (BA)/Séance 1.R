require(astsa)
help(astsa)
help(jj)
plot(jj, type = "o", main = "Johnson & Johnson quaterly earning per share", ylab = "Earning", xlab = "Years")

help(flu)
plot(flu, main = "Monthly Pneumonia and Influenza Deaths in US", ylab = 'Number of deaths per 10.000 people', xlab ="Months")

plot(globtemp, main ="Global mean Land-Ocean deviations from average temperature of 1951-1980", ylab = 'Temperature', xlab = 'Years')
help("globtempl")
plot(globtempl, main = "Global mean land deviation from average temperature from 1951 1980", ylab = "Temperature", xlab = "Years")

help(star)
plot(star,main= "the magnitude of a star taken at midnight for 600 consecutif days", ylab = 'Magnitude', xlab = "days")

purely_random_process= ts(rnorm(100))
plot(purely_random_process)
print(purely_random_process)
(acf(purely_random_process, type = "covariance"))
(acf(purely_random_process,main =' correlogram of a purely random process'))

x = NULL
x[1]= 0 
for (i in 2 :1000){ x[i]= x[i-1] + rnorm(1)}
print(x)
class(x)
random_walk = ts(x)
class(random_walk)
plot(random_walk, main = 'a random walk', xlab = 'days', col = 'blue', lwd = 2)
acf(random_walk)
diff(random_walk)
plot(diff(random_walk))
acf(diff(random_walk))
mean(diff(random_walk))
sd(diff(random_walk))
