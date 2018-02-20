#!/usr/bin/env python

'''
By David French (frenchd@astro.wisc.edu)

$Id:  plot_onsky_absorber_vel.py, v1.0 2/19/18

Plot an impact parameter map showing the locations and velocities of each absorber wrt 
the galaxy 

'''


import sys
import os
import csv
import time


from pylab import *
# import atpy
# from math import *
from utilities import *
from scipy import stats
import getpass
import math
import pickle
import json
import io
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

from scipy.optimize import curve_fit
import matplotlib.ticker as ticker

from matplotlib import rc
fontScale = 14
rc('text', usetex=True)
rc('font', size=fontScale,family='serif',weight='medium')
rc('xtick.major',size=8,width=0.6)
rc('xtick.minor',size=5,width=0.6)
rc('ytick.major',size=8,width=0.6)
rc('ytick.minor',size=5,width=0.6)
rc('xtick',labelsize = fontScale)
rc('ytick',labelsize = fontScale)
rc('axes',labelsize = fontScale)
rc('xtick',labelsize = fontScale)
rc('ytick',labelsize = fontScale)
# rc('font', weight = 450)
# rc('axes',labelweight = 'bold')
rc('axes',linewidth = 1,labelweight='normal')
rc('axes',titlesize='small')


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


def get_data(filename):
    # fields in JSON file are:
    #
    # 'name': galaxy name
    # 'vsys_published': Vhel as found on NED
    # 'dvsys_published': error in Vhel as found in NED
    # 'inclination': inclination
    # 'di': inclination error
    # 'centerTrace': center of spectrum
    # 'distance': best distance to galaxy
    # 'vsys_measured': measured Vhel
    # 'vsys_measured_err': measured error in Vhel
    # 'left_vrot_incCorrected_avg': average left wing velocity, corrected for inc
    # 'left_vrot_incCorrected_avg_err': error in average left wing velocity corrected for inc
    # 'right_vrot_incCorrected_avg': average right wing velocity, corrected for inc
    # 'right_vrot_incCorrected_avg_err':  error in average right wing velocity corrected for inc
    # 'left_vrot_avg': average left wing velocity (redshift subtracted)
    # 'left_vrot_avg_err': error in average left wing velocity (redshift subtracted)
    # 'right_vrot_avg': average right wing velocity (redshift subtracted)
    # 'right_vrot_avg_err': error in average right wing velocity (redshift subtracted)
    # 'vrot_vals': observed velocities (redshift but not inc corrected)
    # 'vrot_errs': errors in observed velocities (redshift but not inc corrected)
    # 'vrot_incCorrected_vals': inclination corrected velocities (redshift subtracted)
    # 'vrot_incCorrected_errs': errors in inclination corrected velocities
    # 'vrot_observed': observed velocities (Vhel + rotation)
    # 'agn': include any information about AGN here
    # 'xVals': physical (kpc) x axis along the slit

    print 'current file: ',filename
    print
    with open(filename) as data_file:
        data = json.load(data_file)
  
#         vrot_vals = data['vrot_vals']
#         vrot_incCorrected_vals = data['vrot_incCorrected_vals']
#         right_vrot_incCorrected_avg = data['right_vrot_incCorrected_avg']
#         left_vrot_incCorrected_avg = data['left_vrot_incCorrected_avg']

        right_vrot_avg = data['right_vrot_avg']
        left_vrot_avg = data['left_vrot_avg']
        
#         xVals = data['xVals']
        inc = data['inclination']
        vsys_measured = data['vsys_measured']
#         galaxyName = data['name']
#         RA_galaxy = data['RAdeg']
#         Dec_galaxy = data['DEdeg']
        dist = data['dist']
        majDiam = data['majDiam']
        PA = data['PA']
#         agn = data['agn']
        
        return vsys_measured, right_vrot_avg, left_vrot_avg, inc, PA, dist, majDiam
        


def main():
    hubbleConstant = 71.0


##########################################################################################
    # get the data
##########################################################################################
    # fields in JSON file are:
    #
    # 'name': galaxy name
    # 'vsys_published': Vhel as found on NED
    # 'dvsys_published': error in Vhel as found in NED
    # 'inclination': inclination
    # 'di': inclination error
    # 'centerTrace': center of spectrum
    # 'distance': best distance to galaxy
    # 'vsys_measured': measured Vhel
    # 'vsys_measured_err': measured error in Vhel
    # 'left_vrot_incCorrected_avg': average left wing velocity, corrected for inc
    # 'left_vrot_incCorrected_avg_err': error in average left wing velocity corrected for inc
    # 'right_vrot_incCorrected_avg': average right wing velocity, corrected for inc
    # 'right_vrot_incCorrected_avg_err':  error in average right wing velocity corrected for inc
    # 'left_vrot_avg': average left wing velocity (redshift subtracted)
    # 'left_vrot_avg_err': error in average left wing velocity (redshift subtracted)
    # 'right_vrot_avg': average right wing velocity (redshift subtracted)
    # 'right_vrot_avg_err': error in average right wing velocity (redshift subtracted)
    # 'vrot_vals': observed velocities (redshift but not inc corrected)
    # 'vrot_errs': errors in observed velocities (redshift but not inc corrected)
    # 'vrot_incCorrected_vals': inclination corrected velocities (redshift subtracted)
    # 'vrot_incCorrected_errs': errors in inclination corrected velocities
    # 'vrot_observed': observed velocities (Vhel + rotation)
    # 'agn': include any information about AGN here
    # 'xVals': physical (kpc) x axis along the slit

#     directory = '/Users/frenchd/Research/inclination/git_inclination/rotation_paper/rot_curves/'
#     filename = 'CGCG039-137-summary4.json'
#     filename = 'RFGC3781-summary4.json'

    
#     with open(directory+filename) as data_file:
#         data = json.load(data_file)    
#         
#         vrot_vals = data['vrot_vals']
#         vrot_incCorrected_vals = data['vrot_incCorrected_vals']
#         right_vrot_incCorrected_avg = data['right_vrot_incCorrected_avg']
#         left_vrot_incCorrected_avg = data['left_vrot_incCorrected_avg']
#         
#         xVals = data['xVals']
#         inc = data['inclination']
#         vsys_measured = data['vsys_measured']
#         galaxyName = data['name']
#         RA_galaxy = data['RAdeg']
#         Dec_galaxy = data['DEdeg']
#         dist = data['dist']
#         majDiam = data['majDiam']
#         inc = data['inclination']
#         PA = data['PA']
#         agn = data['agn']

        # which agn do you want to target?

        # CGCG039-137
#         agnName = 'RX_J1121.2+0326'
#         RA_target = agn[agnName]['RAdeg']
#         Dec_target = agn[agnName]['DEdeg']
        
        # IC5325
#         agnName = 'RBS2000'
#         RA_target = agn[agnName]['RAdeg']
#         Dec_target = agn[agnName]['DEdeg']
        
        # RFGC3781
#         agnName = 'RBS1768'
#         RA_target = agn[agnName]['RAdeg']
#         Dec_target = agn[agnName]['DEdeg']
        
    # this one is for 0 centered
#     xvalStart = xvals[0]
#     xvalEnd = xvals[-1]
#     step = 5
#  
#     lowMean = mean(vels[:6])
#     highMean = mean(vels[-6:])
# 
#     vels2 = vels
#     xvals2 = xvals

##########################################################################################
##########################################################################################
    # collect data
    directory = '/Users/frenchd/Research/inclination/git_inclination/rotation_paper/'
    filename = '{0}salt_galaxy_sightlines.csv'.format(directory)
    theFile = open(filename,'rU')
    tableReader = csv.DictReader(theFile)

    nameList = []
    targetList = []
    combinedNameList = []
    vList = []
    wList = []
#     RA_galaxyList = []
#     Dec_galaxyList = []
    RA_targetList = []
    Dec_targetList = []
    incList = []
    paList = []
    azList = []
    RvirList = []
    markerColorList = []
    VhelList = []
    for t in tableReader:

        name = t['Name']
        target = t['Target']
        lyaV = eval(t['Lya_v'])
        lyaW = eval(t['Lya_W'])
        RA_galaxy = eval(t['RAdeg'])
        Dec_galaxy = eval(t['DEdeg'])
        RA_target = eval(t['RAdeg_target'])
        Dec_target = eval(t['DEdeg_target'])
        vHel = eval(t['Vhel'])
        
        gfilename = directory + 'rot_curves/' + name + '-summary4.json'
        vsys_measured, right_vrot_avg, left_vrot_avg, inc, PA, dist, majDiam = get_data(gfilename)
        
        
        # calculate impact parameter and shit
        impact = calculateImpactParameter(RA_galaxy,Dec_galaxy,RA_target,Dec_target,dist)
    
        # RA component of impact parameter - by setting the Dec to be the same for both
        impact_RA = calculateImpactParameter(RA_galaxy,Dec_galaxy,RA_target,Dec_galaxy,dist)
    
        # Dec component of impact parameter - by setting the RA to be the same for both
        impact_Dec = calculateImpactParameter(RA_galaxy,Dec_galaxy,RA_galaxy,Dec_target,dist)
    
        # calculate azimuth
        az = calculateAzimuth(RA_galaxy,Dec_galaxy,RA_target,Dec_target,dist,PA)
        az2 = calculateAzimuth(RA_galaxy,Dec_galaxy,RA_target,Dec_target,dist,PA+10.)
    
        # calculate R_vir
        Rvir = calculateVirialRadius(majDiam)
        
        print 'Name: ',name
        print 'impact_RA: ',impact_RA
        print 'impact_Dec: ',impact_Dec
        print 'RA_galaxy vs RA_target: ',RA_galaxy,', ',RA_target
        print 'Dec_galaxy vs Dec_target: ',Dec_galaxy,', ',Dec_target

        if RA_galaxy > RA_target:
            # target is on the 'left' side
            if impact_RA >0:
                impact_RA *= -1
            
        if Dec_galaxy > Dec_target:
            # target is 'below' galaxy
            if impact_Dec >0:
                impact_Dec *= -1
                
        # scale to virial radius
        impact_rvir = impact/Rvir
        impact_RA_vir = impact_RA/Rvir
        impact_Dec_vir = impact_Dec/Rvir                
                
        # compare to the absorber velocity:
        # negative means the Lya is higher velocity (red)
        dv = vsys_measured - lyaV
                
        if az2 < az:
            # if az decreases when increasing PA, then the target is on the "left" side of
            # the galaxy
            
            rot_vel = left_vrot_avg
        else:
            rot_vel = right_vrot_avg
        
            
        # now compare to the rotation velocity
        markerColor = 'black'
        
        if (dv > 0 and rot_vel > 0) or (dv < 0 and rot_vel < 0):
            markerColor = 'green'
            
        elif (dv < 0 and rot_vel > 0) or (dv > 0 and rot_vel < 0):
            markerColor = 'red'
            
        else:
            if abs(dv - rot_vel) <= 50:
                markerColor = 'blue'

#         name = name.replace('-','\-')
#         name = name.replace('_','\_')
#         target = name.replace('-','\-')
#         target = name.replace('_','\_')
#         target = name.replace('+','\+')

        matplotlib.rcParams['text.usetex'] = True
        matplotlib.rcParams['text.latex.unicode'] = False

#         combinedName = '${\rm '+name + '-' + target+'}$'.format(name,target)
        combinedName = r'$\rm {0} -  {1}$'.format(name,target)

#         if bfind(combinedName,'_') and not bfind(combinedName,'\_'):
#             combinedName = combinedName.replace('_','\_')
            
            
        # populate the lists
        nameList.append(name)
        targetList.append(target)
        vList.append(lyaV)
        wList.append(lyaW)
        RA_targetList.append(impact_RA_vir)
        Dec_targetList.append(impact_Dec_vir)
        incList.append(inc)
        paList.append(PA)
        azList.append(az)
        RvirList.append(Rvir)
        markerColorList.append(markerColor)
        combinedNameList.append(combinedName)

        print 'added'
        print 'impact_RA_vir: ',impact_RA_vir
        print 'impact_Dec_vir: ',impact_Dec_vir
        print
        
##########################################################################################
    # impact = impact parameter
    # az = azimuth
    # inc = inclination (adjustedInc)

#     CGCG039-137
#     target = 'RX_J1121.2+0326'
#     RA_target = agn[target]['RAdeg']
#     Dec_target = agn[target]['DEdeg']
#     
#     RA_galaxy = 170.36231
#     Dec_galaxy = 3.44491
#     dist = 101.21
#     majDiam = 26.35
#     
#     impact = 98.9
#     R_vir = 166.09
#     az = 71.
#     inc = 63.
#     PA = 157.
#     
#     ESO343-G014
#     target = 'RBS1768'
#     RA_target = 324.7079167
#     Dec_target = -38.47777778
#     
#     RA_galaxy = 324.43825
#     Dec_galaxy = -38.49256
#     dist = 126.07
#     majDiam = 45.23
#     
#     impact = 465.6
#     az = 74.
#     inc = 89.9
#     PA = 158.
#     
#     IC5325
#     target = 'RBS2000'
#     RA_target = 351.18625
#     Dec_target = -40.68027778
#     
#     RA_galaxy = 352.18096
#     Dec_galaxy = -41.33347
#     dist = 18.1
#     majDiam = 20.45
#     
#     impact = 314.335827
#     az = 64.1
#     inc = 25.
#     PA = 15.
#     
#     MCG-03-58-009
#     target = 'MRC2251-178'
#     RA_target = 343.5245833
#     Dec_target = -17.58194444
#     
#     RA_galaxy = 343.42021
#     Dec_galaxy = -17.47889
#     dist = 142.
#     majDiam = 75.31
#     
#     impact = 355.0699641
#     az = 71.
#     inc = 49.
#     PA = 27.
#     
#     NGC1566
#     target = '1H0419-577'
#     RA_target = 66.50291667
#     Dec_target = -57.20055556
#     
#     RA_galaxy = 65.00175
#     Dec_galaxy = -54.93781
#     dist = 7.19
#     majDiam = 15.34
#     
#     impact = 302.77587
#     az = 9.8
#     inc = 48.
#     PA = 170.
# 
#     NGC1566
#     target = 'HE0429-5343'
#     RA_target = 67.66666667
#     Dec_target = -53.61555556
#     
#     RA_galaxy = 65.00175
#     Dec_galaxy = -54.93781
#     dist = 7.19
#     majDiam = 15.34
#     
#     impact = 256.2063291
#     az = 60.1
#     inc = 48.
#     PA = 170.
# 
#     NGC1566
#     target = 'RBS567'
#     RA_target = 69.91125
#     Dec_target = -53.19194444
#     
#     RA_galaxy = 65.00175
#     Dec_galaxy = -54.93781
#     dist = 7.19
#     majDiam = 15.34
#     
#     impact = 422.6192722
#     az = 69.3
#     inc = 48.
#     PA = 170.
    

##########################################################################################
    # Define the galaxy plane



    
##########################################################################################
##########################################################################################
    # now loop through layers of galaxy planes

    
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

    # initial figure
    fig = plt.figure(figsize=(8,8))

    ax = fig.add_subplot(1,1,1)
#     fig.suptitle(r'$\rm {0} - {1}:~ {2} x {3}R_{{vir}}$'.format(galaxyName,agnName,zcutoffm,rcutoffm), fontsize=16)


    # plot circles
    
    def xy(r,phi):
      return r*np.cos(phi), r*np.sin(phi)

    phis=np.arange(0,2*np.pi,0.01)
    
    r = 1.0
    ax.plot(*xy(r,phis), c='black',ls='-' )
    
    r = 2.0
    ax.plot(*xy(r,phis), c='black',ls='-' )
    
    r = 3.0
    ax.plot(*xy(r,phis), c='black',ls='-' )
    
    print 'full RA_targetList: ',RA_targetList
    print
    print
    print 'full Dec_targetList: ',Dec_targetList
    print
    
    ax.scatter(0,0,c='black',marker='*',s=25)
    
    # plot the rest
    largestEW = max(wList)
    smallestEW = min(wList)
    maxSize = 500
    minSize = 30
    
    newSizeList = []
    for w in wList:
        newSize = ((float(w) - smallestEW)/(largestEW - smallestEW)) * (maxSize - minSize) + minSize
        newSizeList.append(newSize)

    ax.scatter(RA_targetList,Dec_targetList, color=markerColorList,s=newSizeList)
    
    xTagOffset = 0.1
    yTagOffset = 0.1
    
    # put some labels on it
    print 'combinedNameList: ',combinedNameList
#     annotate(combinedNameList,xy=(RA_targetList, Dec_targetList),xytext=(xTagOffset,yTagOffset),textcoords='offset points',size=10)

    for i in arange(len(combinedNameList)):
        annotate(combinedNameList[i],xy=(RA_targetList[i], Dec_targetList[i]),\
        xytext=(xTagOffset,yTagOffset),textcoords='offset points',size=8)


    ylabel(r'$\rm R.A. ~[kpc]$')
    xlabel(r'$\rm Dec. ~[kpc]$')
    
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-3.0, 3.0)

    # x-axis
#     majorLocator   = MultipleLocator(0.5)
#     majorFormatter = FormatStrFormatter(r'$\rm %0.1f$')
#     minorLocator   = MultipleLocator(0.25)
#     ax.yaxis.set_major_locator(majorLocator)
#     ax.yaxis.set_major_formatter(majorFormatter)
#     ax.yaxis.set_minor_locator(minorLocator)

    # y axis
#     majorLocator   = MultipleLocator(0.5)
#     majorFormatter = FormatStrFormatter(r'$\rm %0.1f$')
#     minorLocator   = MultipleLocator(0.25)
#     ax.yaxis.set_major_locator(majorLocator)
#     ax.yaxis.set_major_formatter(majorFormatter)
#     ax.yaxis.set_minor_locator(minorLocator)

        
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
    
    show()
    
    directory = '/Users/frenchd/Research/test/'
#     savefig("{0}SALT_map1.pdf".format(directory),dpi=400,bbox_inches='tight')
    savefig("{0}SALT_map1.pdf".format(directory),bbox_inches='tight')


    
if __name__ == '__main__':
    main()
    