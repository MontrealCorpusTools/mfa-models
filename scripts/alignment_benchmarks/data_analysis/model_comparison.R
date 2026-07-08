root_dir = "D:/Data/experiments/mfa_model_benchmarks/huggingface_models/alignment_comparison"

intervals = data.frame()

data = data.frame()

evals = list.dirs(root_dir, recursive = F, full.names = F)

for (e in evals){
  print(e)
  path = file.path(root_dir, e, "interval_analysis.csv")
  if (!file.exists(path)){
    next
  }
  print(path)
  d = read_csv(path, show_col_types = F, lazy=F)
  d$utterance <- paste(d$file, str_replace_all(as.character(d$utterance_begin), '\\.', '-'), str_replace_all(as.character(d$utterance_end), '\\.', '-'), sep="-")
  d$evaluation = e
  d$speaker = as.character(d$speaker)
  intervals = bind_rows(intervals,d)

  path = file.path(root_dir, e, "alignment_reference_evaluation.csv")
  if (!file.exists(path)){
    next
  }
  print(path)
  d = read_csv(path, show_col_types = F, lazy=F)
  d$alignment_score <- as.numeric(d$alignment_score)
  d$utterance <- paste(d$file, str_replace_all(as.character(d$begin), '\\.', '-'), str_replace_all(as.character(d$end), '\\.', '-'), sep="-")
  d$speaker = as.character(d$speaker)
  d$evaluation = e
  data = bind_rows(data,d)
}

intervals$evaluation = factor(intervals$evaluation)
intervals$phone <- factor(intervals$phone)
intervals$begin_error <- intervals$begin_error
intervals$end_error <- intervals$end_error
intervals$abs_begin_error <- abs(intervals$begin_error) * 1000
intervals$abs_end_error <- abs(intervals$end_error) * 1000
intervals$abs_boundary_error <- intervals$abs_begin_error + intervals$abs_end_error

speech_intervals =  intervals %>% subset(!phone %in% c('sil', '[SIL]') & !is.na(begin_error))

ggplot(data=speech_intervals, aes(x=begin_error)) + geom_histogram()+facet_wrap(~evaluation)

speech_intervals %>% subset(begin_error< -2) %>% View


t <- subset(speech_intervals, file=="CZ004_124")

summary(data)


plotData <- summarySE(data, "alignment_score", "evaluation")
ggplot(plotData, aes(y=mean, x=evaluation)) + geom_point()

ggplot(data=data, aes(x=alignment_score)) + geom_histogram()+facet_wrap(~evaluation)
