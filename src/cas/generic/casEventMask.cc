/*
 *      $Id$
 *
 *      Author  Jeffrey O. Hill
 *              johill@lanl.gov
 *              505 665 1831
 *
 *      Experimental Physics and Industrial Control System (EPICS)
 *
 *      Copyright 1991, the Regents of the University of California,
 *      and the University of Chicago Board of Governors.
 *
 *      This software was produced under  U.S. Government contracts:
 *      (W-7405-ENG-36) at the Los Alamos National Laboratory,
 *      and (W-31-109-ENG-38) at Argonne National Laboratory.
 *
 *      Initial development by:
 *              The Controls and Automation Group (AT-8)
 *              Ground Test Accelerator
 *              Accelerator Technology Division
 *              Los Alamos National Laboratory
 *
 *      Co-developed with
 *              The Controls and Computing Group
 *              Accelerator Systems Division
 *              Advanced Photon Source
 *              Argonne National Laboratory
 *
 *
 * History
 * $Log$
 * Revision 1.4  1996/12/06 22:32:11  jhill
 * force virtual destructor
 *
 * Revision 1.3  1996/11/02 00:54:10  jhill
 * many improvements
 *
 * Revision 1.2  1996/09/04 20:20:44  jhill
 * removed sizeof(casEventMask::mask) for MSVISC++
 *
 * Revision 1.1.1.1  1996/06/20 00:28:16  jhill
 * ca server installation
 *
 *
 */


#include <epicsAssert.h>
#include <stdio.h>
#include <limits.h>

#include <server.h>

#ifdef TEST
main ()
{
	casEventRegistry 	reg;
	casEventMask		bill1 (reg, "bill");
	casEventMask		bill2 (reg, "bill");
	casEventMask		bill3 (reg, "bill");
	casEventMask		art1 (reg, "art");
	casEventMask		art2 (reg, "art");
	casEventMask		jane (reg, "jane");
	casEventMask		artBill;
	casEventMask		tmp;

	bill1.show(10u);
	reg.show(10u);
	bill2.show(10u);
	reg.show(10u);
	bill3.show(10u);
	reg.show(10u);
	jane.show(10u);
	reg.show(10u);
	art1.show(10u);
	reg.show(10u);
	art2.show(10u);
	reg.show(10u);

	assert (bill1 == bill2);
	assert (bill1 == bill3);
	assert (jane != bill1);
	assert (jane != art1);
	assert (bill1 != art1);
	assert (art1 == art2);

	artBill = art1 | bill1;
	tmp = artBill & art1;
	assert (tmp.eventsSelected());
	tmp = artBill & bill1;
	assert (tmp.eventsSelected());
	tmp = artBill&jane;
	assert (tmp.noEventsSelected());
}
#endif

//
// casEventRegistry::init()
//
int casEventRegistry::init()  
{
	if (!this->hasBeenInitialized) {
		int status;
		status = this->resTable <casEventMaskEntry, stringId>::
				init(1u<<8u);
		if (status==0) {
			this->hasBeenInitialized = 1u;        
		}
		return status;
	}
	return 0;
}


//
// casEventRegistry::maskAllocator()
//
inline casEventMask casEventRegistry::maskAllocator()
{
        casEventMask    evMask;
 
	this->mutex.osiLock();
        if (this->allocator<CHAR_BIT*sizeof(evMask.mask)) {
        	evMask.mask = 1u<<(this->allocator++);
        }
	this->mutex.osiUnlock();
        return evMask;
}

//
// casEventRegistry::registerEvent()
//
casEventMask casEventRegistry::registerEvent(const char *pName)
{
	casEventMaskEntry	*pEntry;
	stringId 		id (pName);
	casEventMask		mask;

	if (!this->hasBeenInitialized) {
		errMessage(S_cas_noMemory, 
			"casEventRegistry: not initialized?");
		return mask;
	}

	this->mutex.osiLock();
	pEntry = this->lookup (id);
	if (pEntry) {
		mask = *pEntry;
	}
	else {
		mask = this->maskAllocator();
		if (mask.mask == 0u) {
			errMessage(S_cas_tooManyEvents, NULL);
		}
		else {
			pEntry = new casEventMaskEntry(*this, mask, pName);
			if (pEntry) {
				mask = *pEntry;
			}
			else {
				mask.mask = 0u;
				errMessage(S_cas_noMemory, 
					"mask bit was lost during init");
			}
		}
	}
	this->mutex.osiUnlock();
	return mask;
}

//
// casEventMask::show()
//
void casEventMask::show(unsigned level)
{
	if (level>0u) {
		printf ("casEventMask = %x\n", this->mask);
	}
}

casEventMask::casEventMask (casEventRegistry &reg, const char *pName)
{
        *this = reg.registerEvent (pName);
}

//
// casEventRegistry::show()
//
void casEventRegistry::show(unsigned level)
{
	if (!this->hasBeenInitialized) {
		printf ("casEventRegistry: not initialized\n");
	}
	this->mutex.osiLock();
	if (level>1u) {
		printf ("casEventRegistry: bit allocator = %d\n", 
				this->allocator);
	}
	this->resTable <casEventMaskEntry, stringId>::show(level);
	this->mutex.osiUnlock();
}

//
// casEventMaskEntry::casEventMaskEntry()
//
casEventMaskEntry::casEventMaskEntry(
	casEventRegistry &regIn, casEventMask maskIn, const char *pName) :
	reg(regIn), casEventMask (maskIn), stringId (pName) 
{
	int 	stat;

	stat = this->reg.add(*this);
	assert(stat==0);
}

//
// casEventMaskEntry::~casEventMaskEntry()
//
// empty destructor forces virtual
//
// (not inline so that we avoid duplication resulting 
// in the object code created by some compilers)
//
casEventMaskEntry::~casEventMaskEntry()
{
        this->reg.remove (*this);
}

//
// casEventMaskEntry::show()
//
void casEventMaskEntry::show (unsigned level)
{
	this->casEventMask::show(level);
	this->stringId::show(level);
}

