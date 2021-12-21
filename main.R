library(tidyverse)

d <- read.csv("combined.csv")
head(d)

#Comparing occupancy of meals
ggplot(d, aes(x=factor(name, levels=c("Breakfast", "Lunch", "Dinner")), y=average_occupancy)) +
  geom_boxplot() +
  xlab("Meal")

d_formatted <- d %>%
  select(average_occupancy, is_family_dinner, is_weekend) %>%
  mutate(
    is_family_dinner = ifelse(is_family_dinner==1,"True","False"),
    is_weekend = ifelse(is_weekend==1,"True","False")
  )

#Comparing occupancy of weekend dinners
ggplot(d_formatted, aes(x=factor(is_weekend, levels=c("False","True")), y=average_occupancy)) +
  geom_boxplot() +
  xlab("Is Weekend Dinner")

#Comparing occupancy of family dinner
ggplot(d_formatted, aes(x=factor(is_family_dinner, levels=c("False","True")), y=average_occupancy)) +
  geom_boxplot() +
  xlab("Is Family Dinner")

#Analyzing impact of various factors on the occupancy
cor(d$average_occupancy, d[c('date_int','is_weekend','is_family_dinner','PRCP','TMAX','TMIN')], use="complete.obs")

m1 = lm(average_occupancy ~ date_int + is_weekend + is_family_dinner + PRCP + TMAX + TMIN, data=d)
summary(m1)

m2 = lm(average_occupancy ~ date_int + TMIN, data=d)
summary(m2)