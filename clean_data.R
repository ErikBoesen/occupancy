require(plyr)
require(dplyr)


data <- read.csv('occupancy_raw_deduplicated.csv')

convert_timestamp <- function(datetime) {
    as.POSIXct(datetime, format="%Y-%m-%d %H:%M:%OS", tz="")
}
convert_date <- function(datetime) {
    #as.integer(as.POSIXct(paste("1970-01-01" + strsplit(datetime, " ")[[1]][1]), tz="")) ,
    strsplit(datetime, " ")[[1]][1]
}
convert_second <- function(datetime) {
    #as.integer(as.POSIXct(paste("1970-01-01" + strsplit(datetime, " ")[[1]][1]), tz="")) ,
    strsplit(
         strsplit(datetime, " ")[[1]][2],
         "."
    )[[1]][1]
}
data <- data %>% mutate(timestamp = convert_timestamp(datetime))
data <- data %>% mutate(second = convert_second(datetime))
data = data[c('crowdedness', 'dhall', 'timestamp', 'second')]
head(data)

write.csv(data, 'occupancy.csv', row.names = FALSE, quote = FALSE)
