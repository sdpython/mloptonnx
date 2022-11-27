#include <stdexcept>
#include "ort_interface.h"
#include "ortapi/onnxruntime_cxx_api.h"
#include "make_string.h"

//#pragma comment(lib, "user32.lib")
//#pragma comment(lib, "gdi32.lib")
//#pragma comment(lib, "onnxruntime.lib")
// export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

// https://github.com/microsoft/onnxruntime/releases/tag/v1.13.1
// https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx/squeezenet


const OrtApi& GetApi() {
    const OrtApi& api = Ort::GetApi();
    return api;
}


Ort::Env& GetOrtEnv() {
    static Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "mloptonnx");
    return env;
}

void OrtInitialize() {
    GetApi();
    GetOrtEnv();
}