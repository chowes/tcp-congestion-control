library(ggplot2)

dctcp_queue_data <- read.csv(file = "/home/colin/Documents/School/tcp-congestion-control/tests/results/dctcp_queue.csv", na.strings = c("NA"), header = FALSE)
reno_queue_data <- read.csv(file = "/home/colin/Documents/School/tcp-congestion-control/tests/results/reno_queue.csv", na.strings = c("NA"), header = FALSE)

dctcp_start <- dctcp_queue_data[1, 1]
reno_start <- reno_queue_data[1, 1]

dctcp_queue_data[,1] = dctcp_queue_data[,1] - dctcp_start
reno_queue_data[,1] = reno_queue_data[,1] - reno_start

queue_data = data.frame("cong_ctl"=c(rep("reno", length(reno_queue_data[,1])), rep("dctcp", length(dctcp_queue_data[,1]))), "queue_len"=c(reno_queue_data[,2], dctcp_queue_data[,2]), "time"=c(reno_queue_data[,1], dctcp_queue_data[,1]))

queue_graph <- ggplot(queue_data, aes(x=time, y=queue_len, colour = cong_ctl, shape = cong_ctl)) +
  geom_line() + 
  labs(x = "Time (Seconds)", y = "Queue Length") +
  coord_cartesian(ylim = c(0, 200)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_shape_manual(values = c(21, 22)) +
  scale_color_manual(limits = c("reno", "dctcp"), breaks = c("reno", "dctcp"), values = c("black", "dark gray"), labels = c("TCP Reno", "DCTCP")) +
  theme_bw() + 
  theme(axis.title.y = element_text(size=20, margin = margin(0, 15, 0, 0), face="bold"),
        axis.title.x = element_text(size=20, margin = margin(15, 0, 0, 0), face="bold"),
        axis.text.y = element_text(size=16, color = "black"), 
        axis.text.x = element_text(size=20, color = "black"), 
        axis.ticks = element_line(size=1.6, color = "black"),
        legend.text = element_text(size = 20, colour = "black", face = "bold"),
        legend.title = element_blank(),
        legend.key = element_blank(),
        legend.key.size = unit(1.5, "cm"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        axis.line.x = element_line(colour = 'black', size = 1.6),
        axis.line.y = element_line(colour = 'black', size = 1.6),
        plot.margin=unit(c(.5,.5,.5,.5), "cm"))
queue_graph
