library(ggplot2)
library(dplyr)  
library(forcats)
df <- read.csv(file = 'cost.csv')

dodge <- position_dodge(width = 0.9)

df$size <- as.factor(df$size)

max_cost <- max(df$total) + 10

levels(df$composition) <- list(
  `Sequence` = "synchronous_sequence", 
  `Async Sequence` = "asynchronous_sequence",
  `Routing Slip` = "routing_slip",
  `Client-side` = "client_side",
  `Compiled` = "compiled",
  `Coordinator` = "coordinator",
  `Async Coordinator` = "async_coordinator",
  `Message Queue`	= "message_queue",
  `Storage-based`	= "storage_based",
  `Event Sourcing` = "event_sourcing",
  `Blackboard-based` = "blackboard",
  `Step Functions Standard` = "step_functions",
  `Step Functions Express` = "step_functions_express"
)

df %>%
  mutate(composition = fct_reorder(composition, total)) %>%
  mutate(size = fct_reorder(size, total)) %>%
  ggplot(aes(x = size, y = total, fill = factor(composition))) +
    geom_bar(stat = "identity", position = position_dodge(), color="black") +
    scale_y_sqrt(limits = c(0, max_cost), breaks = (1:10)^2, expand = c(0,0)) + 
    ylab("Economic Cost ($)") +
    xlab("Workflows / Month") +
    guides(fill=guide_legend(title="Composition"))
  
aspect_ratio <- 1.5

ggsave("costs_results.pdf", device=cairo_pdf, height=7, width= 7 * 1.5)

