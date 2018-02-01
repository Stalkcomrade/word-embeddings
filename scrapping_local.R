library(stringr)
library(magrittr)
library(tidyr)
library(rvest)
library(stringr)

path = "/home/stlk/Desktop/pwc/imdb_additional/train/"

pgs = paste(readLines(str_c(path, "current.html")), collapse="\n")

#### Making a df with parsed data

df = data.frame(paper_name = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/h1") %>%
                  html_text(),
                rating = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span") %>% 
                  html_text(),
                n_votes = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/a/span") %>% 
                  html_text(),
                metacritic = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/a/div/span") %>% 
                  html_text(),
                director = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[3]/div[2]/div[1]/div[2]/span") %>% 
                  html_text(),
                screenplay = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[3]/div[2]/div[1]/div[3]") %>% 
                  html_text(),
                stars = read_html(x = pgs) %>% 
                  html_node(xpath = "/html/body/div[1]/div/div[4]/div[5]/div[1]/div/div/div[3]/div[2]/div[1]/div[4]") %>% 
                  html_text())


write.csv(str_c(path, "current.csv"), x = df)
