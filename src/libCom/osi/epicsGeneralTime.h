/***************************************************************************
 *   File:		epicsGeneralTime.h
 *   Author:		Sheng Peng
 *   Institution:	Oak Ridge National Laboratory / SNS Project
 *   Date:		07/2004
 *   Version:		1.2
 *
 *   general EPICS timestamp support API
 *   This is the interface to generalTime for all "users", rather than
 *   Time Providers.
 * 
 * Integration into EPICS Base by Peter Denison, Diamond Light Source
 *
 * Copyright (c) 2008 Diamond Light Source Ltd
 * Copyright (c) 2004 Oak Ridge National Laboratory
 * EPICS BASE is distributed subject to a Software License Agreement found
 * in file LICENSE that is included with this distribution.
 ****************************************************************************/
#ifndef _INC_epicsGeneralTime
#define _INC_epicsGeneralTime

#include <epicsTime.h>
#include <epicsTimer.h>

#ifdef __cplusplus
extern "C" {
#endif

void    generalTime_Init(void);     /* this is the init routine you can call explicitly in st.cmd */
int     lastResortEventProviderInstall(void);
int     generalTimeGetCurrentDouble(double * pseconds);  /* for ai record, seconds from 01/01/1990 */
void    generalTimeResetErrorCounts();  /* for bo record */
int     generalTimeGetErrorCounts();    /* for longin record */
void    generalTimeGetBestTcp(char * desc);     /* for stringin record */
void    generalTimeGetBestTep(char * desc);     /* for stringin record */

long    generalTimeReport(int interest);

#ifdef __cplusplus
}
#endif
#endif