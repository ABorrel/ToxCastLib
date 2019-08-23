#!/usr/bin/env Rscript

# remove assays without enough data
cleanChemical = function(dassays, cutoffassay){
  dtemp = dassays
  i = 1
  imax = dim(dtemp)[1]
  while(i <= imax){
    nbnotest = length(which(is.na(dtemp[i,])))
    nbtested = dim(dtemp)[2] - nbnotest
    if(nbtested <= cutoffassay){
      dtemp = dtemp[-i,]
      imax = imax - 1
    }else{
      i = i + 1    
    }
  }
  return(dtemp)
}

# remove chemical without enough assays results
cleanAssays = function(dassays, cutoffchem){
  dtemp = dassays
  i = 1
  imax = dim(dtemp)[2]
  while(i <= imax){
    nbnotest = length(which(is.na(dtemp[,i])))
    nbtested = dim(dtemp)[1] - nbnotest
    if(nbtested <= cutoffchem){
      dtemp = dtemp[,-i]
      imax = imax - 1
    }else{
      i = i + 1    
    }
  }
  return(dtemp)
}



generateCorAssaysMatrix = function(dassays, prout){
  
  pmatrix = paste(prout, "corAssays.csv", sep = "")
  if(file.exists(pmatrix)){
    dmatrix = read.csv(pmatrix, header = TRUE, row.names = 1)
    return(dmatrix)
  }
  
  nbassays = dim(dassays)[2]
  dcor = data.frame()
  i = 1
  while(i <= nbassays){
    j = i
    while(j <= nbassays){
      dtest = cbind(dassays[,i], dassays[,j])
      dtest = na.omit(dtest)
      if(dim(dtest)[1] > 100){
        valcor = abs(cor(dassays[,i], dassays[,j], use = "complete.obs"))
      }else{
        valcor = NA
      }
      dcor[i,j] = valcor
      dcor[j,i] = valcor
      j = j + 1
    }
    i = i + 1
  }
  colnames(dcor) = colnames(dassays)
  rownames(dcor) = colnames(dassays)
  write.csv(dcor, paste(prout, "corAssays.csv", sep = ""))
  return(dcor)
}


reduceMatrix = function(dcor, din, corcutoff){
  
  # reduce dcor with assays in the dassays
  dcor = dcor[colnames(din),]
  dcor = dcor[,colnames(din)]
  i = 1
  imax = dim(dcor)[1]
  lassayremove = NULL
  while(i < imax){
    ltemp = which(dcor[i,] >= corcutoff)
    if(length(ltemp) == 1 || length(ltemp) == 0){
      i = i + 1
    }else{
      lassays = rownames(dcor)[ltemp]
      nbtest = 10000
      for(assay in lassays){
        nbNA = length(which(is.na(din[,assay])))
        if(nbNA < nbtest){
          nbtest = nbNA
          bestassay = assay    
        }
      }
      for(assay in lassays){
        if(assay != bestassay){
          lassayremove = append(lassayremove, assay)
        }
      }
      i = i + 1
    }
  }
  return(unique(lassayremove))
}

outersect <- function(x, y) {
  sort(c(setdiff(x, y),
         setdiff(y, x)))
}


################
#     MAIN     #
################

args <- commandArgs(TRUE)
pAssays = args[1]
cutoffchem = as.integer(args[2])
cutoffassays = as.integer(args[3])
logtransformation = args[4]
corval = as.double(args[5])
prout = args[6]

#pAssays = "/home/borrela2/cancer/BBN/ModelAssays/AC50all.csv"
#prout = "/home/borrela2/cancer/BBN/ModelAssays/"
#cutoffchem = 7000
#cutoffassays = 150
#logtransformation = "1"
#corval= 0.80

dassays = read.csv(pAssays, sep = "\t", header = TRUE)
rownames(dassays) = dassays[,1]
dassays = dassays[,-1]

# generate the correlation matrix with all assays
dcor = generateCorAssaysMatrix(dassays, prout)

print("=====")
print(paste("=== nb assays: ", dim(dassays)[2], sep = ""))
print(paste("=== nb chem: ", dim(dassays)[1], sep = ""))
dassays = cleanAssays(dassays, cutoffchem) #reduce on assays
print(paste("=== nb assays after cutoff chemical active: ", dim(dassays)[2], sep = ""))
dassays = cleanChemical(dassays, cutoffassays) #reduce on chemical
print(paste("=== nb assays after cutoff assays active: ", dim(dassays)[1], sep = ""))
lassaysdel = reduceMatrix(dcor, dassays, corval)
lkeep = outersect(colnames(dassays), lassaysdel)
dassays = dassays[,lkeep]
print(paste("=== nb assays after cutoff correlation: ", dim(dassays)[2], sep = ""))

if(logtransformation == 1){
  dassays = -log10(dassays)
}

# write assays clean
write.csv(dassays, paste(prout, "Massays_",  cutoffchem, "-", cutoffassays, "_", corval, "_log", logtransformation, ".csv", sep = ""))

