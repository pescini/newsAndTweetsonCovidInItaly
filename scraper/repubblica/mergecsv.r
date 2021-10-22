setwd("")

data = NULL
for(file in list.files("CSV")){
  data = rbind(data,read.csv2(paste0("CSV/",file),fileEncoding = "UTF-8-BOM"))
}

data.table::fwrite(data,"newsfinal.csv",sep = ";")
