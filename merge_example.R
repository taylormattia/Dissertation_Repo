#Clear memory and set working directory
rm(list = ls())
setwd("/home/centos")


#Load libraries
library(feather)
library(dplyr)
library(fst)
library(fastLink)
options(mc.cores=1)

#Defining files
#Voter file for last names beginning with A; ages 18-25
vf <- read_fst("all_states_A_18_25.fst")

#Scraped Classmates users with last names beginning with A; ages 18-25
scraped <- read_feather('file_scraped_A_18_25.feather')

#Blocking based on last name
blockdata_out <- blockData(scraped, vf, 
                           varnames = c("Voters_LastName"),
                           kmeans.block = c("Voters_LastName"),
                           #window.block = "age", window.size = 3,
                           nclusters = 20)


#Setting up vectors to hold results from blocking
blocks = length(blockdata_out)
names(blockdata_out) <- NULL
blockdata_out_list_a <- vector('list', length = blocks)
blockdata_out_list_b <- vector('list', length = blocks)
a_18_25 <- vector('list', length = blocks)

#Grabbing blocking indices
for (i in 1:blocks) {
  blockdata_out_list_a[[i]] <- blockdata_out[[i]]$dfA.inds
  blockdata_out_list_b[[i]] <- blockdata_out[[i]]$dfB.inds
}


#FastLink for each block (to merge data sets)
for (i in 1:blocks) {
  print(i)
  a_18_25[[i]] <- fastLink(scraped[blockdata_out_list_a[[i]], ], 
                           vf[blockdata_out_list_b[[i]], ], 
                           varnames = c('Voters_FirstName', 'Voters_LastName', 'age', 'state'),
                           return.df = TRUE, n.cores = 1, threshold.match = 0.99,
                           stringdist.match = 'Voters_FirstName', cut.p = 0.85)
  
}

#Combining in a list
a_18_25_list <- vector('list', length = blocks)
for (i in 1:blocks) {
  a_18_25_list[[i]] <- list(a_18_25[[i]][[1]], a_18_25[[i]][[2]])
  a_18_25_list[[i]] <- do.call("cbind",  a_18_25_list[[i]])
}

#Grabbing number of iterations to converge and posterior
iterations <- vector('list', length = blocks)
posterior <- vector('list', length = blocks)

for (i in 1:blocks) {
  iterations[[i]] <- rep(a_18_25[[i]]$EM$iter.converge, times = nrow(a_18_25_list[[i]]))
  posterior[[i]] <- rep(a_18_25[[i]]$posterior)
}


for (i in 1:blocks) {
  iterations[[i]] <- cbind(iterations[[i]], posterior[[i]])
  a_18_25_list[[i]]  <- cbind(a_18_25_list[[i]], iterations[[i]])
}

#Row binding results and renaming columns
a_18_25_list <- data.table::rbindlist(a_18_25_list)
colnames(a_18_25_list)[668] <- "iterations"
colnames(a_18_25_list)[669] <- "posterior"

colnames(a_18_25_list)[c(2, 3, 12, 20)] <- c("classmates_first_name", "classmates_last_name",
                                             "classmates_state", "classmates_age")

#Creating an age difference variable
a_18_25_list$age_diff <- a_18_25_list$classmates_age - a_18_25_list$age

#Write as an .fst file
fst::write.fst(a_18_25_list, "a_18_25_matched.fst")
