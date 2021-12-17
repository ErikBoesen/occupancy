library(tidyverse)

meals <- read.csv("meals.csv")
colnames(meals)[1] <- "DATE";
weather <- read.csv("NewHavenWeather.csv")
weather_clean <- weather[,c("DATE", "PRCP", "TMAX", "TMIN")]

head(meals)
head(weather_clean)

combined <- merge(meals, weather_clean, by=c("DATE"),all.x=T)
print(nrow(weather_clean))
print(nrow(meals))
print(nrow(combined))

write.csv(combined, "combined.csv")