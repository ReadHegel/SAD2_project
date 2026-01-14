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
ggplot(data %>% filter(freq==1), aes(x=factor(var_num), y=jaccard_result)) +
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



# linear model gives good results *if* we use only data from freq == 1
data_with_dummies <- dummy_cols(data) %>% filter(freq==1)
linear_model <- lm(jaccard_result ~
                     var_num + steps + numtraj + attper + mode_asynchronous + score_type_BDE, data_with_dummies)
summary(linear_model)

# but not given everything else the correlation actually has a very high p value
cor.test(data$attper, data$jaccard_result, method = "spearman")


colnames(data)


# we see that if we filter by only freq 1 we have much more consistent results and its always better to use synchronous with more steps
ggplot(data %>% filter(freq==1), aes(x=mode,y=steps,fill=jaccard_result)) + geom_tile() + facet_wrap(~var_num)

# the synchronous data is less resistant to less frequent probes
ggplot(data, aes(x=mode,y=steps,fill=jaccard_result)) + geom_tile() + facet_wrap(~freq)


data %>% group_by(freq) %>% summarise(med=median(jaccard_result))

ggplot(data, aes(x=mode,y=score_type,fill=jaccard_result)) + geom_tile() + facet_grid(numtraj~steps)

ggplot(data, aes(x=mode,y=score_type,fill=jaccard_result)) + geom_tile()

summary(data %>% filter(freq==1, var_num==10))

ggplot(data %>% filter(freq==1), aes(x=factor(steps), y=jaccard_result)) +
  geom_violin()


ggplot(data %>% filter(var_num == 13), aes(x=factor(freq), y=jaccard_result)) + geom_violin()

ks.test((data %>% filter(score_type=='MDL'))$jaccard_result, (data %>% filter(score_type=='BDE'))$jaccard_result)
