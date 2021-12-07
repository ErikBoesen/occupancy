require(plyr)
require(dplyr)


#data <- read.csv('occupancy_raw.csv')
data <- read.csv('occupancy_raw_trimmed.csv')

convert_timestamp <- function(datetime) {
    round_any(
        as.integer(as.POSIXct(datetime, format="%Y-%m-%d %H:%M:%OS", tz="")),
        10, f=floor
    )
}
convert_date <- function(datetime) {
    #as.integer(as.POSIXct(paste("1970-01-01" + strsplit(datetime, " ")[[1]][1]), tz="")) ,
    strsplit(datetime, " ")[[1]][1]
}
convert_second <- function(datetime) {
    #as.integer(as.POSIXct(paste("1970-01-01" + strsplit(datetime, " ")[[1]][1]), tz="")) ,
    strsplit(
         strsplit(datetime, " ")[[1]][2]
         "."
    )[[1]][1]
}
data <- data %>% filter(
data <- data %>% mutate(timestamp = convert_timestamp(datetime))
data <- data %>% mutate(second = convert_second(datetime))
data = data[c('crowdedness', 'dhall', 'timestamp', 'second')]
data = data %>% distinct()
head(data)

duplicated()

write.csv(data, 'occupancy.csv', row.names = FALSE, quote = FALSE)
