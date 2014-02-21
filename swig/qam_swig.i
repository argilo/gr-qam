/* -*- c++ -*- */

#define QAM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "qam_swig_doc.i"

%{
#include "qam/transport_framing_enc_bb.h"
#include "qam/reed_solomon_enc_bb.h"
#include "qam/interleaver_bb.h"
#include "qam/randomizer_bb.h"
#include "qam/frame_sync_enc_bb.h"
#include "qam/trellis_enc_bb.h"
%}


%include "qam/transport_framing_enc_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, transport_framing_enc_bb);
%include "qam/reed_solomon_enc_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, reed_solomon_enc_bb);
%include "qam/interleaver_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, interleaver_bb);
%include "qam/randomizer_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, randomizer_bb);
%include "qam/frame_sync_enc_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, frame_sync_enc_bb);
%include "qam/trellis_enc_bb.h"
GR_SWIG_BLOCK_MAGIC2(qam, trellis_enc_bb);
