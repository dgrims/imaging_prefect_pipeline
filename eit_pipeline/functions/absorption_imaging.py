def calc_eit_ratio(params, model_twolvl, model_eit):
    params = params.to_parameters()
    x = [params['eit_cen_x'].value]
    y = [params['eit_cen_y'].value]
    # evaluate two level model at center of eit dip
    od_twolvl = model_twolvl.eval(params, x=x, y=y)
    # evaluate full model at center of eit dip
    od_eit = model.eval(params, x=x, y=y)
    ratio = od_eit/od_twolvl
    return ratio.squeeze(('x','y'))