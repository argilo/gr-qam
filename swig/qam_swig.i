/* -*- c++ -*- */

#define QAM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "qam_swig_doc.i"

%{
#include "qam/transport_framing_bb.h"
#include "qam/reed_solomon_bb.h"
#include "qam/interleaver_bb.h"
%}


%include "qam/transport_framing_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, transport_framing_bb);
%include "qam/reed_solomon_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, reed_solomon_bb);
%include "qam/interleaver_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, interleaver_bb);
