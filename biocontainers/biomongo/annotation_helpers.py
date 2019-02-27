

LICENSE_MAP = {}
LICENSE_MAP["SPDX:Apache-2.0"] = [".*Apache.*"]
LICENSE_MAP["BSD-1-Clause"] = [".*BSDlike.*"]
LICENSE_MAP["BSD-3-Clause"] = [".*BSD-3-clause.*"]

# TOOL_LICENSE["0BSD"]="BSD Zero Clause License"
# TOOL_LICENSE["AAL"]="Attribution Assurance License"
# TOOL_LICENSE["Abstyles"]="Abstyles License"
# TOOL_LICENSE["Adobe-2006"]="Adobe Systems Incorporated Source Code License Agreement"
# TOOL_LICENSE["Adobe-Glyph"]="Adobe Glyph List License"
# TOOL_LICENSE["ADSL"]="Amazon Digital Services License"
# TOOL_LICENSE["AFL-1.1"]="Academic Free License v1.1"
# TOOL_LICENSE["AFL-1.2"]="Academic Free License v1.2"
#
# TOOL_LICENSE["AFL-2.0"]="Academic Free License v2.0"
# TOOL_LICENSE["AFL-2.1"]="Academic Free License v2.1"
# TOOL_LICENSE["AFL-3.0"]="Academic Free License v3.0"
# Afmparse License    Afmparse
# Affero General Public License v1.0 only AGPL-1.0-only
# Affero General Public License v1.0 or later AGPL-1.0-or-later
# GNU Affero General Public License v3.0 only AGPL-3.0-only
# GNU Affero General Public License v3.0 or later AGPL-3.0-or-later
# Aladdin Free Public License Aladdin
# AMD's plpa_map.c License    AMDPLPA
# Apple MIT License   AML
# Academy of Motion Picture Arts and Sciences BSD	AMPAS
# ANTLR Software Rights Notice	ANTLR-PD
# Apache License 1.0	Apache-1.0
# Apache License 1.1	Apache-1.1
# Apache License 2.0	Apache-2.0
# Adobe Postscript AFM License	APAFML
# Adaptive Public License 1.0	APL-1.0
# Apple Public Source License 1.0	APSL-1.0
# Apple Public Source License 1.1	APSL-1.1
# Apple Public Source License 1.2	APSL-1.2
# Apple Public Source License 2.0	APSL-2.0
# Artistic License 1.0 w/clause 8	Artistic-1.0-cl8
# Artistic License 1.0 (Perl)	Artistic-1.0-Perl
# Artistic License 1.0	Artistic-1.0
# Artistic License 2.0	Artistic-2.0
# Bahyph License	Bahyph
# Barr License	Barr
# Beerware License	Beerware
# BitTorrent Open Source License v1.0	BitTorrent-1.0
# BitTorrent Open Source License v1.1	BitTorrent-1.1
# Borceux license	Borceux
# BSD 1-Clause License	BSD-1-Clause
# BSD 2-Clause FreeBSD License	BSD-2-Clause-FreeBSD
# BSD 2-Clause NetBSD License	BSD-2-Clause-NetBSD
# BSD-2-Clause Plus Patent License	BSD-2-Clause-Patent
# BSD 2-Clause "Simplified" License	BSD-2-Clause
# BSD with attribution	BSD-3-Clause-Attribution
# BSD 3-Clause Clear License	BSD-3-Clause-Clear
# Lawrence Berkeley National Labs BSD variant license	BSD-3-Clause-LBNL
# BSD 3-Clause No Nuclear License 2014	BSD-3-Clause-No-Nuclear-License-2014
# BSD 3-Clause No Nuclear License	BSD-3-Clause-No-Nuclear-License
# BSD 3-Clause No Nuclear Warranty	BSD-3-Clause-No-Nuclear-Warranty
# BSD 3-Clause "New" or "Revised" License	BSD-3-Clause
# BSD-4-Clause (University of California-Specific)	BSD-4-Clause-UC
# BSD 4-Clause "Original" or "Old" License	BSD-4-Clause
# BSD Protection License	BSD-Protection
# BSD Source Code Attribution	BSD-Source-Code
# Boost Software License 1.0	BSL-1.0
# bzip2 and libbzip2 License v1.0.5	bzip2-1.0.5
# bzip2 and libbzip2 License v1.0.6	bzip2-1.0.6
# Caldera License	Caldera
# Computer Associates Trusted Open Source License 1.1	CATOSL-1.1
# Creative Commons Attribution 1.0 Generic	CC-BY-1.0
# Creative Commons Attribution 2.0 Generic	CC-BY-2.0
# Creative Commons Attribution 2.5 Generic	CC-BY-2.5
# Creative Commons Attribution 3.0 Unported	CC-BY-3.0
# Creative Commons Attribution 4.0 International	CC-BY-4.0	Y
# Creative Commons Attribution Non Commercial 1.0 Generic	CC-BY-NC-1.0
# Creative Commons Attribution Non Commercial 2.0 Generic	CC-BY-NC-2.0
# Creative Commons Attribution Non Commercial 2.5 Generic	CC-BY-NC-2.5
# Creative Commons Attribution Non Commercial 3.0 Unported	CC-BY-NC-3.0
# Creative Commons Attribution Non Commercial 4.0 International	CC-BY-NC-4.0
# Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic	CC-BY-NC-ND-1.0
# Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic	CC-BY-NC-ND-2.0
# Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic	CC-BY-NC-ND-2.5
# Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported	CC-BY-NC-ND-3.0
# Creative Commons Attribution Non Commercial No Derivatives 4.0 International	CC-BY-NC-ND-4.0
# Creative Commons Attribution Non Commercial Share Alike 1.0 Generic	CC-BY-NC-SA-1.0
# Creative Commons Attribution Non Commercial Share Alike 2.0 Generic	CC-BY-NC-SA-2.0
# Creative Commons Attribution Non Commercial Share Alike 2.5 Generic	CC-BY-NC-SA-2.5
# Creative Commons Attribution Non Commercial Share Alike 3.0 Unported	CC-BY-NC-SA-3.0
# Creative Commons Attribution Non Commercial Share Alike 4.0 International	CC-BY-NC-SA-4.0
# Creative Commons Attribution No Derivatives 1.0 Generic	CC-BY-ND-1.0
# Creative Commons Attribution No Derivatives 2.0 Generic	CC-BY-ND-2.0
# Creative Commons Attribution No Derivatives 2.5 Generic	CC-BY-ND-2.5
# Creative Commons Attribution No Derivatives 3.0 Unported	CC-BY-ND-3.0
# Creative Commons Attribution No Derivatives 4.0 International	CC-BY-ND-4.0
# Creative Commons Attribution Share Alike 1.0 Generic	CC-BY-SA-1.0
# Creative Commons Attribution Share Alike 2.0 Generic	CC-BY-SA-2.0
# Creative Commons Attribution Share Alike 2.5 Generic	CC-BY-SA-2.5
# Creative Commons Attribution Share Alike 3.0 Unported	CC-BY-SA-3.0
# Creative Commons Attribution Share Alike 4.0 International	CC-BY-SA-4.0
# Creative Commons Zero v1.0 Universal	CC0-1.0
# Common Development and Distribution License 1.0	CDDL-1.0
# Common Development and Distribution License 1.1	CDDL-1.1
# Community Data License Agreement Permissive 1.0	CDLA-Permissive-1.0
# Community Data License Agreement Sharing 1.0	CDLA-Sharing-1.0
# CeCILL Free Software License Agreement v1.0	CECILL-1.0
# CeCILL Free Software License Agreement v1.1	CECILL-1.1
# CeCILL Free Software License Agreement v2.0	CECILL-2.0
# CeCILL Free Software License Agreement v2.1	CECILL-2.1
# CeCILL-B Free Software License Agreement	CECILL-B
# CeCILL-C Free Software License Agreement	CECILL-C
# Clarified Artistic License	ClArtistic
# CNRI Jython License	CNRI-Jython
# CNRI Python Open Source GPL Compatible License Agreement	CNRI-Python-GPL-Compatible
# CNRI Python License	CNRI-Python
# Condor Public License v1.1	Condor-1.1
# copyleft-next 0.3.0	copyleft-next-0.3.0
# copyleft-next 0.3.1	copyleft-next-0.3.1
# Common Public Attribution License 1.0	CPAL-1.0
# Common Public License 1.0	CPL-1.0
# Code Project Open License 1.02	CPOL-1.02
# Crossword License	Crossword
# CrystalStacker License	CrystalStacker
# CUA Office Public License v1.0	CUA-OPL-1.0
# Cube License	Cube
# curl License	curl
# Deutsche Freie Software Lizenz	D-FSL-1.0
# diffmark license	diffmark
# DOC License	DOC
# Dotseqn License	Dotseqn
# DSDP License	DSDP
# dvipdfm License	dvipdfm
# Educational Community License v1.0	ECL-1.0
# Educational Community License v2.0	ECL-2.0
# Eiffel Forum License v1.0	EFL-1.0
# Eiffel Forum License v2.0	EFL-2.0
# eGenix.com Public License 1.1.0	eGenix
# Entessa Public License v1.0	Entessa
# Eclipse Public License 1.0	EPL-1.0
# Eclipse Public License 2.0	EPL-2.0
# Erlang Public License v1.1	ErlPL-1.1
# EU DataGrid Software License	EUDatagrid
# European Union Public License 1.0	EUPL-1.0
# European Union Public License 1.1	EUPL-1.1
# European Union Public License 1.2	EUPL-1.2
# Eurosym License	Eurosym
# Fair License	Fair
# Frameworx Open License 1.0	Frameworx-1.0
# FreeImage Public License v1.0	FreeImage
# FSF All Permissive License	FSFAP
# FSF Unlimited License	FSFUL
# FSF Unlimited License (with License Retention)	FSFULLR
# Freetype Project License	FTL
# GNU Free Documentation License v1.1 only	GFDL-1.1-only
# GNU Free Documentation License v1.1 or later	GFDL-1.1-or-later
# GNU Free Documentation License v1.2 only	GFDL-1.2-only
# GNU Free Documentation License v1.2 or later	GFDL-1.2-or-later
# GNU Free Documentation License v1.3 only	GFDL-1.3-only
# GNU Free Documentation License v1.3 or later	GFDL-1.3-or-later
# Giftware License	Giftware
# GL2PS License	GL2PS
# 3dfx Glide License	Glide
# Glulxe License	Glulxe
# gnuplot License	gnuplot
# GNU General Public License v1.0 only	GPL-1.0-only
# GNU General Public License v1.0 or later	GPL-1.0-or-later
# GNU General Public License v2.0 only	GPL-2.0-only
# GNU General Public License v2.0 or later	GPL-2.0-or-later
# GNU General Public License v3.0 only	GPL-3.0-only
# GNU General Public License v3.0 or later	GPL-3.0-or-later
# gSOAP Public License v1.3b	gSOAP-1.3b
# Haskell Language Report License	HaskellReport
# Historical Permission Notice and Disclaimer	HPND
# IBM PowerPC Initialization and Boot Software	IBM-pibs
# ICU License	ICU
# Independent JPEG Group License	IJG
# ImageMagick License	ImageMagick
# iMatix Standard Function Library Agreement	iMatix
# Imlib2 License	Imlib2
# Info-ZIP License	Info-ZIP
# Intel ACPI Software License Agreement	Intel-ACPI
# Intel Open Source License	Intel
# Interbase Public License v1.0	Interbase-1.0
# IPA Font License	IPA
# IBM Public License v1.0	IPL-1.0
# ISC License	ISC
# JasPer License	JasPer-2.0
# JSON License	JSON
# Licence Art Libre 1.2	LAL-1.2
# Licence Art Libre 1.3	LAL-1.3
# Latex2e License	Latex2e
# Leptonica License	Leptonica
# GNU Library General Public License v2 only	LGPL-2.0-only
# GNU Library General Public License v2 or later	LGPL-2.0-or-later
# GNU Lesser General Public License v2.1 only	LGPL-2.1-only
# GNU Lesser General Public License v2.1 or later	LGPL-2.1-or-later
# GNU Lesser General Public License v3.0 only	LGPL-3.0-only
# GNU Lesser General Public License v3.0 or later	LGPL-3.0-or-later
# Lesser General Public License For Linguistic Resources	LGPLLR
# libpng License	Libpng
# libtiff License	libtiff
# Licence Libre du Québec – Permissive version 1.1	LiLiQ-P-1.1
# Licence Libre du Québec – Réciprocité version 1.1	LiLiQ-R-1.1
# Licence Libre du Québec – Réciprocité forte version 1.1	LiLiQ-Rplus-1.1
# Linux Kernel Variant of OpenIB.org license	Linux-OpenIB
# Lucent Public License Version 1.0	LPL-1.0
# Lucent Public License v1.02	LPL-1.02
# LaTeX Project Public License v1.0	LPPL-1.0
# LaTeX Project Public License v1.1	LPPL-1.1
# LaTeX Project Public License v1.2	LPPL-1.2
# LaTeX Project Public License v1.3a	LPPL-1.3a
# LaTeX Project Public License v1.3c	LPPL-1.3c
# MakeIndex License	MakeIndex
# MirOS License	MirOS
# MIT No Attribution	MIT-0
# Enlightenment License (e16)	MIT-advertising
# CMU License	MIT-CMU
# enna License	MIT-enna
# feh License	MIT-feh
# MIT License	MIT
# MIT +no-false-attribs license	MITNFA
# Motosoto License	Motosoto
# mpich2 License	mpich2
# Mozilla Public License 1.0	MPL-1.0
# Mozilla Public License 1.1	MPL-1.1
# Mozilla Public License 2.0 (no copyleft exception)	MPL-2.0-no-copyleft-exception
# Mozilla Public License 2.0	MPL-2.0
# Microsoft Public License	MS-PL
# Microsoft Reciprocal License	MS-RL
# Matrix Template Library License	MTLL
# Mup License	Mup
# NASA Open Source Agreement 1.3	NASA-1.3
# Naumen Public License	Naumen
# Net Boolean Public License v1	NBPL-1.0
# University of Illinois/NCSA Open Source License	NCSA
# Net-SNMP License	Net-SNMP
# NetCDF license	NetCDF
# Newsletr License	Newsletr
# Nethack General Public License	NGPL
# Norwegian Licence for Open Government Data	NLOD-1.0
# No Limit Public License	NLPL
# Nokia Open Source License	Nokia
# Netizen Open Source License	NOSL
# Noweb License	Noweb
# Netscape Public License v1.0	NPL-1.0
# Netscape Public License v1.1	NPL-1.1
# Non-Profit Open Software License 3.0	NPOSL-3.0
# NRL License	NRL
# NTP License	NTP
# Open CASCADE Technology Public License	OCCT-PL
# OCLC Research Public License 2.0	OCLC-2.0
# ODC Open Database License v1.0	ODbL-1.0
# Open Data Commons Attribution License v1.0	ODC-By-1.0
# SIL Open Font License 1.0	OFL-1.0
# SIL Open Font License 1.1	OFL-1.1
# Open Government Licence v1.0	OGL-UK-1.0
# Open Government Licence v2.0	OGL-UK-2.0
# Open Government Licence v3.0	OGL-UK-3.0
# Open Group Test Suite License	OGTSL
# Open LDAP Public License v1.1	OLDAP-1.1
# Open LDAP Public License v1.2	OLDAP-1.2
# Open LDAP Public License v1.3	OLDAP-1.3
# Open LDAP Public License v1.4	OLDAP-1.4
# Open LDAP Public License v2.0.1	OLDAP-2.0.1
# Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)	OLDAP-2.0
# Open LDAP Public License v2.1	OLDAP-2.1
# Open LDAP Public License v2.2.1	OLDAP-2.2.1
# Open LDAP Public License 2.2.2	OLDAP-2.2.2
# Open LDAP Public License v2.2	OLDAP-2.2
# Open LDAP Public License v2.3	OLDAP-2.3
# Open LDAP Public License v2.4	OLDAP-2.4
# Open LDAP Public License v2.5	OLDAP-2.5
# Open LDAP Public License v2.6	OLDAP-2.6
# Open LDAP Public License v2.7	OLDAP-2.7
# Open LDAP Public License v2.8	OLDAP-2.8
# Open Market License	OML
# OpenSSL License	OpenSSL
# Open Public License v1.0	OPL-1.0
# OSET Public License version 2.1	OSET-PL-2.1
# Open Software License 1.0	OSL-1.0
# Open Software License 1.1	OSL-1.1
# Open Software License 2.0	OSL-2.0
# Open Software License 2.1	OSL-2.1
# Open Software License 3.0	OSL-3.0
# ODC Public Domain Dedication & License 1.0	PDDL-1.0
# PHP License v3.0	PHP-3.0
# PHP License v3.01	PHP-3.01
# Plexus Classworlds License	Plexus
# PostgreSQL License	PostgreSQL
# psfrag License	psfrag
# psutils License	psutils
# Python License 2.0	Python-2.0
# Qhull License	Qhull
# Q Public License 1.0	QPL-1.0
# Rdisc License	Rdisc
# Red Hat eCos Public License v1.1	RHeCos-1.1
# Reciprocal Public License 1.1	RPL-1.1
# Reciprocal Public License 1.5	RPL-1.5
# RealNetworks Public Source License v1.0	RPSL-1.0
# RSA Message-Digest License	RSA-MD
# Ricoh Source Code Public License	RSCPL
# Ruby License	Ruby
# Sax Public Domain Notice	SAX-PD
# Saxpath License	Saxpath
# SCEA Shared Source License	SCEA
# Sendmail License 8.23	Sendmail-8.23
# Sendmail License	Sendmail
# SGI Free Software License B v1.0	SGI-B-1.0
# SGI Free Software License B v1.1	SGI-B-1.1
# SGI Free Software License B v2.0	SGI-B-2.0
# Simple Public License 2.0	SimPL-2.0
# Sun Industry Standards Source License v1.2	SISSL-1.2
# Sun Industry Standards Source License v1.1	SISSL
# Sleepycat License	Sleepycat
# Standard ML of New Jersey License	SMLNJ
# Secure Messaging Protocol Public License	SMPPL
# SNIA Public License 1.1	SNIA
# Spencer License 86	Spencer-86
# Spencer License 94	Spencer-94
# Spencer License 99	Spencer-99
# Sun Public License v1.0	SPL-1.0
# SugarCRM Public License v1.1.3	SugarCRM-1.1.3
# Scheme Widget Library (SWL) Software License Agreement	SWL
# TCL/TK License	TCL
# TCP Wrappers License	TCP-wrappers
# TMate Open Source License	TMate
# TORQUE v2.5+ Software License v1.1	TORQUE-1.1
# Trusster Open Source License	TOSL
# Technische Universitaet Berlin License 1.0	TU-Berlin-1.0
# Technische Universitaet Berlin License 2.0	TU-Berlin-2.0
# Unicode License Agreement - Data Files and Software (2015)	Unicode-DFS-2015
# Unicode License Agreement - Data Files and Software (2016)	Unicode-DFS-2016
# Unicode Terms of Use	Unicode-TOU
# The Unlicense	Unlicense
# Universal Permissive License v1.0	UPL-1.0
# Vim License	Vim
# VOSTROM Public License for Open Source	VOSTROM
# Vovida Software License v1.0	VSL-1.0
# W3C Software Notice and License (1998-07-20)	W3C-19980720
# W3C Software Notice and Document License (2015-05-13)	W3C-20150513
# W3C Software Notice and License (2002-12-31)	W3C
# Sybase Open Watcom Public License 1.0	Watcom-1.0
# Wsuipa License	Wsuipa
# Do What The F*ck You Want To Public License	WTFPL
# X11 License	X11
# Xerox License	Xerox
# XFree86 License 1.1	XFree86-1.1
# xinetd License	xinetd
# X.Net License	Xnet
# XPP License	xpp
# XSkat License	XSkat
# Yahoo! Public License v1.0	YPL-1.0
# Yahoo! Public License v1.1	YPL-1.1
# Zed License	Zed
# Zend License v2.0	Zend-2.0
# Zimbra Public License v1.3	Zimbra-1.3
# Zimbra Public License v1.4	Zimbra-1.4
# zlib/libpng License with Acknowledgement	zlib-acknowledgement
# zlib License	Zlib
# Zope Public License 1.1	ZPL-1.1
# Zope Public License 2.0	ZPL-2.0
# TOOL_LICENSE["ZPL-2.1"]="Zope Public License 2.1"