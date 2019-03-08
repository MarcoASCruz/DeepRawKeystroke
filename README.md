#DeepRawKeystroke (DRK)

This documentation explains how to use the DeepRawKeystroke (DRK), a deep neural network able to recognize users based on keystroke dynamics raw data. You will be able to see details about DRK [in this paper](). 

## Environment Configuration

In order to run the DRK it’s necessary to set up the computational environment properly. Some of the most important requirements are the Python (3.6.2) and some libs like mysql-connector (I use MySQL 5.7) , keras (2.1.5), among others. In order to speed up the environment configuration and also give more details about the used libraries, two conda envs (if you want to learn more about conda envs, please check out [this link](https://docs.anaconda.com/anaconda/)) were made available in “"/envConfigs” directory: DRKLinuxEnv.yaml and DRKWindowsEnv.yml. As the names suggest, the files correspond to the environment configurations for Linux and Windows. See how to import conda envs [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

## Datasets

The data that was used to evaluate the DRK are available in "/data/datasets". Each file corresponds to a different dataset named as presented in the table below. This table also have the users and samples amount (second and third columns) and the references (in [latex format](https://www.latex-project.org/)) to the works that published the original data. To access the datasets it’s necessary to run the .sql files in MySQL (5.7). The datasets contains the raw data already cleaned and adjusted (you can see more in the [published  paper]()). The raw data, associated with the corresponding user and sample, are available in table “user_string_keystrokes”.


| name                      | users | samples | reference                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------------------|-------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| killourhy_and_maxion_2009 | 51    | 20400   | @inproceedings{killourhy2009comparing, title={Comparing anomaly-detection algorithms for keystroke dynamics}, author={Killourhy, Kevin S and Maxion, Roy A}, booktitle={Dependable Systems \& Networks, 2009. DSN'09. IEEE/IFIP International Conference on}, pages={125--134}, year={2009}, organization={IEEE} }                                                                                             |
| greyc_giot_2009           | 133   | 7544    | @INPROCEEDINGS{ giot2009benchmark, author = {Giot, Romain and El-Abed, Mohamad and Rosenberger Christophe}, title = {GREYC Keystroke: a Benchmark for Keystroke Dynamics Biometric Systems}, booktitle = {IEEE International Conference on Biometrics: Theory, Applications and Systems (BTAS 2009)}, year = {2009}, publisher = {IEEE Computer Society}, address = {Washington, District of Columbia, USA}, } |
| rhu_2014                  | 51    | 955     | @INPROCEEDINGS{rhu2014benchmark, title = {RHU Keystroke: A Mobile-based Benchmark for Keystroke Dynamics Systems}, author = {El-Abed, Mohamad and Dafer, Mostafa and El Khayat, Ramzi}, Booktitle = {Proceedings of the 48th IEEE International Carnahan Conference on Security Technology} year = {2014} }                                                                                                    |
| antal_2016_mobikey        | 54    | 10313   | @incollection{antal2016mobikey, title={The MOBIKEY Keystroke Dynamics Password Database: Benchmark Results}, author={Antal, Margit and Nemes, Lehel}, booktitle={Software Engineering Perspectives and Application in Intelligent Systems}, pages={35--46}, year={2016}, publisher={Springer} }                                                                                                                |
| antal_2015                | 42    | 2142    | @article{antal2015keystroke, title={Keystroke dynamics on android platform}, author={Antal, Margit and Szab{\'o}, L{\'a}szl{\'o} Zsolt and L{\'a}szl{\'o}, Izabella}, journal={Procedia Technology}, volume={19}, pages={820--826}, year={2015}, publisher={Elsevier} }                                                                                                                                        |

## Experiments

After create the databases, you can do experiments to evaluate the DRK performance using the codes in “/experiments”. Each directory in “/experiments” has two files, one, “analyseRawData.py”, to execute experiments using just the raw data and another, “analyseAugmentedRawData.py”, that do data augmentation before run the DRK. Thus, you can run experiments executing in terminal something like: “python analyseRawData.py”.

If you have some CPU cores available and want to speed up the experiments, use parallel processes. You can do this running for example the “analyseRawDataParallelProcesses.py” in “/experiments/killourhyAndMaxion”.

## Contact

If you want contact me, please send a message to marco.aurelio.s.cruz@gmail.com
