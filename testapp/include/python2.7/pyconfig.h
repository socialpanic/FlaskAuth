#if defined(__linux__)
# if defined(__x86_64__) && defined(__LP64__)
#  include <x86_64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__x86_64__) && defined(__ILP32__)
#  include <x86_64-linux-gnux32/python2.7/pyconfig.h>
# elif defined(__i386__)
#  include <i386-linux-gnu/python2.7/pyconfig.h>
# elif defined(__aarch64__) && defined(__AARCH64EL__)
#  include <aarch64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__alpha__)
#  include <alpha-linux-gnu/python2.7/pyconfig.h>
# elif defined(__ARM_EABI__) && defined(__ARM_PCS_VFP)
#  include <arm-linux-gnueabihf/python2.7/pyconfig.h>
# elif defined(__ARM_EABI__) && !defined(__ARM_PCS_VFP)
#  include <arm-linux-gnueabi/python2.7/pyconfig.h>
# elif defined(__hppa__)
#  include <hppa-linux-gnu/python2.7/pyconfig.h>
# elif defined(__ia64__)
#  include <ia64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__m68k__) && !defined(__mcoldfire__)
#  include <m68k-linux-gnu/python2.7/pyconfig.h>
# elif defined(__mips_hard_float) && defined(_MIPSEL)
#  if defined(_ABIO32)
#   include <mipsel-linux-gnu/python2.7/pyconfig.h>
#  elif defined(_ABIN32)
#   include <mips64el-linux-gnuabin32/python2.7/pyconfig.h>
#  elif defined(_ABI64)
#   include <mips64el-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__mips_hard_float)
#  if defined(_ABIO32)
#   include <mips-linux-gnu/python2.7/pyconfig.h>
#  elif defined(_ABIN32)
#   include <mips64-linux-gnuabin32/python2.7/pyconfig.h>
#  elif defined(_ABI64)
#   include <mips64-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__powerpc__) && defined(__SPE__)
#  include <powerpc-linux-gnuspe/python2.7/pyconfig.h>
# elif defined(__powerpc__)
#  include <powerpc-linux-gnu/python2.7/pyconfig.h>
# elif defined(__powerpc64__)
#  include <powerpc64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__s390x__)
#  include <s390x-linux-gnu/python2.7/pyconfig.h>
# elif defined(__s390__)
#  include <s390-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sh__) && defined(__LITTLE_ENDIAN__)
#  include <sh4-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sparc__)
#  include <sparc-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sparc64__)
#  include <sparc64-linux-gnu/python2.7/pyconfig.h>
# else
#   error unknown multiarch location for pyconfig.h
# endif
#elif defined(__FreeBSD_kernel__)
# if defined(__LP64__)
#  include <x86_64-kfreebsd-gnu/python2.7/pyconfig.h>
# elif defined(__i386__)
#  include <i386-kfreebsd-gnu/python2.7/pyconfig.h>
# else
#   error unknown multiarch location for pyconfig.h
# endif
#elif defined(__gnu_hurd__)
# include <i386-gnu/python2.7/pyconfig.h>
#else
# error unknown multiarch location for pyconfig.h
#endif
