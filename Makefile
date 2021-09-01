# Copyright 2021 The Khronos Group, Inc.
#
# SPDX-License-Identifier: CC-BY-4.0

TARGETS = README.adoc guide.adoc $(wildcard chapters/[A-Za-z]*.adoc) $(wildcard chapters/extensions/[A-Za-z]*.adoc)

all: guide.html

guide.html: $(TARGETS)
	asciidoctor --failure-level WARNING -b html5 guide.adoc

GENERATED = guide.html
clean:
	-rm -f $(GENERATED)
