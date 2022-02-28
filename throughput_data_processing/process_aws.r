library(ggplot2)
library(dplyr)
library(sqldf)
library(scales)


file_names <- list.files('.', recursive=T, pattern="^aws.*csv$")

df <- do.call(rbind, lapply(file_names, read.csv))

df$rps <- as.factor(df$rps)

aspect_ratio <- 1.5

df <- df %>%
  mutate(workflow_count = case_when(
    composition == 'async_coordinator' ~ invocation_count / 4,
    composition == 'async_sequence' ~ invocation_count / 3,
    composition == 'workflow_engine' ~ invocation_count / 3,
    composition == 'blackboard' ~ invocation_count / 4,
    composition == 'client_side' ~ invocation_count / 3,
    composition == 'compiled' ~ invocation_count,
    composition == 'coordinator' ~ invocation_count / 4,
    composition == 'event_sourcing' ~ invocation_count / 4,
    composition == 'message_queue' ~ invocation_count / 3 ,
    composition == 'routing_slip' ~ invocation_count / 3,
    composition == 'sequence' ~ invocation_count / 3,
    composition == 'storage' ~ invocation_count / 3
  ))

df$workflow_count = round(floor(df$workflow_count), 0)
max_workflow_count <- max(df$workflow_count)
max_throttle_count <- max(df$throttle_count)

for (composition in levels(factor(df$composition))){
   
  sub_df = df[df$composition == composition,]
  
  sub_df %>%
    ggplot(aes(x=rps)) +
    geom_line(aes(y=workflow_count, group=1)) +
    # add a 4 multiplier to get the range to (0, 0.25) instead of (0, 1.00)
    geom_line(aes(y=error_rate * (max_workflow_count * 4) , group=1), color="red") +
    
    scale_y_continuous(
      labels = label_number(suffix = "K", scale = 1e-3, accuracy = 1),
      breaks = seq(0, max_workflow_count, by = 1000),
      limits = c(0, max_workflow_count),
      sec.axis = sec_axis(~.* 1/ (max_workflow_count * 4), name = "Error Rate")
    ) +
    scale_colour_manual(values = c("red", "black")) +
    ggtitle("Workflow Count & Error Rate") +
    labs(y = "Workflow Count",
         x = "Invocation Rate (RPS)") +
    theme(
      plot.title = element_text(size=30, hjust=0.5),
      axis.title.x = element_text(size = 26),
      axis.text.x = element_text(size = 24),
      axis.title.y = element_text(size = 26),
      axis.text.y = element_text(size = 24),
      axis.title.y.right = element_text(
        size=26, 
        margin =  margin(t = 0, r = 0, b = 0, l = 15),
        colour = "red"
      )) +
    
    ggsave(paste("aws_throughput_", composition, "_errorrate.pdf", sep=""), device=cairo_pdf, height=5, width= 5 * aspect_ratio)
  
  
  sub_df %>%
    ggplot(aes(x=rps, y=throttle_count, group=1)) +
    geom_line() +
    scale_y_continuous(
      labels = label_number(suffix = "K", scale = 1e-3, accuracy = 1),
      breaks = seq(0, max_throttle_count, by = 2000),
      limits = c(0, max_throttle_count),
    ) +
    labs(y = "Throttle Count",
         x = "Invocation Rate (RPS)") +
    ggtitle("Throttle Count") +
    theme(
      plot.title = element_text(size=30, hjust=0.5),
      axis.title.x = element_text(size = 26),
      axis.text.x = element_text(size = 24),
      axis.title.y = element_text(size = 26),
      axis.text.y = element_text(size = 24)) +
    
    ggsave(paste("aws_throughput_", composition, "_throttlecount.pdf", sep=""), device=cairo_pdf, height=5, width= 5 * aspect_ratio)
}

