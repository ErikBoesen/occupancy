require(dplyr)
require(ggplot2)
require("ggpubr")

data <- read.csv('occupancy.csv')
#data <- read.csv('occupancy_trimmed.csv')

hall_ids <- c('BK', 'BR', 'GH', 'DC', 'MC', 'JE', 'PC', 'SM', 'TD', 'SY', 'ES', 'TC', 'BF', 'PM')

create_scatterplot <- function(hall_id) {
    ggplot(subset(data, dhall == hall_id), aes(x=timestamp, y=crowdedness, color=dhall)) +
        geom_point(alpha=0.01)
}

png(file = "timeline.png")
ggplot(data, aes(x=timestamp, y=crowdedness, color=dhall)) +
    geom_point(alpha=0.01)

png(file = "daily.png", width=2000, height=6000)
hall_plots <- lapply(hall_ids, create_scatterplot)
ggarrange(plotlist=hall_plots, labels=hall_ids, ncol=1, nrow=14)
