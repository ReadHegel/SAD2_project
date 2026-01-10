#install.packages("here")
#install.packages("ggplot2")
#install.packages("dplyr")
#install.packages("fastDummies")


library(here)
library(ggplot2)
library(dplyr)
library(GGally)
library(fastDummies)


data <- read.csv(here("task1", "all_data.csv"))


# we can see that the more states there are the more probability of encountering a non attractor node
ggplot(data, aes(y=attper, x=factor(var_num))) + geom_violin()

# we can see that the jaccard result and jaccard weighted result are actually very similar and more often than not the same
ggplot(data, aes(x=jaccard_result, y=jaccard_weighted_result)) + geom_point()

mean(data$jaccard_result == data$jaccard_weighted_result)

# the scores are low with median being 0.2
summary(data$jaccard_result)

ggplot(data, aes(x="", y=jaccard_result)) + 
  geom_violin()


# taking the frequency to be 1 is the best and then it gets progressively worse
ggplot(data, aes(x=factor(freq), y=jaccard_result)) + 
  geom_violin()

# we can almost certainly conclude that higher frequency gives worse result
cor.test(data$freq, data$jaccard_result, method = "spearman")

# for some reason it works best on 7 variables
ggplot(data, aes(x=factor(var_num), y=jaccard_result)) + 
  geom_violin()
# test of correlation between var number and result doesn't give anything conclusive
cor.test(data$var_num, data$jaccard_result, method = "spearman")


# turns out synchronous is better for some reason
ggplot(data, aes(x=mode, y=jaccard_result)) + 
  geom_violin()
# synchronous mode has much more zero score entries with p value 0.01
data_with_zero_jaccard <- data %>% mutate(jaccard_zero = (jaccard_result==0))
ggplot(data_with_zero_jaccard, aes(x = jaccard_zero, y=attper)) + geom_violin()
contingency_table <- table(data_with_zero_jaccard$mode, data_with_zero_jaccard$jaccard_zero)
chisq.test(contingency_table)
contingency_table

# score type does not change much
ggplot(data, aes(x=score_type, y=jaccard_result)) + 
  geom_violin()


ggplot(data, aes(x=attper, y=jaccard_result)) + geom_point()




# linear model doesn't actually do anything
data_with_dummies <- dummy_cols(data) %>% filter(var_num == 16)
linear_model <- lm(jaccard_result ~
                     steps + numtraj + freq + attper + mode_asynchronous + score_type_BDE, data_with_dummies)
summary(linear_model)

# but not given everything else the correlation actually has a very high p value
cor.test(data$attper, data$jaccard_result, method = "spearman")

