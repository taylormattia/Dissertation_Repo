### Distribution plot of dismissal dates

#Clearing memory
rm(list = ls())

#Loading libraries
library(haven)
library(ggplot2)
library(dplyr)

#Setting working directory
setwd("/volumes/easystore/voter_files/demographic_files/matched_files/merged/")

#Reading in court order data and subsetting to six states of interest
dismissal <- read_dta("district_court_order_data.dta")
dismissal <- subset(dismissal, 
                    state == "LA"|state=="FL"|state=="GA"|state=="TN"|
                      state=="NC"|state=="SC")

#Keeping only if inpaper1==1
dismissal <- subset(dismissal, inpaper1 == 1)

#Reading in pro-publica data
setwd("/volumes/easystore/voter_files/demographic_files/matched_files/merged")
pro_pub <- read_excel("pro_publica_dates.xlsx")

#Convering leaid to numeric to merge
pro_pub$leaid <- as.numeric(pro_pub$leaid)

#Joining by leaid
dismissal <- left_join(dismissal, pro_pub)

#Assign year of dismissal based on ProPublica data if there is no conflict 
#with the original
dismissal <- within(dismissal, {
  yrdiss[status_2013_2014 == 1989 & is.na(conflicts_with_original)] <- 1989
  yrdiss[status_2013_2014 == 1992 & is.na(conflicts_with_original)] <- 1992
  yrdiss[status_2013_2014 == 1995 & is.na(conflicts_with_original)] <- 1995
  yrdiss[status_2013_2014 == 1999 & is.na(conflicts_with_original)] <- 1999
  yrdiss[status_2013_2014 == 2005 & is.na(conflicts_with_original)] <- 2005
  yrdiss[status_2013_2014 == 2006 & is.na(conflicts_with_original)] <- 2006
  yrdiss[status_2013_2014 == 2007 & is.na(conflicts_with_original)] <- 2007
  yrdiss[status_2013_2014 == 2008 & is.na(conflicts_with_original)] <- 2008
  yrdiss[status_2013_2014 == 2009 & is.na(conflicts_with_original)] <- 2009
  yrdiss[status_2013_2014 == 2010 & is.na(conflicts_with_original)] <- 2010
  yrdiss[status_2013_2014 == 2011 & is.na(conflicts_with_original)] <- 2011
  yrdiss[status_2013_2014 == 2012 & is.na(conflicts_with_original)] <- 2012
  yrdiss[status_2013_2014 == 2013 & is.na(conflicts_with_original)] <- 2013
})



#Total number of districts = 197
total_num <- 197

#Getting total # by year dismissed
dismissal_by_year <- dismissal %>% group_by(yrdiss) %>% summarize(count = n())

#Removing instances where yrdiss is missing
dismissal_by_year <- subset(dismissal_by_year, !is.na(yrdiss))

#Creating data frame that is # of released districts/# of total districts
year_plot_df <- data.frame(year = seq.int(1990, 2013, 1))

#Creating total number of districts
year_plot_df$total_district_num <- 197

#Creating dismissed/non-dismissed variables
dismiss_vector <- c(0, 0, dismissal_by_year$count)

#Getting running total
running_total <- c(0, 0, 1, 1, 3, 4, 6, 9, 11, 13, 15, 21, 24, 27, 33, 38, 48, 58, 63, 73, 76, 78, 80, 86)

#Defining dismissed as running total
year_plot_df$dismissed <-running_total 

#Non-dismisssed = 1 - dismissed
year_plot_df$non_dismissed <- with(year_plot_df,
                                   total_district_num - dismissed)

#Creating panel 
year_plot_df2 <- data.frame(year = rep(seq.int(1990, 2013, 1), times = 2))

#Creating groups
year_plot_df2$group <- NA
year_plot_df2$group[1:24] <- rep(c("Dismissed"), times = 24)
year_plot_df2$group[25:48] <- rep(c("Not Dissmissed"), times = 24)

#Getting number of dismissed districts over time
year_plot_df2$num <- NA
year_plot_df2$num[1:24] <- year_plot_df$dismissed
year_plot_df2$num[25:48] <- year_plot_df$non_dismissed

#Creating histrogram over time 
g1 <- ggplot(year_plot_df2, aes(x=year, y = num, fill = group)) + 
  geom_histogram(stat = "identity") +
  xlab("Year") +
  ylab("Number of Districts") +
  guides(fill=guide_legend(title="Status")) +
  theme(axis.text=element_text(size=12, face = "bold"),
        axis.title=element_text(size=14,face="bold"),
        legend.title = element_text(colour="black", size=10, 
                                    face="bold"),
        legend.text = element_text(colour="black", size=10, 
                                   face="bold"))

ggsave("yr_diss.jpeg", g1, width=8, height=2.5)

