import os
from conans import ConanFile, tools


class ProtobufConan(ConanFile):
    name = "protobuf"
    version = "2.6.1"
    license = "BSD-3-Clause"
    url = "https://github.com/omicronns/conan-protobuf"
    description = "Protocol Buffers - Google's data interchange format"
    settings = {"os": ["Linux"], "compiler": None,
                "build_type": None, "arch": None}

    def source(self):
        url = "https://github.com/protocolbuffers/protobuf/releases/download/v{}/protobuf-{}.tar.gz"
        tools.get(url.format(self.version, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        self.run("./configure", cwd="sources")
        self.run("make -j{}".format(tools.cpu_count()), cwd="sources")

    def package(self):
        self.copy("*.h", dst="include", src="sources/src")
        self.copy("*.a", dst="lib", src="sources/src/.libs", keep_path=False)
        self.copy("*.so", dst="bin", src="sources/src/.libs", keep_path=False)
        self.copy("lt-protoc", dst="bin/.libs",
                  src="sources/src/.libs", keep_path=False)
        self.copy("protoc", dst="bin/.libs",
                  src="sources/src/.libs", keep_path=False)
        self.copy("protoc", dst="bin", src="sources/src", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ['bin']
