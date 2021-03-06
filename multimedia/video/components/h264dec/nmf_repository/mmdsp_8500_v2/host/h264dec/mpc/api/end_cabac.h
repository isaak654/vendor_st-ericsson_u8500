/*
 * Copyright (C) ST-Ericsson SA 2010. All rights reserved.
 * This code is ST-Ericsson proprietary and confidential.
 * Any use of the code for whatever purpose is subject to
 * specific written permission of ST-Ericsson SA.
 */

/*****************************************************************************/
/**
 * This is a Nomadik Multiprocessing Framework generated file, please do not modify it.
 */

/* 'h264dec.mpc.api.end_cabac' interface */
#if !defined(h264dec_mpc_api_end_cabac_IDL)
#define h264dec_mpc_api_end_cabac_IDL

#include <cm/inc/cm_type.h>
#include <host/t1xhv_common.idt.h>
#include <host/t1xhv_vdc_h264.idt.h>


typedef struct sIh264dec_mpc_api_end_cabac {
  void* THIS;
  t_cm_error (*endCabac)(void* THIS, t_t1xhv_status status, t_t1xhv_decoder_info info, t_uint32 durationInTicks);
} Ih264dec_mpc_api_end_cabac;

typedef struct {
  void* THIS;
  void (*endCabac)(void* THIS, t_t1xhv_status status, t_t1xhv_decoder_info info, t_uint32 durationInTicks);
} CBh264dec_mpc_api_end_cabac;

#endif
