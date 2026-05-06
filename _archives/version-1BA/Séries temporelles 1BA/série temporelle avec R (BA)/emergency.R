#reading data 
edvoldata = read.csv("EGDailyVolume.csv", header= T) 
class(edvoldata)
#process dates
year=edvoldata$Year
month= edvoldata$Month
day= edvoldata$Day
datemat = cbind(as.character(day),as.character(month), as.character(year))
paste.dates = function(date){
  day = date[1]; month = date[2]; year = date[3] 
return(paste(day, month,year, sep = "/"))
  }
dates = apply(datemat, 1 , paste.dates)
dates = as.Date(dates, format = "%d/ %m/%Y")

##Plot time serie
library(ggplot2)
??ggplot
