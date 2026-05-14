# Import the csv
CO2_Practical <- read.csv("/media/engine/KINGSTON/CSIE_Sources/Anul_II/Sem_2/Practică de Specialitate/raspunsuri_chestionar_edit.csv", header = TRUE)

# View the csv
View(CO2_Practical)

# View the dataframe of csv, useful for identifying variables
str(CO2_Practical)
str(CO2_Practical$Intrebarea_3)

# Descriptive Statistics (Min, Quartile, Median, Mean, Max)
summary(CO2_Practical$Emisii_Totale_tone_CO2)
summary(CO2_Practical$Intrebarea_1)
summary(CO2_Practical$Intrebarea_3)


# Marked as comment, if psych is already installed. Doing so, takes more time!
# install.packages("psych", dependencies = TRUE)

# Activate the package
library(psych)

# ============================================================================

# Descriptive Statistics, using psych::describe()
psych::describe(CO2_Practical$Emisii_Totale_tone_CO2)
psych::describe(CO2_Practical$Intrebarea_1)

# Localized, 26 questions. Incompleted values are null (=0)
psych::describe(CO2_Practical[, 8:34])

# Models for variables axis
x_axis <- CO2_Practical$Emisii_Totale_tone_CO2
y_axis <- CO2_Practical$Intrebarea_3

# PLOTTING THE REGRESSION
plot(x_axis, y_axis,
     main = "Consumul lunar de gaz, cu excepția sezonului rece\nraportat la emisii totale de CO2",
     xlab = "Emisii totale de CO2", ylab = "mc",
     col = 'limegreen', pch = 1, lwd = 1,
     frame = TRUE)

# Models for abline + lines
model_CO2_Emission_Q3 <- lm(CO2_Practical$Intrebarea_3 ~ CO2_Practical$Emisii_Totale_tone_CO2)
x_CO2_Emission <- seq(0, 50, by = 0.05)
y_Q3 <- x_CO2_Emission^2 + rnorm(length(x_CO2_Emission), sd = 6.12)

lines(x_CO2_Emission, x_CO2_Emission^2, col = 2, lwd = 3)
abline(model_CO2_Emission_Q3, col = 'blue', lwd = 3)

# ==================================================================================

# install.packages("ggplot2", dependencies = TRUE)
library(ggplot2)

model_aes_Emission_Q3 <- aes(x = Emisii_Totale_tone_CO2, y = Intrebarea_3)


ggplot(data = CO2_Practical, model_aes_Emission_Q3) +
  geom_point(color = 'blue') +
  geom_smooth(method = "lm", color = 'red', se = FALSE) +
  labs(title = "Consumul lunar de gaz, cu excepția sezonului rece, raportat la emisii totale de CO2",
       x = "Emisii totale de CO2",
       y = "mc") +
  theme_minimal()

# ==================================================================================

summary(model_CO2_Emission_Q3)
anova(model_CO2_Emission_Q3)

# Intercept
CO2_Emission_Coef <- round(model_CO2_Emission_Q3$coefficients, digits = 4)
CO2_Emission_Coef
coefficients(model_CO2_Emission_Q3)

# Estimated values
CO2_Emission_Estimated <- round(model_CO2_Emission_Q3$fitted.values, digits = 4)
CO2_Emission_Estimated

# Residuals
CO2_Emission_Residuals <- round(model_CO2_Emission_Q3$residuals, digits = 4)
CO2_Emission_Residuals

hist(CO2_Emission_Estimated)
hist(CO2_Emission_Residuals)

# Confidence level
CO2_Emission_CONF_95 <- round(confint(model_CO2_Emission_Q3), digits = 4)
CO2_Emission_CONF_95

CO2_Emission_CONF_98 <- round(confint(model_CO2_Emission_Q3, level = 0.98), digits = 4)
CO2_Emission_CONF_98

# ==================================================================================

CSV_MODEL <- data.frame(ID = CO2_Practical$ID,
                        Utilizator = CO2_Practical$Utilizator,
                        Data_Trimiterii = CO2_Practical$Data_Trimiterii,
                        Emisii_Totale_tone_CO2 = CO2_Practical$Emisii_Totale_tone_CO2,
                        Emisii_de_CO2_Estimat = CO2_Emission_Estimated,
                        Emisii_de_CO2_Reziduu = CO2_Emission_Residuals)
CSV_MODEL

write.csv(CSV_MODEL,
          file = "/media/engine/KINGSTON/CSIE_Sources/Anul_II/Sem_2/Practică de Specialitate/CO2_Practical.csv",
          row.names = FALSE,
          col.names = TRUE)

# ==================================================================================

