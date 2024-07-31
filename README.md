Pregenerated data for ICU library.

You can regenerate the litte-endian data in the following way:
1. Download ICU source code: https://github.com/unicode-org/icu
2. In `icu4c/source` directory run `./configure` and `make`.
3. The resulting file will be located at `./data/out/tmp/icudt75l_dat.S`

The simplest way to regenerate the big-endian data is to (like above) compile icu on a big-endian system and copy the data: 

As most of our computers are not big-endian doing this in a docker container is simplest:
1. Install [docker engine](https://docs.docker.com/engine/install/) and [qemu](https://docs.docker.com/build/building/multi-platform/#qemu-without-docker-desktop)
2. Run `docker run -it --memory="16g" --cpus="8" --platform linux/s390x ubuntu:latest`

In the S390x docker container or VM:
1. Run `apt-get update` and `apt-get install build-essential python3 python-is-python3 git`
3. Download ICU `git clone https://github.com/unicode-org/icu.git`
4. Checkout the version you want to build
5. Change to the correct directory `cd icu/icu4c/source`
6. Make sure all scripts have the right permissions `chmod +x runConfigureICU configure install-sh`
7. Run `./runConfigureICU Linux` and `make` (this can take a while in a docker image...)
8. The resulting file will be located at `./data/out/tmp/icudt75b_dat.S`

Motivation: ICU is using complicated two-stage build process 
that is hard to integrate to the build system of another project.

Reference: https://unicode-org.github.io/icu/userguide/icu4c/build.html#how-to-build-and-install-on-unix
