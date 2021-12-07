require(plyr)
require(dplyr)


data <- read.csv('occupancy_raw.csv')
#data <- read.csv('occupancy_raw_trimmed.csv')

data <- subset(data, dhall == 'GH')

write.csv(data, 'occupancy_GH.csv', row.names = FALSE, quote = FALSE)
