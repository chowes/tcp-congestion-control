#!/usr/bin/Rscript

setwd("~/Documents/School/tcp-congestion-control/")

library(ggplot2)
source("tests/plots.R")

queue_data <- read.csv(file = "tests/results/queue.csv", header = TRUE)
converg_data <- read.csv(file = "tests/results/converg.csv", header = TRUE)
throughput_data <- read.csv(file = "tests/results/dctcp_k_thru.csv", header=TRUE)

# generate graph of queue length over time
queue_data_2_flow <- subset(queue_data, cong_ctl=='reno_2' | cong_ctl=='dctcp_2')
queue_time_graph(queue_data_2_flow, "paper/figures/queue_2_flows.pdf", save=FALSE)

# generate CDF graph of queue length for tests with 2 and 20 flows
queue_cdf_graph(queue_data, "paper/figures/queue_cdf.pdf", save=FALSE)

# generate convergance graph
converg_graph(subset(converg_data, cong_ctl == "dctcp"), "paper/figures/dctcp_converg.pdf", save=FALSE)
converg_graph(subset(converg_data, cong_ctl == "reno"), "paper/figures/reno_converg.pdf", save=FALSE)

# generate throughput graph based on K, no effect after 20 so we can cut it off at k = 60
k_throughput_graph(throughput_data, "paper/figures/k_throughput.pdf", save=FALSE)
