# okay lets look at how we do that

# we first need to import all necessary stuff into the enviroment
#   SMAC3 components - needs numerical or categorical params) - look at the parameters we need to do that. Should be fine tho
#   scikit learn components
#   have a dataset to test this on and work on during processing
#   prerequisites and preprocessing  methods we need to pursue all the different implementations

# SMBO general Process

# take initial config and instances and make it incumbent (Theta, II, ThetaInc, R = Runtime)
# until R is up do:
#   fit the surrogate model M
#   choose from M list of promising configs using ThetaInc and Theta of promising params - Result is ThetaNew
#   test ThetaNew and ThetaInc with II and a defined cost function c, taking into account run configs R
#       Intensifying: using promising ThetaNews, the ThetaInc, the Model M, sequence of runs R, time constraint for
#       entire intensify loop (if exceeded and above 2 then stops), Instances II, cost function c
#           for each Theta do until time spend for loop exceeds TIntensify and loop > 2
#               If R includes less than maxR runs wirh config ThetaInc do:
#                   sample random PI instance from set of instances II
#                   draw random seed s
#                   executeRun with Target Algo seqquence R, thetaInc, sampled seed and instance - adding this to target algos Run R
#               set N = 1
#               while abode is true
#                   sMissing = instance, seed pairs which are missing from ThetaNew when comparing to thetaInc
#                   sToRun = random subset of sMissing of size min(N, sMissing)
#                   for each element in sToRun do: executeRun with ThetaNew, instance and seed - assigning to target algo list
#                   sMsssing  = sMissing/sToRun (if there is no more stuff to run, so all instances and seeds have been run for thetaNew, this is impossible)
#                   IICommon (instances) = common instances of ThetaInc and ThetaNew
#                   if (cost of ThetaNew runs, from IIcommon > cost of ThetaInc runs, from IICommon) then break -< inc is better
#                   else if (sMissing = impossbie) then ThetaInc = ThetaNew and break else do n = 2*n (to initiate run with sMissings)


#need to be installed
#pip, SMAC, scikit-learn, ms visual c++, swig, resource
#   requirements need to be installed as well from these packages
#   path needs to be set so that all those files can be found during installation

#all of this does not work on Windows because of missing package permission namely resource
#have to resort to vm and linux to do that
#set it up with som ram and gb stuff
#check which python version is installed - needs to be 3.5+
#setup shared folders, using add service in the box, then use terminal to check that. mMake sure to automount and stuff
#check whether pip3 is installed for python3, if not install using python3
#install swig, scikit learn, smac from smac website
#then lets hope pip and python do work together this time

#for all of this preprocessing is needed
#categorical as well as numerical vars can be considered
