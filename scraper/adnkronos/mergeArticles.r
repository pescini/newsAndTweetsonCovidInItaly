setwd("")

read.file = function(path){
  file = readr::read_csv2(path,quote='""',)
  return(file)
}

data1 = NULL
for(file in list.files("CSV")){
  data1 = rbind(data1,read.file(paste0("CSV/",file)))
}
data1$date = as.Date(data1$date,format = "%d %b %Y")

data2 = NULL
for(file in list.files("CSVARTICLE")){
  data2 = rbind(data2,read.file(paste0("CSVARTICLE/",file)))
}

data1 = data1[order(data1$url),]
data2 = data2[order(data2$url),]
sum(data2$url!=data1$url)


data = cbind(data1,data2[,-1])

data = data[order(data$date,data$time),]

readr::write_csv2(data,"ESPERTI.csv")
