###########################################################################
# evaluation-script.R                                                     #
#                                                                         #
# Comparing Anomaly Detectors for Keystroke Biometrics                    #
# Evaluation Proceedure                                                   #
# R Script                                                                #
#                                                                         #
# by: Kevin Killourhy                                                     #
# date: May 19, 2009                                                      #
###########################################################################

# This script demonstrates how the DSL-StrongPassword data set can be
# used to train and evaluate three anomaly detectors, reproducing the
# results for those anomaly detectors reported in:

#   K.S. Killourhy and R.A. Maxion. "Comparing Anomaly Detectors for
#   Keystroke Biometrics," in Proceedings of the 39th Annual
#   Dependable Systems and Networks Conference, pages 125-134,
#   Estoril, Lisbon, Portugal, June 29-July 2, 2009.  IEEE Computer
#   Society Press, Los Alamitos, California. 2009.

# The script is shared in order to promote open scientific discourse,
# and to encourage other researchers to reproduce and expand upon our
# results (e.g., by evaluating their own, novel anomaly detectors)
# using our data and procedures.

###########################################################################
# Table of Contents
###########################################################################

# 1. Anomaly detectors
# 2. Evaluation functions
# 3. Main procedure

library( MASS );
library( ROCR );
library( stats );


###########################################################################
# 2. Evaluation procedures
###########################################################################

# The calculateEqualError function takes a set of user scores and
# impostor scores, makes an ROC curve using the ROCR functionality,
# and then geometrically calculates the point at which the miss and
# false-alarm (i.e., false-negative and false-positive) rates are
# equal.

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


###########################################################################
# 3. Main procedure
###########################################################################

#######################
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

eers <- list();
for( detectorName in detectorSet ) {
    #print("detectorName")
    #print(detectorName)

    #######################
    cat("Evaluating the", detectorName, "detector\n");

    #print(rep(NA, length(subjects)))
    

    n <- length(subjects);
    eers[[ detectorName ]] <- rep(NA, n);
    #print("eers[[ detectorName ]]")
    #print(eers)
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
        #print("userScores")
        #print(userScores[1:20])
        impostorScores <- as.vector(
            as.matrix(
                subset(
                    X,
                    subset = (user == subjects[i] & target == 0 & description == detectorName),
                    select = c(output)
                )
            )
        );
        #print("impostorScores")
        #print(impostorScores[1:20])

        eer <- calculateEqualError(userScores, impostorScores);
        #print("eer")
        #print(eer)

        eers[[ detectorName ]][i] <- eer;
        cat("\r  ", i, "/", n, ":",eer);
    }
    cat("\r  average equal-error:", mean(eers[[detectorName]]), "\n");
}


#print(eers)

#######################
cat("Tabulating results:\n");

eers <- data.frame( eers );
rownames( eers ) <- subjects;

res <- data.frame(eer.mean = colMeans(eers),
                  eer.sd   = apply( eers, 2, sd ));

print( round( res, digits = 3 ) );
