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
    path = file.path(root_dir, e, c, "word_alignment.csv")
    if (! file.exists(path)){
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


data$utt_id <- paste(as.character(data$file), as.character(data$begin), sep='_')

data.subset <- subset(data, evaluation %in% c("torchaudio_mms_fa", "nemo_forced_aligner", "mfa_3.0", "arpa_1.0", "whisperx"))

plotData <- summarySE(data=data.subset, measurevar = 'alignment_score', groupvars=c('evaluation', 'corpus'))

corpus_label <- as_labeller(c(buckeye="Buckeye", timit="TIMIT"))
evaluation_label <- as_labeller(c(arpa_3.0="ARPA 3.0", mfa_3.0="MFA 3.0", nemo_forced_aligner="NeMo", torchaudio_mms_fa="Wav2Vec2"))

ggplot(aes(x=evaluation_label(evaluation), y=mean * 1000), data=plotData) + geom_point(size = 5, color='#FB5607') +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5, color='#FB5607') +
  ylab('Word boundary error (ms)') + xlab('Alignment condition') +ggtitle('Word boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) + facet_trelliscope(~corpus_label(corpus), ncol = 2, scales="free_x")

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 2.5) +
  ylab('Word boundary error (ms)') + xlab('Aligner') +ggtitle('Word boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(labels=c("MFA 1.0", "MFA 3.0", "NeMo", "Wav2Vec2.0", "WhisperX"))  +
  scale_color_manual(values=c("#FB5607", "#FFBE0B"), labels=c('Buckeye', "TIMIT"), name='Corpus')

ggsave("docs/source/_static/benchmarks/word_alignment.svg", width=blog_width, height=blog_height, units="px", dpi=blog_dpi)

ggsave("docs/source/_static/benchmarks/word_alignment.png", width=1500, height=800, units="px", dpi=200)

plotData %>% mutate(Evaluation = recode_factor(evaluation, torchaudio_mms_fa = "Wav2Vec2", nemo_forced_aligner = "NeMo", mfa_3.0 = "MFA 3.0", arpa_3.0 = 'ARPA 3.0', arpa_1.0 = "ARPA 1.0", whisperx = "WhisperX"), Corpus = recode_factor(corpus, buckeye="Buckeye", timit="TIMIT"), Error = round(mean*1000,1)) %>% group_by(Evaluation, Corpus) %>% select(Evaluation, Corpus, Error) %>% write_csv("docs/source/_static/benchmarks/word_alignment.csv")

# Debugging


subset(data, corpus=='timit' & phone_set=='mfa') %>% group_by(version) %>% summarise(n())

t = subset(data.subset, evaluation=="torchaudio_mms_fa" & corpus=='timit') %>% inner_join(subset(data, evaluation=="mfa_3.0"), by="utt_id", suffix = c(".torchaudio", '.mfa'))

t$diff <- t$alignment_score.mfa - t$alignment_score.torchaudio
