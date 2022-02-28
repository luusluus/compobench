library(ggplot2)
library(dplyr)  


data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(median = median(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- plyr::rename(data_sum, c("median" = varname))
  return(data_sum)
}

file_names <- list.files('.', recursive=T, pattern="*.csv")

df <- do.call(rbind, lapply(file_names, read.csv, row.names="workflow_instance_id"))


df2 <- data_summary(df, varname="overhead", 
                    groupnames=c("composition", "is_cold"))

df2 <- transform(df2, p=overhead+3*sd)

df2$composition <- recode_factor(df2$composition, 
                                 sequence = "SS",
                                 coordinator = "CO",
                                 async_sequence = "AS",
                                 routing_slip = "RS",
                                 async_coordinator = "AC", 
                                 event_sourcing = "ES",
                                 message_queue = "MQ",
                                 storage = "SB",
                                 workflow_engine = "SF",
                                 client_side = "CS",
                                 compiled = "COM",
                                 )
df2 = df2[df2$is_cold == 'cold',]
df2$is_cold <- recode_factor(df2$is_cold,
                             cold = "Cold Start",
                             warm = "Warm Function")

p<- ggplot(df2, aes(x=composition, y=overhead)) + 
  geom_bar(stat="identity", color="black", fill="lightblue", position=position_dodge()) + 
  # coord_cartesian(ylim=c(0, 13)) + 
  ylab("Overhead (s)") +
  coord_cartesian(ylim=c(0,6.7)) +
  xlab(NULL) +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) +
  scale_y_continuous(expand = expansion(mult = c(0, .1)), breaks = scales::pretty_breaks(n = 10)) +
  theme(axis.text.x = element_text(size = 11)) + 
  theme(axis.line = element_line(size = 0.5, color = rgb(0,0,0,max=255))) +
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0))) +
  theme(axis.ticks.x=element_blank()) + 
  theme(
    axis.text.x = element_text(size = 20),
    axis.title.y = element_text(size = 26),
    axis.text.y = element_text(size = 24)) +

  theme(panel.grid.major.x = element_blank()) + 
  theme(legend.title=element_blank()) + 
  theme(legend.position="bottom")


print(p)

aspect_ratio <- 1.5

ggsave("overhead_results.pdf", device=cairo_pdf, height=5, width= 5 * aspect_ratio)
