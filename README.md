# ECOSTRESS Collection 3 Data Product Granule Encapsulation Classes

[![CI](https://github.com/ECOSTRESS-Collection-3/ECOv003-granules/actions/workflows/ci.yml/badge.svg)](https://github.com/ECOSTRESS-Collection-3/ECOv003-granules/actions/workflows/ci.yml)

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

## ECOSTRESS Granules Data Layers

This document provides a detailed listing of the data layers available in the ECOSTRESS granules for various products, including L2T STARS, L3T ETAUX, L3T JET, L4T ESI, and L4T WUE.

### L2T STARS NDVI & Albedo Product

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| NDVI | Normalized Difference Vegetation Index | float32 | Index | NaN | N/A | -1 | 1 | N/A | 12.96 mb |
| NDVI-UQ | NDVI Uncertainty | float32 | Index | NaN | N/A | -1 | 1 | N/A | 12.96 mb |
| NDVI-bias | NDVI Bias | float32 | Index | NaN | N/A | N/A | N/A | N/A | 12.96 mb |
| NDVI-bias-UQ | NDVI Bias Uncertainty | float32 | Index | NaN | N/A | N/A | N/A | N/A | 12.96 mb |
| albedo | Albedo | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 12.96 mb |
| albedo-UQ | Albedo Uncertainty | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 12.96 mb |
| albedo-bias | Albedo Bias | float32 | Ratio | NaN | N/A | N/A | N/A | N/A | 12.96 mb |
| albedo-bias-UQ | Albedo Bias Uncertainty | float32 | Ratio | NaN | N/A | N/A | N/A | N/A | 12.96 mb |

### L3T ETAUX Ecosystem Auxiliary Inputs Product

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| Ta | Near-surface air temperature | float32 | $$^\circ\text{C}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| RH | Relative Humidity | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| Rg | Global Radiation | float32 | $$\text{W m}^{-2}$$ | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| Rn | Net Radiation | float32 | $$\text{W m}^{-2}$$ | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| SM | Soil Moisture | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

### L3T JET Evapotranspiration Product

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| PTJPLSMinst | PT-JPL-SM Instantaneous | float32 | $$\text{W m}^{-2}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMdaily | PT-JPL-SM Daily | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLinst | STIC-JPL Instantaneous | float32 | $$\text{W m}^{-2}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLdaily | STIC-JPL Daily | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| BESSJPLdaily | BESS-JPL Daily | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PMJPLdaily | PM-JPL (MOD16) Daily | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| ETdaily | Daily Evapotranspiration | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| ETuncertainty | Daily Evapotranspiration Uncertainty | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMcanopy | PT-JPL-SM Canopy | float32 | proportion | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLcanopy | STIC-JPL Canopy | float32 | proportion | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMsoil | PT-JPL-SM Soil | float32 | proportion | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMinterception | PT-JPL-SM Interception | float32 | proportion | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

### L4T ESI Product

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| ESI | Evaporative Stress Index | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| PET | Potential Evapotranspiration | float32 | $$\text{mm day}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

### L4T WUE Product

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| WUE | Water Use Efficiency | float32 | $$\text{g C kg}^{-1} \text{H}_2\text{O}$$ | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| GPP | Gross Primary Production | float32 | $$\mu\text{mol m}^{-2} \text{s}^{-1}$$ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
