library(ggplot2)
library(dplyr)
library(sqldf)


file_names <- list.files('.', recursive=T, pattern="^hey.*csv$")

# df <- do.call(rbind, lapply(file_names, read.csv, row.names="Id"))
df <- do.call(rbind, lapply(file_names, read.csv))

df$rps <- as.factor(df$rps)

aspect_ratio <- 1.5

max_median_makespan <- max(df$response_time)

for (composition in levels(factor(df$composition))){
  sub_df = df[df$composition == composition,]

  sub_df %>%
    ggplot(aes(x=rps, y=response_time)) + 
    geom_violin(trim = TRUE, alpha = .8, width = 1) +
    geom_boxplot(width=0.1, color="grey", alpha=0.2) +
    
    
    ylab("Median Makespan (s)") +
    xlab("Invocation Rate (RPS)") +
    ggtitle("Median Makespan") +
    theme(
      plot.title = element_text(size=30, hjust=0.5),
      axis.title.x = element_text(size = 26),
      axis.text.x = element_text(size = 24),
      axis.title.y = element_text(size = 26),
      axis.text.y = element_text(size = 24)) +
    ggsave(paste("hey_throughput_", composition, "_makespan.pdf", sep=""), device=cairo_pdf, height=5, width= 5 * aspect_ratio)
  
  
  # no_error_df = sqldf("SELECT rps, COUNT(*) AS responses FROM sub_df GROUP BY rps")
  # 
  # error_df = sqldf("SELECT rps, COUNT(*) AS error_responses FROM sub_df WHERE status_code != 200 GROUP BY rps")
  # 
  # merged_df = merge(no_error_df, error_df, by="rps", all = TRUE)
  # 
  # merged_df[is.na(merged_df)] <- 0
  # 
  # merged_df['error_rate'] = merged_df$error_responses / merged_df$responses
  # 
  # merged_df %>%
  #   ggplot(aes(x=rps, y=error_rate, group=1)) + 
  #   geom_line() + 
  #   ylab("Error Rate") +
  #   xlab("Invocation Rate (RPS)") +
  #   ggtitle("Error Rate") +
  #   ylim(0, 1) +
  #   theme(
  #     plot.title = element_text(size=34, hjust=0.5),
  #     axis.title.x = element_text(size = 26),
  #     axis.text.x = element_text(size = 24),
  #     axis.title.y = element_text(size = 26),
  #     axis.text.y = element_text(size = 24)) +
  #   
  #   ggsave(paste("hey_throughput_", composition, "_errorrate.pdf", sep=""), device=cairo_pdf, height=5, width= 5 * aspect_ratio)
}