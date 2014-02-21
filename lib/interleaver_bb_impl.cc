/* -*- c++ -*- */
/* 
 * Copyright 2014 Clayton Smith.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "interleaver_bb_impl.h"

#include <stdio.h>

namespace gr {
  namespace qam {

    interleaver_bb::sptr
    interleaver_bb::make(int I, int J)
    {
      return gnuradio::get_initial_sptr
        (new interleaver_bb_impl(I, J));
    }

    /*
     * The private constructor
     */
    interleaver_bb_impl::interleaver_bb_impl(int I, int J)
      : gr::sync_block("interleaver_bb",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
        registers = (unsigned char *) malloc(sizeof(unsigned char) * I * ((I-1) * J));
        if (registers == NULL) {
            fprintf(stderr, "Out of memory.\n");
            exit(1);
        }

        pointers = (int *) malloc(sizeof(int) * I);
        if (pointers == NULL) {
            fprintf(stderr, "Out of memory.\n");
            exit(1);
        }

        memset(registers, 0, sizeof(unsigned char) * I * ((I-1) * J));
        memset(pointers, 0, sizeof(int) * I);

        this->I = I;
        this->J = J;
        commutator = 0;
    }

    /*
     * Our virtual destructor.
     */
    interleaver_bb_impl::~interleaver_bb_impl()
    {
        free(pointers);
        free(registers);
    }

    int
    interleaver_bb_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        unsigned char *out = (unsigned char *) output_items[0];

        int i, p;

        for (i = 0; i < noutput_items; i++) {
            if (commutator == 0) {
                out[i] = in[i];
            } else {
                p = pointers[commutator];

                out[i] = registers[commutator * (I-1) * J + p];
                registers[commutator * (I-1) * J + p] = in[i];

                pointers[commutator] = (p + 1) % (commutator * J);
            }
            commutator = (commutator + 1) % I;
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace qam */
} /* namespace gr */

