/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because @@INCLUDE@@ has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifndef @@INCLUDE_MACRO@@_MULTILIB_H
#define @@INCLUDE_MACRO@@_MULTILIB_H
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "@@INCLUDE@@-32.h"
#elif __WORDSIZE == 64
#include "@@INCLUDE@@-64.h"
#else
#error "unexpected value for __WORDSIZE macro"
#endif

#endif
