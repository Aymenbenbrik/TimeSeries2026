help(sleep)
class(sleep) 
dim(sleep)
names(sleep)
sleep
plot(extra~group,data= sleep, lwd=2 , col = 'blue', main = 'extra hours of sleep by group')
summary(sleep)
#utiliser les variables de jeu de données sleep directement
attach(sleep)
extra
#créer deux vecteurs différents pour chaque médicament 
extra.1 = extra[group==1]
extra.2 = extra[group==2]
#test d'hypothèses 
t.test(extra.1,extra.2,paired = TRUE, alternative = "two.sided")
