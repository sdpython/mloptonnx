# pragma once

#include "onnxruntime_c_api.h"
#include "onnxruntime_cxx_api.h"

int _ORT_API_VERSION();
void OrtInitialize();


struct ApiDevice {
    int8_t type;
    int8_t mem_type;
    int16_t device_id;
    ApiDevice();
    ApiDevice(int8_t t, int8_t mt, int16_t devid);
};
