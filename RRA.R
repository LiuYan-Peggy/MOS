library(RobustRankAggreg)

rra <- function(df, N){
  r_new <- t(df)
  #print(r_new)
  #print(dim(r_new))
  rmat = matrix(0, N, dim(r_new)[2])
  ncol = dim(r_new)[2]
  for(i in 1:N){
    for(j in 1:ncol){
      rmat[i, j] <- r_new[i, j]
    }
  }
  rownames(rmat) <- c(1:N)
  #print(rmat)
  ag = aggregateRanks(rmat=rmat, method = "stuart")
  #ag <- aggregateRanks(rmat=rmat, method = "RRA")
  write.csv(ag, file="rra.csv", quote=F)
  #return(ag)
}
