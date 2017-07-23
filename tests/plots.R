#!/usr/bin/Rscript

require(ggplot2)

queue_time_graph <- function(queue_data, filename, save=FALSE) {

  plot <- ggplot(queue_data, aes(x=time, y=q_len, colour = cong_ctl, linetype = cong_ctl)) +
    geom_line(size=1.2) + 
    labs(x = "Time (Seconds)", y = "Queue Length (Packets)") +
    coord_cartesian(ylim = c(0, 400), xlim=c(0, 60)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_linetype_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c(1, 1), labels = c("TCP Reno", "DCTCP")) +
    scale_color_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c("blue", "red"), labels = c("TCP Reno", "DCTCP")) +
    theme_bw() + 
    theme(axis.title.y = element_text(size=20, margin = margin(0, 15, 0, 0), face="bold"),
          axis.title.x = element_text(size=20, margin = margin(15, 0, 0, 0), face="bold"),
          axis.text.y = element_text(size=16, color = "black"), 
          axis.text.x = element_text(size=20, color = "black"), 
          axis.ticks = element_line(size=1.6, color = "black"),
          legend.text = element_text(size = 20, colour = "black", face = "bold"),
          legend.title = element_blank(),
          legend.key = element_blank(),
          legend.key.size = unit(1, "cm"),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          panel.background = element_blank(),
          axis.line.x = element_line(colour = 'black', size = 1.6),
          axis.line.y = element_line(colour = 'black', size = 1.6),
          plot.margin=unit(c(.5,.5,.5,.5), "cm"))
  
  if (save) {
    ggsave(plot=plot, filename=filename, width=10, height=5)
  } else {
    print(plot)
  }
}


queue_cdf_graph <- function(queue_data, filename, save=FALSE) {
  
  plot <- ggplot(queue_data, aes(q_len, color=cong_ctl)) +
    stat_ecdf(size=2) +
    labs(x = "Queue Length (Packets)", y = "Cumulative Fraction") +
    coord_cartesian(ylim = c(0, 1), xlim=c(0, 400)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_linetype_manual(limits = c("dctcp_2", "dctcp_20", "reno_2", "reno_20"), breaks = c("dctcp_2", "dctcp_20", "reno_2", "reno_20"), values = c(1,2,4,5), labels = c("DCTCP - 2 Flows", "DCTCP - 20 Flows", "TCP - 2 Flows", "TCP - 20 Flows")) +
    scale_color_manual(limits = c("dctcp_2", "dctcp_20", "reno_2", "reno_20"), breaks = c("dctcp_2", "dctcp_20", "reno_2", "reno_20"), values = c("red", "green", "blue", "black"), labels = c("DCTCP - 2 Flows", "DCTCP - 20 Flows", "TCP - 2 Flows", "TCP - 20 Flows")) +
    theme_bw() + 
    theme(axis.title.y = element_text(size=20, margin = margin(0, 15, 0, 0), face="bold"),
          axis.title.x = element_text(size=20, margin = margin(15, 0, 0, 0), face="bold"),
          axis.text.y = element_text(size=16, color = "black"), 
          axis.text.x = element_text(size=20, color = "black"), 
          axis.ticks = element_line(size=1.6, color = "black"),
          legend.text = element_text(size = 20, colour = "black", face = "bold"),
          legend.title = element_blank(),
          legend.key = element_blank(),
          legend.key.size = unit(1, "cm"),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          panel.background = element_blank(),
          axis.line.x = element_line(colour = 'black', size = 1.6),
          axis.line.y = element_line(colour = 'black', size = 1.6),
          plot.margin=unit(c(.5,.5,.5,.5), "cm"))
  
  if (save) {
    ggsave(plot=plot, filename=filename, width=10, height=5)
  } else {
    print(plot)
  }
}


converg_graph <- function(converg_data, filename, save=FALSE) {
  
  plot <- ggplot(converg_data, aes(x=time, y=thru, color=sender)) +
    geom_line(size=1) +
    labs(x = "Time (Seconds)", y = "Throughput (Mbits/Second)") +
    coord_cartesian(ylim = c(0, 100), xlim=c(0, 540)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_x_continuous(breaks = seq(0, 540, by = 60)) +
    scale_color_manual(limits = c("h2", "h3", "h4", "h5", "h6"), breaks = c("h2", "h3", "h4", "h5", "h6"), values = c("purple", "red", "green", "blue", "black"), labels = c("Flow 1", "Flow 2", "Flow 3", "Flow 4", "Flow 5")) +
    theme_bw() + 
    theme(axis.title.y = element_text(size=20, margin = margin(0, 15, 0, 0), face="bold"),
          axis.title.x = element_text(size=20, margin = margin(15, 0, 0, 0), face="bold"),
          axis.text.y = element_text(size=16, color = "black"), 
          axis.text.x = element_text(size=20, color = "black"), 
          axis.ticks = element_line(size=1.6, color = "black"),
          legend.text = element_text(size = 20, colour = "black", face = "bold"),
          legend.title = element_blank(),
          legend.key = element_blank(),
          legend.key.size = unit(1, "cm"),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          panel.background = element_blank(),
          axis.line.x = element_line(colour = 'black', size = 1.6),
          axis.line.y = element_line(colour = 'black', size = 1.6),
          plot.margin=unit(c(.5,.5,.5,.5), "cm"))
  
  if (save) {
    ggsave(plot=plot, filename=filename, width=10, height=5)
  } else {
    print(plot)
  }
}


k_throughput_graph <- function(throughput_data, filename, save=FALSE) {
  plot <- ggplot(throughput_data, aes(x=k, y=thru)) +
    geom_line(size = 1.2) +
    labs(x = "K", y = "Throughput (Mbps)") +
    coord_cartesian(ylim = c(0, 100), xlim=c(0, 60)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_x_continuous(breaks = seq(0, 60, by = 20)) +
    theme_bw() + 
    theme(axis.title.y = element_text(size=20, margin = margin(0, 15, 0, 0), face="bold"),
          axis.title.x = element_text(size=20, margin = margin(15, 0, 0, 0), face="bold"),
          axis.text.y = element_text(size=16, color = "black"), 
          axis.text.x = element_text(size=20, color = "black"), 
          axis.ticks = element_line(size=1.6, color = "black"),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          panel.background = element_blank(),
          axis.line.x = element_line(colour = 'black', size = 1.6),
          axis.line.y = element_line(colour = 'black', size = 1.6),
          plot.margin=unit(c(.5,.5,.5,.5), "cm"))
  
  if (save) {
    ggsave(plot=plot, filename=filename, width=8, height=5)
  } else {
    print(plot)
  }
}