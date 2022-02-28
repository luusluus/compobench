library(ggplot2)
library(dplyr)  

file_names <- list.files('.', recursive=T, pattern="*.csv")

df <- do.call(rbind, lapply(file_names, read.csv, row.names="workflow_instance_id"))


aspect_ratio <- 1.5


for (composition in levels(factor(df$composition))){
  sub_df = df[df$composition == composition,]
  ggplot(sub_df, aes(x=is_cold, y=overhead)) +
    geom_violin(trim = TRUE, alpha = .8, width = 1) +
    geom_boxplot(width=0.1, color="grey", alpha=0.2) +
    ylab("Overhead (s)") +
    xlab(NULL) +
    theme(axis.text.x = element_text(size = 11)) +
    theme(axis.ticks.x=element_blank()) +
    theme(panel.grid.major.x = element_blank()) + 
    theme(axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0))) + 
    theme(
      axis.title.x = element_text(size = 26),
      axis.text.x = element_text(size = 24),
      axis.title.y = element_text(size = 26),
      axis.text.y = element_text(size = 24))

  ggsave(paste("overhead_", composition, "_violin.pdf", sep=""), device=cairo_pdf, height=5, width= 5 * aspect_ratio)
}



