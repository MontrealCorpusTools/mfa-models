library(ggplot2)
library(lme4)
library(stringr)
library(dplyr)
library(tidyr)
library(scales)
library(readr)
library(tidyverse)
library(fs)
library(purrr)
library(svglite)
library(seewave)
library(gganimate)
library(transformr)
library(magick)
library(rsvg)
library(gifski)
library(cowplot)
library(gsignal)
library(colorspace)
library(tidyr)
library(dplyr)
library(plotly)
library(trelliscopejs)
library(stringr)

blog_width = 2400
blog_height =1000
blog_dpi = 175

windowsFonts("Gentium Book Plus" = windowsFont("Gentium Book Plus"))

cbbPalette <- c("#FB5607", "#8338EC", "#FF006E", "#FFBE0B",  "#3A86FF", '#6EC200', '#BA3200', "#009E73")


very_light_yellow = '#FFE819'
light_yellow = '#F9D213'
base_yellow = '#F2BC0C'
dark_yellow = '#BD9105'
very_dark_yellow = '#A07A00'

sky_blue = '#2D99FF'

very_light_blue = '#1265B2'
light_blue = '#0A4B89'
base_blue = '#053561'
dark_blue = '#01192F'
very_dark_blue = '#000C17'


very_light_red = '#FF4619'
light_red = '#D43610'
base_red = '#AA2809'
dark_red = '#761A03'
very_dark_red = '#5C1200'

theme_memcauliffe <- function (base_family="Gentium Book Plus") {
  base_size = 12
  half_line <- base_size/2
  theme_bw(base_size=base_size, base_family=base_family) %+replace%
    theme(
      plot.background = element_rect(fill = "#003566"),
      panel.background = element_rect(fill = "#003566", color = '#003566'),
      panel.border = element_rect(color='#000814', fill='NA'),
      panel.grid.major = element_line(size = 0.25, linetype = 'solid',
                                      colour = "#FFC300"),
      panel.grid.minor = element_line(size = 0.125, linetype = 'solid',
                                      colour = "#FFD60A"),
      axis.text = element_text(size = rel(1.2), colour = "#FFD60A"),
      axis.text.y = element_text(margin = margin(r = 0.8*half_line/2),
                                 hjust = 1, colour = "#FFD60A"),
      axis.title = element_text(colour = "#FFC300", size = rel(1.6)),
      plot.title = element_text(colour = "#FFC300", size = rel(1.8), hjust=0,
                                margin = margin(b = half_line * 1.2)),
      strip.background = element_rect(fill = "#FFC300", colour = NA),
      strip.text = element_text(colour = "#000814", size = rel(1.2),  margin = margin( b = 3, t = 3,  l = 4, r = 4)),
      legend.background = element_blank(),
      legend.key = element_blank(),
      legend.title = element_text(size = rel(1.2), colour = "#FFC300"),
      legend.text = element_text(size = rel(1), colour = "#FFC300"),
    )
}

summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  require(dplyr)

  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }

  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  dots <- lapply(groupvars, as.symbol)

  functions <- list("n()", paste("mean(",measurevar,")", sep = ''), as.formula(paste("~median(",measurevar,")", sep = '')), paste("sd(",measurevar,")", sep = ''))


  # hack to deal with median specified as formula
  names <-  lapply(functions, function(x){if(length(x)>1){as.character(x[2])}else{x[1]}})
  names <- lapply(names, as.name)

  datac <- data %>% group_by_(.dots = dots) %>% summarise_(.dots = functions) %>% rename_(.dots = setNames(names, c('N', 'mean', 'median', 'sd')))

  # Rename the "mean" column

  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval:
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult

  return(datac)
}
