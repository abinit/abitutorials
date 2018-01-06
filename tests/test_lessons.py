"""Tests for lessons"""
from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import os


pack_dir, x = os.path.split(os.path.abspath(__file__))
pack_dir, x = os.path.split(pack_dir)
sys.path.insert(0, pack_dir)

from abipy.core.testing import AbipyTest


class TestLessons(AbipyTest):
    """Unit tests for lessons."""

    def get_options(self):
        from abipy.flowtk import build_flow_main_parser
        parser = build_flow_main_parser()
        return parser.parse_args("")
        #flow.make_scheduler().start()
        #flow.rmtree()

    def test_lesson_base1(self):
        """Testing base1 lessons."""
        from abitutorials.base1.lesson_base1 import build_flow
        flow = build_flow(self.get_options())
        self.abivalidate_flow(flow)

    def test_lesson_base3(self):
        """Testing base3 lessons."""
        from abitutorials.base3.lesson_base3 import build_ngkpt_flow, build_relax_flow, build_ebands_flow

        flow = build_ngkpt_flow(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_relax_flow(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_ebands_flow(self.get_options())
        self.abivalidate_flow(flow)

    def test_lesson_base4(self):
        """Testing base4 lessons."""
        from abitutorials.base4.lesson_base4 import build_relax_flow, build_relax_tsmear_nkpts_convflow

        flow = build_relax_flow(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_relax_tsmear_nkpts_convflow(self.get_options())
        self.abivalidate_flow(flow)

    def test_lesson_bse(self):
        """Testing bse lessons."""
        from abitutorials.bse.lesson_bse import build_bse_flow, build_bse_metallicW_flow, build_bse_kconv_flow

        flow = build_bse_flow(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_bse_metallicW_flow(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_bse_kconv_flow(self.get_options())
        self.abivalidate_flow(flow)

    def test_lesson_dfpt(self):
        """Testing dfpt lessons."""
        from abitutorials.dfpt.lesson_dfpt import build_flow_alas_ecut_conv, build_flow_alas_phonons
        flow = build_flow_alas_ecut_conv(self.get_options())
        self.abivalidate_flow(flow)

        flow = build_flow_alas_phonons(self.get_options())
        self.abivalidate_flow(flow)

    #def test_lesson_g0w0(self):
    #    """Testing g0w0 lessons."""
    #    from abitutorials.g0w0.lesson_g0w0 import build_g0w0_flow
    #    flow = build_g0w0_flow(self.get_options())

    #def test_lesson_optic(self):
    #    """Testing g0w0 lessons."""
    #    from abitutorials.optic.lesson_optic import build_g0w0_flow
    #    flow = build_g0w0_flow(self.get_options())

    #def test_lesson_paw1(self):
    #    """Testing paw1 lessons."""
    #    from abitutorials.paw1.lesson_paw1 import build_flow
    #    flow = build_flow(self.get_options())
