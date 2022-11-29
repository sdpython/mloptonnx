#include "onnxruntime_c_api.h"
#include "onnxruntime_cxx_api.h"
#include <stdexcept>
#include <iostream>
#include "ort_interface.h"
#include "make_string.h"

//#pragma comment(lib, "user32.lib")
//#pragma comment(lib, "gdi32.lib")
//#pragma comment(lib, "onnxruntime.lib")
// export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

// https://github.com/microsoft/onnxruntime/releases/tag/v1.13.1
// https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx/squeezenet

#define OrtEnv Ort::Env

int _ORT_API_VERSION() {
    return ORT_API_VERSION;
}


const OrtApi& GetApi() {
    static const OrtApi* api = OrtGetApiBase()->GetApi(ORT_API_VERSION);
    if (api == nullptr)
        throw std::runtime_error(MakeString("Unable to load OrtApi, ORT_API_VERSION=", ORT_API_VERSION, "."));
    return *api;
}


OrtEnv& GetOrtEnv() {
    static OrtEnv env(ORT_LOGGING_LEVEL_WARNING, "mloptonnx");
    return env;
}


void OrtInitialize() {
    GetApi();
    GetOrtEnv();
}
