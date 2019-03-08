###########################################################################
# This is a modified version of evaluation.R code that creates a json     #
# ("outputEER.json") with the results of each user-algorithm              #
#                                                                         #
# by: Marco Cruz                                                         #
###########################################################################


library( MASS );
library( ROCR );
library( stats );


calculateEqualError <- function( userScores, impostorScores ) {

  predictions <- c( userScores, impostorScores );
  labels <- c( rep( 0, length( userScores ) ),
              rep( 1, length( impostorScores ) ) );
  
  pred <- prediction( predictions, labels );

  missrates <- pred@fn[[1]] / pred@n.pos[[1]];
  farates <- pred@fp[[1]] / pred@n.neg[[1]];

  # Find the point on the ROC with miss slightly >= fa, and the point
  # next to it with miss slightly < fa.
  
  dists <- missrates - farates;
  idx1 <- which( dists == min( dists[ dists >= 0 ] ) );
  idx2 <- which( dists == max( dists[ dists < 0 ] ) );
  stopifnot( length( idx1 ) == 1 );
  stopifnot( length( idx2 ) == 1 );
  stopifnot( abs( idx1 - idx2 ) == 1 );

  # Extract the two points as (x) and (y), and find the point on the
  # line between x and y where the first and second elements of the
  # vector are equal.  Specifically, the line through x and y is:
  #   x + a*(y-x) for all a, and we want a such that
  #   x[1] + a*(y[1]-x[1]) = x[2] + a*(y[2]-x[2]) so
  #   a = (x[1] - x[2]) / (y[2]-x[2]-y[1]+x[1])
  
  x <- c( missrates[idx1], farates[idx1] );
  y <- c( missrates[idx2], farates[idx2] );
  a <- ( x[1] - x[2] ) / ( y[2] - x[2] - y[1] + x[1] );
  eer <- x[1] + a * ( y[1] - x[1] );

  return( eer );
}

concatenateStrings <- function(str1, str2) {
  return (paste(str1, str2, sep = ""));
}


###########################################################################
# 3. Main procedure
###########################################################################

#######################
fileContent <- "";

cat("Loading the data file\n");

datafile <- 'input.txt';
if( ! file.exists(datafile) )
  stop( "Password data file ", datafile, " does not exist");

# Retrieve the data and the list of subjects
  
X <- read.table( datafile, header = TRUE );

noneFunction <- function(a){}

userColumnName = "user"
agregatedUsers = aggregate(x = X, by = X[userColumnName], FUN = noneFunction)
subjects <- agregatedUsers[[userColumnName]]

# For each of the detectors, evaluate the detector on each subject,
# and record the equal-error rates in a data frame.

detectorColumnName = "description"
detectorSet = aggregate(x = X, by = X[detectorColumnName], FUN = noneFunction)
detectorSet <- detectorSet[[detectorColumnName]]
print(detectorSet)

fileContent <- ""
fileContent <- concatenateStrings(fileContent, '{"algorithms": [');
for (algorithm in detectorSet) {
  fileContent <- concatenateStrings(fileContent, paste('"', algorithm, '"', ',', sep = ''));
}
fileContent <- substr(fileContent, 1, nchar(fileContent) - 1)

fileContent <- concatenateStrings(fileContent, '], "eers": [');

eers <- list();
for( detectorName in detectorSet ) {

    cat("Evaluating the", detectorName, "detector\n");

    fileContent <- concatenateStrings(fileContent, '[');    
    
    n <- length(subjects);
    eers[[ detectorName ]] <- rep(NA, n);

    for(i in 1:n) {
        userScores <- as.vector(
            as.matrix(
                subset(
                    X,
                    subset = (user == subjects[i] & target == 1 & description == detectorName),
                    select = c(output) 
                )
            )
        );

        impostorScores <- as.vector(
            as.matrix(
                subset(
                    X,
                    subset = (user == subjects[i] & target == 0 & description == detectorName),
                    select = c(output) 
                )
            )
        );

        eer <- calculateEqualError(userScores, impostorScores);

        fileContent <- concatenateStrings(fileContent, eer);

        if (n > i){
          fileContent <- concatenateStrings(fileContent, ', ');
        }

        eers[[ detectorName ]][i] <- eer;
        #cat("\r  ", i, "/", n, ":",eer);
    }
    
    fileContent <- concatenateStrings(fileContent, '],');

    cat("\r  average equal-error:", mean(eers[[detectorName]]), "\n");
}


print(eers)

fileContent <- substr(fileContent, 1, nchar(fileContent) - 1)
fileContent <- concatenateStrings(fileContent, "]}");
fileConn<-file("outputEER.json")
writeLines(fileContent, fileConn)
close(fileConn)

#######################
cat("Tabulating results:\n");

eers <- data.frame( eers );
rownames( eers ) <- subjects;

res <- data.frame(eer.mean = colMeans(eers),
                  eer.sd   = apply( eers, 2, sd ));

print( round( res, digits = 3 ) );
