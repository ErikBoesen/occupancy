library(tidyverse)

d <- read.csv("combined.csv")
head(d)

#m1 = lm(average_occupancy ~ date_int + PRCP + TMAX + TMIN, data=d)
m1 = lm(average_occupancy ~ name, data=d)
summary(m1)

#Comparing occupancy of meals
ggplot(d, aes(x=factor(name, levels=c("Breakfast", "Lunch", "Dinner")), y=average_occupancy)) +
  geom_boxplot() +
  xlab("Meal")

d_formatted <- d %>%
  select(average_occupancy, is_family_dinner) %>%
  mutate(
    is_family_dinner = ifelse(is_family_dinner==1,"True","False")
  )
#Comparing occupancy of meals
ggplot(d_formatted, aes(x=factor(is_family_dinner, levels=c("False","True")), y=average_occupancy)) +
  geom_boxplot() +
  xlab("Is Family Dinner")