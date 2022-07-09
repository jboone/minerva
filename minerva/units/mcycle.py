from amaranth import *

from ..csr import *

__all__ = ["McycleUnit"]

mcycle_layout = [
    ("value", 32, CSRAccess.RW),
]

mcycleh_layout = [
    ("value", 32, CSRAccess.RW),
]

class McycleUnit(Elaboratable, AutoCSR):
    def __init__(self):
        self.mcycle  = CSR(0xb00, mcycle_layout)
        self.mcycleh = CSR(0xb80, mcycleh_layout)

    def elaborate(self, platform) -> Module:
        m = Module()

        mcycle_count = Signal(64)
        m.d.sync += mcycle_count.eq(mcycle_count + 1)

        # for csr in self.iter_csrs():
        #     with m.If(csr.we):
        #         m.d.sync += mcycle_count.eq(Cat(csr.w, Const(0, 32)))

        with m.If(self.mcycle.re):
            m.d.sync += self.mcycle.r.value.eq(mcycle_count[0:32])
        with m.If(self.mcycleh.re):
            m.d.sync += self.mcycleh.r.value.eq(mcycle_count[32:64])

        return m
