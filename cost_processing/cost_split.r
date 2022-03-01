library(ggplot2)
library(dplyr)  
library(forcats)
library(tidyr)
library(reshape2)

df <- read.csv(file = 'cost.csv')

dodge <- position_dodge(width = 0.9)

df$size <- as.factor(df$size)

df <- subset(df, select = -c(median_overhead,total))

small_df = df[df$size == '10000',]

levels(small_df$composition)[4] <- 'client_side_10k'

medium_df = df[df$size == '100000',]
medium_client = subset(medium_df, medium_df$composition == 'client_side')
medium_client$composition = 'client_side_100k'

small_df <- rbind(small_df, medium_client)

large_df = df[df$size == '1000000',]
large_client = subset(large_df, large_df$composition == 'client_side')
large_client$composition = 'client_side_1M'

small_df <- rbind(small_df, large_client)

melted_df = melt(small_df, 
          id.vars = c("size", "composition"),
          variable.name = "cost_source", 
          value.name = "cost_value")

levels(melted_df$cost_source) <- list(
  `Lambda Compute Time` = "lambda_duration",
  `Lambda Data Transfer` = "lambda_data",
  `S3 Reads` = "s3_read",
  `S3 Writes` = "s3_write",
  `SNS Data Out Transfer` = "sns_data_out",
  `DynamoDB Reads` = "dynamodb_read",
  `DynamoDB Writes` = "dynamodb_write",
  `SF State Transitions` = "sf_state_transitions",
  `SF Workflow Requests` = "sf_express_requests",
  `SF Memory Duration` = "sf_express_duration",
  `EC2 On-Demand Per Day` = "ec2"
)

levels(melted_df$composition) <- list(
  `Sequence` = "synchronous_sequence", 
  `Async Sequence` = "asynchronous_sequence",
  `Routing Slip` = "routing_slip",
  `Coordinator` = "coordinator",
  `Async Coordinator` = "async_coordinator",
  `Message Queue` = "message_queue",
  `Storage-based`	= "storage_based",
  `Event Sourcing` = "event_sourcing",
  `Blackboard` = "blackboard",
  `Step Functions Standard` = "step_functions",
  `Step Functions Express` = "step_functions_express",
  `Compiled` = "compiled",
  `Client-side (10k)` = "client_side_10k",
  `Client-side (100k)` = "client_side_100k",
  `Client-side (1M)` = "client_side_1M"
)

melted_df %>%
  ggplot(aes(fill=cost_source, y=cost_value, x=composition)) +
  geom_bar(position="fill", stat="identity", color="black") +
  scale_y_continuous(breaks = c(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)) +
  guides(fill=guide_legend(title="Cost Source")) + 
  ylab("Cost Distribution") +
  theme(axis.text.x = element_text(angle = 45, vjust=1, hjust=1)) + 
  theme(axis.title.x=element_blank()) 
  

ggsave("costs_distribution.pdf", device=cairo_pdf, height=5, width=5 * 1.5)

