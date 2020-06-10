from rydanalysis import AbsorptionImaging, OldStructure, ExpSequence, ReferenceAnalysis, RectangularMask, EllipticalMask
from rydanalysis import AbsorptionImaging, OldStructure, ExpSequence, Gaussian2D, fit_dataarray
from rydanalysis import EllipticalMask, PolygonMask
from pathlib import Path
from lmfit import Parameter
import matplotlib.pyplot as plt
import numpy as np
from prefect import task
import numpy as np

# @task
# def calc_transmission(data, mask_center_x, mask_center_y, mask_width_x, mask_width_y, crop_mask_width_x, crop_mask_width_y ):
#     crop_mask = RectangularMask(image=data.image_01).mask(mask_center_x=mask_center_x, mask_center_y=mask_center_y,
#                                                           crop_mask_width_x=mask_width_x, crop_mask_width_y=mask_width_y)
#     roi_mask = EllipticalMask(image=data.image_01).mask(center_x=mask_center_x, center_y=mask_center_x,
#                                                         width_x=mask_width_x, width_y=mask_width_x)
#     ai = AbsorptionImaging.from_raw_data(data, crop_mask=crop_mask.data, mask=roi_mask.data)
#     return ai.transmission

@task
def calc_transmission(data, mask_kwargs, vertices):
    crop_mask = data.image_01.polygon_mask.get_mask(coord_vertices=vertices)
    roi_mask = data.image_01.elliptical_mask.get_mask(**mask_kwargs)
    ai = AbsorptionImaging.from_raw_data(data, crop_mask=crop_mask.data, mask=roi_mask.data)
    return ai.transmission

@task
def average_od_from_transmission(trans, average_coord):
    trans_averaged = trans.groupby(average_coord).mean('shot')
    od = -np.log(trans_averaged)
    return od

@task
def fit_EIT_dip(od, var):
    average_coord = var
    model_twolvl = Gaussian2D(prefix='twolvl_')
    params_twolvl = model_twolvl.make_params()
    params_twolvl['twolvl_amp'] = Parameter(value=0.8)
    params_twolvl['twolvl_cen_x'] = Parameter(value=0, min=-50, max=50)
    params_twolvl['twolvl_cen_y'] = Parameter(value=-200, min=-300, max=-100)
    params_twolvl['twolvl_sig_x'] = Parameter(value=100, min=100, max=400)
    params_twolvl['twolvl_sig_y'] = Parameter(value=100, min=40, max=700)
    params_twolvl['twolvl_offset'] = Parameter(value=0, vary=False)

    # %%

    model_dip = Gaussian2D(prefix='eit_')
    params_dip = model_dip.make_params()
    params_dip['eit_amp'] = Parameter(value=-0.8)
    params_dip['eit_cen_x'] = Parameter(value=0, min=-50, max=50)
    params_dip['eit_cen_y'] = Parameter(value=-200, min=-250, max=-100)
    params_dip['eit_sig_x'] = Parameter(value=80, min=10, max=100)
    params_dip['eit_sig_y'] = Parameter(value=80, min=10, max=100)

    # %%

    model = model_twolvl + model_dip
    params = params_twolvl + params_dip

    # %%

    def calc_eit_ratio(params, model_twolvl, model_eit):
        params = params.to_parameters()
        x = [params['eit_cen_x'].value]
        y = [params['eit_cen_y'].value]
        # evaluate two level model at center of eit dip
        od_twolvl = model_twolvl.eval(params, x=x, y=y)
        # evaluate full model at center of eit dip
        od_eit = model.eval(params, x=x, y=y)
        ratio = od_eit / od_twolvl
        return ratio.squeeze(('x', 'y'))


    res = od.groupby(average_coord).apply(fit_dataarray, args=(model, params))

    # %%

    eit_ratio = res.groupby(average_coord).apply(calc_eit_ratio, args=(model_twolvl, model))
    eit_ratio.name = 'EIT-ratio'
