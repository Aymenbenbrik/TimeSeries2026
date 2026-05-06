# LIVRABLE — Module Time Series Analysis

**Responsable :** Aymen Ben Brik · `aymen.benbrik@esprit.tn`
**Établissement :** Esprit School of Business
**Année universitaire :** 2025–2026

> Checklist de conformité du module *Time Series Analysis* par rapport
> à la fiche pédagogique (`Fiche Module/Fiche_TimeSeries.docx`).

> Le contenu pédagogique (polycopié, slides, TPs, projet) est en
> **anglais**. La fiche module officielle ECUE est rédigée en
> **français**, conformément aux exigences de la DGRU.

---

## 1. Identification du module

| Champ | Valeur | Statut |
|---|---|---|
| Intitulé de l'UE | Analyse de séries temporelles | ✅ |
| Code UE / Code ECUE | **à confirmer** (placeholders `UEF6x0` / `ECUE6xx`) | ⏳ |
| Filière | Mathématiques / GAMMA (à confirmer) | ⏳ |
| Département | Statistique et économétrie appliquées | ✅ |
| Option | Sciences des données | ✅ |
| Semestre | S6 (à confirmer) | ⏳ |
| Responsable | Aymen Ben Brik | ✅ |
| Email pro | aymen.benbrik@esprit.tn | ✅ |

## 2. Volume horaire et coefficient

| Composante | Valeur fiche | Réel produit | Statut |
|---|---|---|---|
| Cours (C) | 30 h | Polycopié 37 pages, 6 chapitres | ✅ |
| TD | 18 h | Inclus dans le polycopié | ✅ |
| TP | 18 h | 6 TPs (Lab 1 → Lab 6) | ✅ |
| Projet | 9 h | 6 mini-projets de chapitre + 1 projet final intégrateur | ✅ |
| **Total présentiel** | 75 h | — | ✅ |
| Coefficient | 2.5 | — | ⏳ à confirmer |
| ECTS | 5 | — | ⏳ à confirmer |

## 3. Acquis d'apprentissage (AA)

| AA | Libellé | Couvert par |
|---|---|---|
| AA1 | Mobiliser les notions statistiques fondamentales (moments, estimation, IC, tests) et conduire la décomposition classique d'une série temporelle | Ch.1, Ch.2 (polycopié + slides + Lab 1, Lab 2, Project 1, Project 2) |
| AA2 | Maîtriser les diagnostics de stationnarité (ACF, PACF, Ljung--Box) et de non-stationnarité (opérateurs $B$ et $\Delta$, ADF / KPSS / Phillips--Perron, ordre $I(d)$) | Ch.3, Ch.4 (polycopié + slides + Lab 3, Lab 4, Project 3, Project 4) |
| AA3 | Construire, estimer (MLE) et valider des modèles ARMA, ARIMA et SARIMA selon Box--Jenkins ; produire des prévisions multi-horizons avec IC | Ch.5 (polycopié + slides + Lab 5, Project 5) |
| AA4 | Modéliser la volatilité conditionnelle (ARCH, GARCH, test de Engle), estimer une Value-at-Risk et conduire un projet intégrateur Python avec back-test de Kupiec | Ch.6 + projet final intégrateur |

### Acquis d'apprentissage du programme (AAP) ciblés par le module

| AAP (proposé) | Couvert par |
|---|---|
| Mobiliser les statistiques de base et la décomposition d'une série | AA1 |
| Diagnostiquer la stationnarité et la non-stationnarité d'une série | AA2 |
| Construire et valider des modèles ARMA, ARIMA, SARIMA | AA3 |
| Modéliser la volatilité conditionnelle et calculer la VaR | AA4 |
| Maîtriser ACF/PACF/Ljung--Box et la combinaison ADF/KPSS pour la classification TS/DS | AA2 |
| Construire et valider une SARIMA(p,d,q)(P,D,Q)$_s$ ; identifier l'ordre par AIC/BIC et Ljung--Box | AA3 |
| Modéliser la volatilité conditionnelle (ARCH/GARCH), tester les effets ARCH (Engle) et calculer une VaR back-testée | AA4 |
| Appliquer l'analyse de séries temporelles à une étude complète de risque financier (back-test inclus) | AA4 + projet final |

> Cette table est une proposition. Le responsable confirme la grille
> AAP officielle du programme via la dernière table de la fiche
> (`Fiche Module/Fiche_TimeSeries.docx`, section "Acquis de Formation
> visés").

## 4. Supports produits

### Polycopié (`polycopie/polycopie.pdf`)

- [x] Page de garde personnalisée (auteur Aymen Ben Brik, email pro)
- [x] Avant-propos signé en anglais
- [x] Table des matières globale
- [x] Ch.1 Basic statistics (moments, estimation, sampling distributions, inference)
- [x] Ch.2 Decomposition (trend, seasonality, residual)
- [x] Ch.3 Stationarity (strict/weak stationarity, ACF/PACF, Wold)
- [x] Ch.4 Non-stationarity (random walk, unit roots, ADF/KPSS, ARIMA, SARIMA)
- [x] Ch.5 ARMA models (AR, MA, ARMA, MLE, AIC/BIC, forecasting)
- [x] Ch.6 ARCH/GARCH (volatility clustering, Engle LM, MLE, VaR)
- [x] Bibliographie organisée par thème (Box-Jenkins → Engle 1982 → Bollerslev 1986 → Hyndman 2021 → docs statsmodels/arch)
- [x] **37 pages** au total, références croisées résolues, aucun overfull

### Slides Beamer (Metropolis 16:9, par chapitre)

- [x] `chapitre1-statistics/slides.pdf` — **24 frames**
- [x] `chapitre2-decomposition/slides.pdf` — **22 frames**
- [x] `chapitre3-stationarity/slides.pdf` — **25 frames**
- [x] `chapitre4-nonstationarity/slides.pdf` — **24 frames**
- [x] `chapitre5-arma/slides.pdf` — **~25 frames**
- [x] `chapitre6-arch-garch/slides.pdf` — **~25 frames**
- [x] Authorship Aymen Ben Brik / aymen.benbrik@esprit.tn sur chaque slide titre
- [x] Charte couleur cohérente (espritBlue, espritAccent)

### TPs (énoncé + correction + canevas + solution Python)

- [x] **Lab 1** Basic statistics : énoncé 2p, correction 2p, `seed.py` + `correction.py` testés (Atlanta temperatures, T = 1656)
- [x] **Lab 2** Decomposition : énoncé + correction, fits Fourier + averaging vérifiés
- [x] **Lab 3** ACF/PACF + Ljung-Box : statsmodels + Bartlett bands
- [x] **Lab 4** Unit-root tests + ARIMA : ADF/KPSS + SARIMA(0,1,1)(0,1,1)$_{12}$ sur log SouvenirSales, AIC = -43.08, LB(24) p = 0.887
- [x] **Lab 5** ARMA estimation + forecasting : AR(2)/MA(1)/ARMA(1,1) sur séries simulées + Atlanta residual
- [x] **Lab 6** ARCH/GARCH + VaR : Engle LM, GARCH(1,1) sur retours synthétiques, VaR(1%, 5%)
- [x] Reproductibilité : `numpy.random.seed(42)` + UTF-8 forcé partout
- [x] Auteur Aymen Ben Brik dans chaque docstring d'en-tête
- [x] Toutes les solutions de référence ont été exécutées **end-to-end** ; les valeurs numériques de `correction.tex` correspondent aux sorties effectives

### Mini-projets par chapitre

- [x] **Project 1** : étude statistique complète sur Atlanta (Ch.1)
- [x] **Project 2** : décomposition log-additive de SouvenirSales 1995-2001 (Ch.2)
- [x] **Project 3** : diagnostic de stationnarité du résidu de Project 2 (Ch.3)
- [x] **Project 4** : étude complète ADF/KPSS + SARIMA sur SouvenirSales (Ch.4)
- [x] **Project 5** : full Box-Jenkins ARMA avec back-transform sur log-prix (Ch.5)
- [x] **Project 6** : mean-variance modelling (ARMA + GARCH + VaR + Kupiec) (Ch.6)

### Projet final intégrateur (`projet-final/`)

- [x] `sujet.pdf` (4 pages) avec grille de notation /100
- [x] `seed/projet.py` (canevas étudiant, 7 parts A–G)
- [x] `correction/projet.py` (solution de référence, **vérifiée end-to-end**) :
  - GARCH(1,1) recouvre $(\alpha_1, \beta_1) = (0.073, 0.884)$ proche du DGP
  - Variance non conditionnelle implicite $0.0204$ ≈ écart-type empirique
  - Résidus standardisés passent Engle LM à tous les lags
  - **Back-test de Kupiec : 19 dépassements / expected 12.5, LR = 3.09 < 3.84 → VaR bien calibrée**
- [x] Mobilise les 6 chapitres : stats descriptives (Ch.1) → décomposition (Ch.2) → ACF/PACF (Ch.3) → ADF/KPSS (Ch.4) → ARMA (Ch.5) → GARCH + VaR (Ch.6)
- [x] Dataset synthétique reproductible (`generate_dataset.py`, GARCH(1,1) caché avec seed 42)

### Activité réflexive (`activite-reflexive/`)

- [x] `activite-reflexive.tex` : 8 questions guidées d'auto-évaluation
      (auto-positionnement par chapitre, schéma Box-Jenkins de mémoire,
      calcul mental sur AR(1)/MA(1)/GARCH/ADF-KPSS, lien entre les 6
      chapitres, plan d'action personnel)
- [x] Non notée, à proposer en fin de module

### Fiche pédagogique (`Fiche Module/`)

- [x] `Fiche_TimeSeries.docx` au format officiel Esprit/DGRU (template ECUE)
- [x] Génération automatisée et reproductible via `generate_fiche.py`
      (single-pass XML walk, idempotent, zero-leak vérifié)
- [ ] **À confirmer manuellement par le responsable** : code ECUE, code UE,
      semestre, volumes horaires précis, AAP du programme, durée examen final

## 5. Modalités d'évaluation

| Composante | Pondération | Statut |
|---|---|---|
| Activités formatives (quiz, activité réflexive) | 0% (feedback uniquement) | ✅ prévu (`activite-reflexive/`) |
| Contrôle continu | 15% épreuve écrite courte | ⏳ à organiser |
| Mini-projet | 15% (un mini-projet par chapitre, retenu : projet 6 par défaut) | ⏳ à organiser |
| Examen final | 70% | ⏳ à organiser (durée 2h par défaut) |
| **Total** | **100%**, validation ≥ 10/20 | — |

## 6. Reproductibilité technique

- [x] Repo Git initialisé (`git log --oneline` : un commit par étape 1 → 11)
- [x] `.gitignore` LaTeX complet
- [x] Compilation testée sous **MiKTeX 21** + **Python 3.14**
- [x] Dépendances Python : `numpy`, `pandas`, `scipy`, `matplotlib`, `statsmodels`, `arch`
      (toutes installées et testées)
- [x] Préambules réutilisables : `slides-preamble.tex`, `poly-preamble.tex`,
      `td-tp-preamble.tex`, `macros.tex`
- [x] Wrappers standalone par chapitre + assemblage dans le polycopié final
- [x] Toutes les solutions de référence Python ont été **exécutées
      localement** ; les valeurs numériques affichées dans les
      `correction.tex` correspondent aux sorties effectives
      (cf.\ `numpy.random.seed(42)`)

## 7. À finaliser avec la direction Esprit

- [ ] Fixer le **code ECUE et code UE** définitif (actuellement `UEF6x0` / `ECUE6xx` placeholders)
- [ ] Confirmer **semestre / filière / option** exacts dans le programme
- [ ] Confirmer **volumes horaires** exacts (C / TD / TP / Projet) -- ils sont actuellement 30 / 18 / 18 / 9 h pour un total de 75 h, à valider
- [ ] Confirmer **coefficient et ECTS**
- [ ] Cocher les **AAP** (acquis d'apprentissage du programme) effectivement
      ciblés par le module dans la grille (dernière table de la fiche)
- [ ] Préciser la **durée de l'examen final** (par défaut : 2h)
- [ ] Indiquer si le module remplace ou complète un module existant
      (ex.\ "Statistique inférentielle 2" ou "Économétrie")

---

**Statut global : ✅ tous les supports techniques sont produits et
testés ; il reste les choix administratifs à arbitrer avec la direction
Esprit.**

\hfill *Aymen Ben Brik, aymen.benbrik@esprit.tn*
