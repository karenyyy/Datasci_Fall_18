## Import Packages
library(ggplot2)
library(plyr)
library(knitr)
library(lsmeans)
library(multcomp)
library(xtable)

## Dataset Loading
class=c(rep("freshmen", 12), 
        rep("sophomore", 12),
        rep("junior", 12),
        rep("senior", 12))
major=c(rep(c(rep("Engineering", 4), 
              rep("Business", 4),
              rep('Liberal Arts', 4)),
            4))
num_of_dues_per_week = c(5, 4, 6, 7,
                         4, 3, 3, 5,
                         2, 3, 4, 4,
                         6, 5, 8, 7,
                         6, 3, 4, 6,
                         4, 3, 3, 4,
                         4, 6, 4, 5,
                         5, 4, 6, 4,
                         4, 5, 5, 4,
                         6, 5, 5, 7,
                         6, 4, 5, 6,
                         4, 2, 3, 3)
avg_sleep_hrs_per_week=c(7.1, 7.5, 7.2, 6.9, 
                         7.1, 7.6, 7.4, 7.1,
                         8.5, 8.3, 8.0, 8.1,
                         7.0, 7.4, 6.4, 6.7,
                         7.3, 8.0, 6.4, 7.5,
                         8.0, 8.3, 8.2, 7.9,
                         6.5, 6.6, 7.0, 7.2,
                         7.5, 7.7, 7.8, 7.8,
                         7.1, 7.7, 7.8, 7.6,
                         6.4, 6.9, 5.9, 6.1,
                         6.5, 7.3, 6.8, 6.4,
                         7.4, 8.0, 7.3, 7.8)
df=data.frame(class, major, num_of_dues_per_week, avg_sleep_hrs_per_week)

## Exploratory Analysis

### Average sleeping hours 
df_sleep <- ddply(df, .(class), transform, pos = cumsum(avg_sleep_hrs_per_week) - (0.5 * avg_sleep_hrs_per_week)) 
df_sleep$class_adjusted = factor(df_sleep$class, levels=c('freshmen','sophomore','junior','senior'))

ggplot(df_sleep, aes(x = major, y = avg_sleep_hrs_per_week*0.25)) + 
  geom_bar(stat="identity") + 
  facet_grid(.~class_adjusted) +
  ylab('Average sleeping hours per week') + 
  xlab('Majors') +
  ggtitle('Average sleeping hours per week of different majors') +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(axis.text.x = element_text(angle = 90, size = 8))

ggplot(df_sleep, aes(x=major, y=avg_sleep_hrs_per_week, color=major)) +
        geom_boxplot() +
        facet_grid(vars(class_adjusted)) +
        ylab('Average sleeping hours per week') +
        ggtitle('Avgerage sleeping hours per week based on class standing and majors in PSU') +
        theme(plot.title = element_text(hjust = 0.2)) +
        ylim(min(df$avg_sleep_hrs_per_week)-0.2, max(df$avg_sleep_hrs_per_week)+0.2)

### Number of dues per week
df_due <- ddply(df, .(class), transform, pos = cumsum(num_of_dues_per_week) - (0.5 * num_of_dues_per_week)) 
df_due$class_adjusted = factor(df_due$class, levels=c('freshmen','sophomore','junior','senior'))

ggplot(df_due, aes(x = major, y = num_of_dues_per_week*0.25)) + 
  geom_bar(stat="identity") + 
  facet_grid(.~class_adjusted) +
  ylab('Average sleeping hours per week') + 
  xlab('Majors') +
  ggtitle('Number of dues per week of different majors') +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(axis.text.x = element_text(angle = 90, size = 8))

ggplot(df_due, aes(x=major, y=num_of_dues_per_week, color=major)) +
        geom_boxplot() +
        facet_grid(vars(class_adjusted)) +
        ylab('Number of dues per week') +
        ggtitle('Number of dues per week based on class standing and majors in PSU') +
        theme(plot.title = element_text(hjust = 0.2)) +
        ylim(min(df$num_of_dues_per_week)-0.2, max(df$num_of_dues_per_week)+0.2)

## Before model building

### check whether the interaction between class standing and num_of_dues_per_week
mod1 <- aov(avg_sleep_hrs_per_week ~ I(num_of_dues_per_week-mean(num_of_dues_per_week)) + class, data = df)
mod2 <- aov(avg_sleep_hrs_per_week ~ I(num_of_dues_per_week-mean(num_of_dues_per_week))*class, data = df)
anova(mod1, mod2)

### check whether the interaction between major and num_of_dues_per_week
mod1 <- aov(avg_sleep_hrs_per_week ~ I(num_of_dues_per_week-mean(num_of_dues_per_week)) + major, data = df)
mod2 <- aov(avg_sleep_hrs_per_week ~ I(num_of_dues_per_week-mean(num_of_dues_per_week))*major, data = df)
anova(mod1, mod2)

### diagnostics of linearity and equal slopes assumptions
qplot(x = df$num_of_dues_per_week, 
      y = df$avg_sleep_hrs_per_week, 
      col = df$class,
      xlab = 'Number of dues per week',
      ylab = 'Average sleeping hours per week') + 
geom_abline(intercept = 8.7053, 
            slope = -0.3025, 
            color="red", 
            linetype="dashed", 
            size=1)

## ANCOVA Model

### test the significance of interaction terms
aov.sleep=aov(avg_sleep_hrs_per_week~class+major+class:major+I(num_of_dues_per_week-mean(num_of_dues_per_week)), data = df)
anova(aov.sleep)

### check residuals Normality and Variance Constance Violation
par(mfrow=c(2,2))
plot(aov.sleep)

### interaction plot
interaction.plot(x.factor = df$major, trace.factor = df$class,
                response = df$avg_sleep_hrs_per_week, type ="b",col = 2:3,
                xlab ="Majors", 
                ylab ="Average sleeping hours per week",
                trace.label ="class standing")

### test the pairwise difference of interactive terms
lsminter=lsmeans(aov.sleep, ~ class:major)
contrast(lsminter,method="pairwise")
contrast_inter = cld(lsminter, alpha=0.05)
plot(contrast_inter)


