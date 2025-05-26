library(tidyr)
library(dplyr)
library(readr)
library(stringr)
root_dir = "D:/Data/experiments/alignment_benchmarking/alignments"

evals = list.dirs(root_dir, recursive = F, full.names = F)

data = data.frame()

for (e in evals){
  corpora = list.dirs(file.path(root_dir, e), recursive = F, full.names = F)
  for (c in corpora){

    print(e)
    print(c)
    path = file.path(root_dir, e, c, "alignment_reference_evaluation.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$alignment_score <- as.numeric(d$alignment_score)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$begin), '\\.', '-'), str_replace_all(as.character(d$end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    data = bind_rows(data,d)
  }
}

data$evaluation = factor(data$evaluation)


data$version = "train"
data[str_detect(data$evaluation, '_1.0'),]$version = "1.0"
data[str_detect(data$evaluation, '_2.0'),]$version = "2.0"
data[str_detect(data$evaluation, '_2.0a'),]$version = "2.0a"
data[str_detect(data$evaluation, '_2.1'),]$version = "2.1"
data[str_detect(data$evaluation, '_2.2'),]$version = "2.2"
data[str_detect(data$evaluation, '_3.0'),]$version = "3.0"
data[str_detect(data$evaluation, '_3.1'),]$version = "3.1"
#data[str_detect(data$evaluation, 'trained_2.2'),]$version = "trained_2.2"
data[str_detect(data$evaluation, 'trained_3.0'),]$version = "trained_3.0"
data$version <- factor(data$version)


data$phone_set = "mfa"
data[str_detect(data$evaluation, 'arpa'),]$phone_set = "arpa"
data[str_detect(data$evaluation, 'gp'),]$phone_set = "gp"
data$phone_set <- factor(data$phone_set)

data <- subset(data, !is.na(data$alignment_score))
data = subset(data, word_count > 1)
data = subset(data, !(word_count == 2 & reference_phone_count == 2))

plotData <- summarySE(data=data, measurevar = 'alignment_score', groupvars=c('evaluation', 'corpus','phone_set'))

ggplot(aes(x=evaluation, y=mean * 1000), data=plotData) + geom_point(size = 5, color='#FB5607') +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5, color='#FB5607') +
  ylab('Phone boundary error (ms)') + xlab('Alignment condition') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) + facet_trelliscope(phone_set~corpus, ncol = 2, scales="free_x")

plotData <- summarySE(data=data, measurevar = 'phone_error_rate', groupvars=c('version', 'corpus','phone_set'))

ggplot(aes(x=version, y=mean * 100), data=plotData) + geom_point(size = 5, color='#FB5607') +
  geom_errorbar(aes(ymin = (mean - ci) * 100, ymax = (mean + ci)* 100),size=2, width=0.5, color='#FB5607') +
  ylab('Phone error rate %') + xlab('Alignment condition') +ggtitle('Phone error rate') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) + facet_trelliscope(phone_set~corpus, ncol = 2, scales="free_x")


labphon_data <- subset(data, corpus %in% c('timit', 'buckeye', 'csj', 'seoul') & evaluation %in% c('arpa_1.0', 'gp_1.0', 'mfa_3.0'))

labphon_data[labphon_data$evaluation == 'gp_1.0',]$evaluation = 'arpa_1.0'
labphon_data$evaluation <- factor(labphon_data$evaluation)


plotData <- summarySE(data=labphon_data, measurevar = 'alignment_score', groupvars=c('evaluation', 'corpus'))


ggplot(aes(x=evaluation, y=mean * 1000, color=corpus, group=corpus), data=plotData) +geom_path() + geom_point(size = 2.5)  +
  ylab('Phone boundary error (ms)') + xlab('MFA version') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(labels=c("1.0", "3.0")) +
  scale_color_manual(values=cbbPalette, labels=c('Buckeye', 'CSJ', "Seoul", "TIMIT"), name='Corpus')

ggsave("docs/source/_static/benchmarks/phone_alignment.png", width=1000, height=800, units="px", dpi=200)


uw_colloquium_data <- subset(data, corpus %in% c('timit', 'buckeye', 'csj', 'seoul') & evaluation %in% c('mfa_3.0'))
uw_colloquium_data$corpus <- factor(uw_colloquium_data$corpu, levels=c('timit', 'buckeye', 'csj', 'seoul'))


plotData <- summarySE(data=uw_colloquium_data, measurevar = 'alignment_score', groupvars=c('corpus'))


ggplot(aes(x=corpus, y=mean * 1000), data=plotData) + geom_point(size = 6, color='#FB5607')  +
  ylab('Phone boundary error (ms)') + xlab('Corpus') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(labels=c("English-TIMIT", 'English-Buckeye', 'Japanese-CSJ', "Korean-Seoul"))

ggsave("docs/source/_static/benchmarks/uw_phone_alignment.png", width=1500, height=800, units="px", dpi=150)



t <- subset(data, corpus=='seoul'& version=='3.0')


subset(data, corpus=='buckeye' & phone_set=='mfa') %>% group_by(version) %>% summarise(n())
