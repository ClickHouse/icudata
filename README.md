Pregenerated data for ICU library.

Motivation: ICU is using complicated two-stage build process
that is hard to integrate to the build system of another project.

## What is in the data

The data is filtered with [`filter.json`](filter.json): it contains only what ClickHouse can read.

ClickHouse uses ICU for collation (`COLLATE`, `system.collations`), charset conversion (`convertCharset`),
normalization, case mapping, word segmentation (the `icu` tokenizer) and character properties (`system.unicode`).
It links none of the ICU code for formatting dates, numbers, units and currencies, for time zone names,
transliteration, spelled-out numbers or display names of regions, so the data for these is left out.
For display names of languages, only English is kept (the `language` column of `system.collations`).

| | full | filtered |
|---|---|---|
| items | 4305 | 694 |
| size | 31.6 MiB | 13.6 MiB |

Kept as is: converters (4.9 MiB), break iteration rules and dictionaries (3.6 MiB), collation (3.2 MiB),
normalization, character properties and names, string preparation profiles.

If ClickHouse starts using another part of ICU, remove the corresponding line from `filter.json` and regenerate the data.
The categories are described in the [ICU Data Build Tool](https://unicode-org.github.io/icu/userguide/icu_data/buildtool.html).

## How to regenerate

All three files are generated on a little-endian Linux machine; a big-endian machine is not needed.

1. Download ICU source code: https://github.com/unicode-org/icu and check out the version to build.
2. Build it with the filter, out of the source tree:
   ```
   mkdir build && cd build
   ICU_DATA_FILTER_FILE=/path/to/icudata/filter.json sh ../icu/icu4c/source/runConfigureICU Linux --disable-tests --disable-samples --disable-extras
   make -j
   export LD_LIBRARY_PATH=$PWD/lib:$PWD/stubdata
   ```
   The data package is `data/out/tmp/icudt78l.dat`.
3. Little-endian ELF: the build has already made it, copy `data/out/tmp/icudt78l_dat.S`.
4. Big-endian ELF:
   ```
   mkdir be && bin/icupkg -tb data/out/tmp/icudt78l.dat be/icudt78b.dat
   python3 /path/to/icudata/dat_to_asm.py be/icudt78b.dat icudt78b_dat.S big
   ```
   `genccode` writes the package as 32-bit words in the byte order of the machine it runs on,
   so its output is only correct for a target of the same endianness. `dat_to_asm.py` writes
   the same format with the words in the byte order of the target.
5. Mach-O:
   ```
   mkdir darwin && bin/genccode -a gcc-darwin -e icudt78 -f icudt78l_dat -d darwin data/out/tmp/icudt78l.dat
   ```

Steps 3 to 5 were checked against the previous, unfiltered revision of this repository: applied to its data package,
they reproduce its three files byte for byte.

Reference: https://unicode-org.github.io/icu/userguide/icu4c/build.html#how-to-build-and-install-on-unix
