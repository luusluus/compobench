library(ggplot2)
library(dplyr)
library(here)
library(hrbrthemes)
library(viridis)

df <- read.csv(file = here("out.csv"))

# df$composition <- levels(with(df, reorder(composition, cc_avg)))
df$composition <- factor(df$composition, levels = levels(with(df, reorder(composition, cc_avg))))

levels(df$composition) <- list(
  `Sequence` = "sync-function-sequence", 
  `Async Sequence` = "async-function-sequence",
  `Routing Slip` = "routing-slip",
  `Client-side` = "client-side-scheduling",
  `Compiled` = "compiled-sequence",
  `Coordinator` = "coordinator",
  `Async Coordinator` = "async-coordinator",
  `Message Queue`	= "message-queue-based",
  `Storage-based`	= "storage-based",
  `Event Sourcing` = "event-sourcing",
  `Blackboard-based` = "blackboard-based",
  `Step Functions` = "workflow-engine"
)

df %>%
  arrange(desc(loc_total)) %>%
  ggplot(aes(x=time_delta, y=cc_avg, size=loc_total, fill=composition)) +
  geom_point(alpha=0.5, shape=21, color="black") +
  scale_size(range = c(.1, 24), name="SLOC") +
  scale_fill_discrete() +
  scale_fill_hue() +
  guides(fill = guide_legend(override.aes = list(size = 5))) +
  theme_ipsum() +
  theme(legend.position="right") +
  ylab("Average CC (McCabe)") +
  xlab("Development Time (h)") +
  theme(axis.title.x = element_text(vjust=0, hjust=0.5, size=13)) +
  theme(axis.title.y = element_text(vjust=5, hjust=0.5, size=13)) +
  theme(axis.line = element_line(size = 0.5, color = rgb(0,0,0,max=255))) +
  ylim(1, 2.1) +
  xlim(0, 17) +


  ggsave("programmability_results.pdf", device=cairo_pdf, height=7, width= 7 * 1.5)