noise = rnorm(10000)
ma_2 = NULL
for(i in 3:10000)
{ma_2[i]= noise[i]+ 0.7*noise[i-1]+0.2*noise[i-2]}

moving_average_process = ts(ma_2[3:1000])
class(moving_average_process)
par(mfrow = c(2,1) )
plot(moving_average_process, main ='simulation of a MA(2)')
(acf(moving_average_process))
