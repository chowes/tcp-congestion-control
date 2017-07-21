#!/usr/bin/Rscript
setwd("~/Documents/School/tcp-congestion-control/")

library(ggplot2)
source("tests/plots.R")

queue_data <- read.csv(file = "tests/results/queue.csv", header = TRUE)

# generate graph of queue length over time - replicates figure 1 from Alizadeh et al. 2010 
queue_data_2_flow <- subset(queue_data, cong_ctl=='reno_2' | cong_ctl=='dctcp_2')
queue_time_graph(queue_data_2_flow, "paper/figures/queue_2_flows.pdf")

# generate CDF of queue length for tests with 2 and 20 flows
