# Makefile for source rpm: xorg-x11-server
# $Id$
NAME := xorg-x11-server
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
