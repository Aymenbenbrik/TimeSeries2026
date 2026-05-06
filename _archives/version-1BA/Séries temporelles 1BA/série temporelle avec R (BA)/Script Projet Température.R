# Lire le fichier texte contenant les températures moyennes d’Atlanta
data = read.table("AvTempAtlanta.txt", header = T)

# Afficher les noms des colonnes du tableau
names(data)

# Ouvrir les données dans le viewer pour les inspecter visuellement
View(data)

# Supprimer les colonnes 1 et 14 (souvent année et moyenne annuelle)
data = data[,-c(1,14)]

# Vérifier le tableau après suppression des colonnes
View(data)

# Ouvrir l’aide de la fonction as.vector
help(as.vector)

# Transposer la matrice puis la transformer en vecteur
# t(data) : transpose lignes/colonnes
# as.vector : transforme la matrice en un seul vecteur
data = as.vector(t(data))

# Visualiser le vecteur obtenu
View(data)

# Créer une série temporelle mensuelle
# start = 1879 : la série commence en 1879
# frequency = 12 : 12 observations par an (mensuel)
temp = ts(data, start = 1879, frequency = 12)

# Vérifier la classe de l’objet (doit être "ts")
class(temp)

# Tracer la série temporelle
ts.plot(temp, ylab = 'temperature')

# --------------------------------------------------
# ESTIMATION DE LA TENDANCE
# --------------------------------------------------

# Créer des points de temps régulièrement espacés
time.pts = c(1:length(temp))

# Normaliser le temps entre 0 et 1
# Cela améliore la stabilité des modèles polynomiaux
time.pts = c(time.pts - min(time.pts))/max(time.pts)

# Afficher les points de temps
time.pts


# --------------------------------------------------
# Estimation de la tendance par moyenne mobile
# --------------------------------------------------

# Aide de la fonction ksmooth
help(ksmooth)

# Appliquer un lissage par noyau (kernel smoothing)
# kernel="box" correspond à une moyenne mobile
mav.fit = ksmooth(time.pts, temp, kernel = "box")

# Convertir les valeurs lissées en série temporelle
temp.fit.mav = ts(mav.fit$y, start = 1879, frequency = 12)


# --------------------------------------------------
# Visualiser la tendance estimée
# --------------------------------------------------

# Tracer la série originale
ts.plot(temp, ylab = 'temperature')

# Ajouter la tendance estimée par moyenne mobile
lines(temp.fit.mav, lwd = 2, col = 'purple')

# Tracer une ligne horizontale au niveau de la première valeur
# Sert de référence pour voir si une tendance existe
abline(temp.fit.mav[1], 0, lwd = 2, col = 'blue')

# Aide de la fonction abline
help(abline)


# --------------------------------------------------
# Estimation de la tendance par régression polynomiale
# --------------------------------------------------

# Variable temps
x1 = time.pts

# Temps au carré (trend quadratique)
x2 = time.pts^2

# Ajuster un modèle linéaire avec tendance quadratique
lm.fit = lm(temp ~ x1 + x2)

# Afficher le résumé du modèle
summary(lm.fit)


# Vérifier la tendance estimée

# Valeurs ajustées du modèle
temp.fit.lm = ts(fitted(lm.fit), start = 1879, frequency = 12)

# Tracer la série originale
ts.plot(temp, ylab = 'temperature')

# Ajouter la tendance estimée
lines(temp.fit.lm, lwd = 2, col = 'green')

# Ligne horizontale de référence
abline(temp.fit.lm[1], 0, lwd = 2, col = 'blue')


# --------------------------------------------------
# Estimation non paramétrique de la tendance (LOESS)
# --------------------------------------------------

# Ajuster une régression locale
loc.fit = loess(temp ~ time.pts)

# Extraire la tendance estimée
temp.loc.fit = ts(fitted(loc.fit), start = 1879, frequency = 12)


# --------------------------------------------------
# Estimation de la tendance par splines (GAM)
# --------------------------------------------------

# Charger le package mgcv
library(mgcv)

# Ajuster un modèle GAM avec spline
gam.fit = gam(temp ~ s(time.pts))

# Valeurs ajustées
temp.fit.gam = ts(fitted(gam.fit), start = 1879, frequency = 12)


# Visualiser les tendances estimées

ts.plot(temp, ylab = "temperature")

# tendance LOESS
lines(temp.loc.fit, lwd = 2, col = "red")

# tendance spline
lines(temp.fit.gam, lwd = 2, col = 'yellow')

# ligne horizontale de référence
abline(temp.loc.fit[1], 0, lwd = 2, col = "blue")


# --------------------------------------------------
# Comparaison des différentes tendances
# --------------------------------------------------

# Combiner toutes les tendances estimées
all.val = c(temp.fit.mav, temp.fit.mav, temp.loc.fit, temp.fit.gam)

# Définir limites du graphique
ylim = c(min(all.val), max(all.val))

# Tracer la tendance moyenne mobile
ts.plot(temp.fit.mav, lwd = 2, ylim = ylim, ylab = "temperature", col = 'blue')

# tendance régression polynomiale
lines(temp.fit.lm, lwd = 2, col = "green")

# tendance LOESS
lines(temp.loc.fit, lwd = 2, col = 'red')

# tendance spline
lines(temp.fit.gam, lwd = 2, col = 'yellow')

# Ajouter une légende (optionnel)
# legend(x = 1900, y = 64, legend = c('MAV',"LM",'LOC','SPLINE'),
#        lty = 1, col = c("blue",'green','red','yellow'))


# --------------------------------------------------
# DETECTION DE LA SAISONNALITE
# --------------------------------------------------

# Charger le package TSA
library(TSA)

# Identifier la saison (mois) pour chaque observation
month = season(temp)


# --------------------------------------------------
# Estimation de la saisonnalité avec modèle des moyennes mensuelles
# --------------------------------------------------

# Régression avec variables indicatrices (dummies)
model1 = lm(temp ~ month)

# Résumé du modèle
summary(model1)

# Modèle sans intercept (donne directement la moyenne de chaque mois)
model2 = lm(temp ~ month - 1)

# Résumé
summary(model2)


# --------------------------------------------------
# Estimation de la saisonnalité par modèle harmonique
# --------------------------------------------------

# Premier harmonique (sin/cos)
har1 = harmonic(temp, 1)

# Régression avec premier harmonique
model3 = lm(temp ~ har1)

summary(model3)

# Deuxième harmonique
har2 = harmonic(temp, 2)

# Régression avec deux harmoniques
model4 = lm(temp ~ har2)

summary(model4)


# --------------------------------------------------
# Comparer les deux estimations de saisonnalité
# --------------------------------------------------

# coefficients du modèle des moyennes mensuelles
st1 = coef(model2)

# valeurs ajustées du modèle harmonique pour un cycle de 12 mois
st2 = fitted(model4)[1:12]

# tracer saisonnalité mensuelle
plot(1:12, st1, lwd = 2, type = "l", xlab = 'month', ylab = 'Seasonality')

# ajouter saisonnalité harmonique
lines(1:12, st2, lwd = 2, col = 'blue')


# --------------------------------------------------
# Estimation simultanée trend + saisonnalité
# --------------------------------------------------

# Modèle avec tendance quadratique + saison
lm.fit2 = lm(temp ~ x1 + x2 + month)

summary(lm.fit2)

# calculer les résidus (température - trend - saison)
dif.fit.lm = ts(temp - fitted(lm.fit2), start = 1879, frequency = 12)

# tracer le processus résiduel
ts.plot(dif.fit.lm, ylab = 'Residual Process')


# --------------------------------------------------
# Modèle non paramétrique pour la tendance + saison harmonique
# --------------------------------------------------

gam.fit2 = gam(temp ~ s(time.pts) + har2)

# résidus du modèle
dif.gam.fit2 = ts(temp - fitted(gam.fit2), start = 1879, frequency = 12)

# ajouter les résidus sur le graphique
lines(dif.gam.fit2, col = "blue")


# --------------------------------------------------
# Analyse de l’autocorrélation (ACF)
# --------------------------------------------------

# 3 graphiques l’un sous l’autre
par(mfrow = c(3,1))

# ACF de la série originale
acf(temp, lag.max = 4*12, main = '')

# ACF des résidus du modèle linéaire
acf(dif.fit.lm, lag.max = 4*12)

# ACF des résidus du modèle GAM
acf(dif.gam.fit2, lag.max = 4*12)