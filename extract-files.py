# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixup_remove_arch_suffix,
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
namespace_imports = [
    "hardware/qcom-caf/sm8150",
    "hardware/qcom-caf/wlan",
    "hardware/xiaomi",
    "vendor/qcom/opensource/commonsys/display",
    "vendor/qcom/opensource/commonsys-intf/display",
    "vendor/qcom/opensource/dataservices",
    "vendor/qcom/opensource/data-ipa-cfg-mgr-legacy-um",
    "vendor/qcom/opensource/display",
]
def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None
lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libwfdaac_vendor',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib/miwatermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    ('vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so')
        .add_needed('libcrypto_shim.so'),
    ('vendor/lib64/libvendor.goodix.hardware.biometrics.fingerprint@2.1.so', 'vendor/lib64/libgoodixhwfingerprint.so'): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
        
}  # fmt: skip

module = ExtractUtilsModule(
    'ginkgo',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)
if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

_remove_vtcamera('vendor/etc/camera/camera_config.xml', 'vendor/etc/camera/camera_config.xml')