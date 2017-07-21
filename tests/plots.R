queue_time_graph <- function(queue_data, filename) {

  plot <- ggplot(queue_data, aes(x=time, y=q_len, colour = cong_ctl, linetype = cong_ctl)) +
    geom_line(size=1.2) + 
    labs(x = "Time (Seconds)", y = "Queue Length") +
    coord_cartesian(ylim = c(0, 400), xlim=c(0, 60)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_linetype_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c(3, 1), labels = c("TCP Reno", "DCTCP")) +
    scale_color_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c("black", "dark gray"), labels = c("TCP Reno", "DCTCP")) +
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

  ggsave(filename=filename, width=8, height=5, plot=plot)
}


queue_cdf_graph <- function(queue_data, filename) {
  
  plot <- ggplot(queue_data, aes(x=time, y=q_len, colour = cong_ctl, linetype = cong_ctl)) +
    geom_line(size=1.2) + 
    labs(x = "Time (Seconds)", y = "Queue Length") +
    coord_cartesian(ylim = c(0, 400), xlim=c(0, 60)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_linetype_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c(3, 1), labels = c("TCP Reno", "DCTCP")) +
    scale_color_manual(limits = c("reno_2", "dctcp_2"), breaks = c("reno_2", "dctcp_2"), values = c("black", "dark gray"), labels = c("TCP Reno", "DCTCP")) +
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
  
  ggsave(filename=filename, width=8, height=5, plot=plot)
}