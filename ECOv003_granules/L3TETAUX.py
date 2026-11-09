from rasters import Raster

from .tiled_granule import ECOSTRESSTiledGranule

class L3TETAUX(ECOSTRESSTiledGranule):
    _PRIMARY_VARIABLE = "Ta"
    _PRODUCT_NAME = "L3T_ETAUX"

    @property
    def Ta(self) -> Raster:
        return self.variable("Ta")

    @property
    def RH(self) -> Raster:
        return self.variable("RH")

    @property
    def Rg(self) -> Raster:
        return self.variable("Rg")

    @property
    def Rn(self) -> Raster:
        return self.variable("Rn")
    
    @property
    def SM(self) -> Raster:
        return self.variable("SM")

    @property
    def cloud(self) -> Raster:
        return self.variable("cloud")

    @property
    def water(self) -> Raster:
        return self.variable("water")
