Pregenerated data for ICU library.

You can regenerate this data in the following way:
1. Download ICU source code: https://github.com/unicode-org/icu
2. In `icu4c/source` directory run `./configure` and `make`.
3. The resulting file will be located at `./data/out/tmp/icudt70l_dat.S`

Motivation: ICU is using complicated two-stage build process 
that is hard to integrate to the build system of another project.
