/*************************************************************************\
* Copyright (c) 2002 The University of Chicago, as Operator of Argonne
*     National Laboratory.
* Copyright (c) 2002 The Regents of the University of California, as
*     Operator of Los Alamos National Laboratory.
* EPICS BASE Versions 3.13.7
* and higher are distributed subject to a Software License Agreement found
* in file LICENSE that is included with this distribution. 
\*************************************************************************/
/*
 *      $Id$
 *
 *      Author  Jeffrey O. Hill
 *              johill@lanl.gov
 *              505 665 1831
 */

#include <stdexcept>

#define epicsExportSharedSymbols
#include "casMonEvent.h"
#include "casMonitor.h"
#include "casCoreClient.h"

caStatus casMonEvent::cbFunc ( 
    casCoreClient & client, epicsGuard < epicsMutex > & guard )
{
    return this->monitor.executeEvent ( 
        client, * this, this->pValue, guard );
}

void casMonEvent::assign ( const gdd & valueIn )
{
	this->pValue = & valueIn;
}

void casMonEvent::swapValues ( casMonEvent & in )
{
    assert ( & in.monitor == & this->monitor );
    this->pValue.swap ( in.pValue );
}

casMonEvent::~casMonEvent ()
{
}

#ifdef CXX_PLACEMENT_DELETE
void casMonEvent::operator delete ( void * pCadaver, 
    tsFreeList < class casMonEvent, 1024, epicsMutexNOOP > & freeList ) 
{
    freeList.release ( pCadaver, sizeof ( casMonEvent ) );
}
#endif

void * casMonEvent::operator new ( size_t ) // X aCC 361
{
    // The HPUX compiler seems to require this even though no code
    // calls it directly
    throw std::logic_error ( "why is the compiler calling private operator new" );
}

void casMonEvent::operator delete ( void * )
{
    // Visual C++ .net appears to require operator delete if
    // placement operator delete is defined? I smell a ms rat
    // because if I declare placement new and delete, but
    // comment out the placement delete definition there are
    // no undefined symbols.
    errlogPrintf ( "%s:%d this compiler is confused about placement delete - memory was probably leaked",
        __FILE__, __LINE__ );
}



