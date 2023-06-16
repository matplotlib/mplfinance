from mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict
from mplfinance._arg_validators import _mav_validator
import numpy  as np
import pandas as pd
import matplotlib.colors as mcolors
from mplfinance._helpers import _list_of_dict

def _valid_indicator_kwargs():
    valid_indicators = ('sma','ema','ichimoku','bband')

    vikwargs = {
        'kind'        : { 'Default'     : 'sma',
                          'Description' : 'Name of Studies: "sma","ema","ichimoku","bband"',
                          'Validator'   : lambda value: value in valid_indicators },
        
        'period'      : { 'Default'     : None,
                          'Description' : 'Indicator window size(s); (int or tuple of ints)',
                          'Validator'   : _mav_validator },
        
        'color'       : { 'Default'     : None,
                          'Description' : 'color (or sequence of colors) of line(s), scatter marker(s), or bar(s).',
                          'Validator'   : lambda value: mcolors.is_color_like(value) or
                                         (isinstance(value,(list,tuple,np.ndarray)) and all([mcolors.is_color_like(v) for v in value])) },

        'legend_label' : { 'Default'     : None,
                          'Description' : 'Figure Title (see also `axtitle`)',
                          'Validator'   : lambda value: isinstance(value,(str,list)) },
    }

    _validate_vkwargs_dict(vikwargs)

    return vikwargs


def _validate_indicator_para(inlist):
    valid_study = _process_kwargs(inlist, _valid_indicator_kwargs())

    return valid_study
        
def _make_indicator_plot(astudy,colss,axA1,closes,highs,lows,xdates,script_title):
    if astudy.get("kind") == "ema":
        if astudy.get("period") is not None:
            ema_period = astudy['period']
        else:
            ema_period = 7

        if astudy.get("color") is not None:
            colss = astudy['color']

        else:
            colss = colss

        yticks = [*axA1.get_yticks(),]
        yticklabels = [*axA1.get_yticklabels(),]
        colors = {}

        if isinstance(ema_period,tuple):
            for i_id,ilength in enumerate(ema_period):
                iema = pd.Series(closes).ewm(span=ilength,adjust=False).mean()
                iema_values = iema.values
                yticks.append(iema_values[-1].round(2))
                yticklabels.append(float(iema_values[-1].round(2)))
                colors.update({str(iema_values[-1].round(2)):colss[i_id]})
                if 'legend_label' in astudy:
                    label = astudy['legend_label']
                    axA1.plot(xdates,iema_values,color=colss[i_id],label=label[0])
                    axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
                else:
                    axA1.plot(xdates,iema_values,color=colss[i_id])
        else:
            iema = pd.Series(closes).ewm(span=ema_period,adjust=False).mean()
            iema_values = iema.values
            yticks.append(iema_values[-1].round(2))
            yticklabels.append(iema_values[-1].round(2))
            colors.update({str(iema_values[-1].round(2)):colss[0]})
            if 'legend_label' in astudy:
                label = astudy['legend_label']
                axA1.plot(xdates,iema_values,color=colss[0],label=label[0])
                axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
            else:
                axA1.plot(xdates,iema_values,color=colss[0])
        axA1.set_yticks(yticks, labels=yticklabels)
        for xtic in axA1.get_yticklabels():
            if xtic.get_text() in colors.keys():
                xtic.set_color(colors[xtic.get_text()])

    if astudy.get("kind") == "sma":  
        if astudy.get("period") is not None:
            sma_period = astudy['period']
        else:
            sma_period = 7

        if astudy.get("color") is not None:
            colss = astudy['color']

        else:
            colss == colss

        yticks = [*axA1.get_yticks(),]
        yticklabels = [*axA1.get_yticklabels(),]
        colors = {}

        if isinstance(sma_period,tuple):
            for i_id,ilength in enumerate(sma_period):
                isma = pd.Series(closes).rolling(ilength).mean()
                isma_values = isma.values
                yticks.append(isma_values[-1].round(2))
                yticklabels.append(float(isma_values[-1].round(2)))
                colors.update({str(isma_values[-1].round(2)):colss[i_id]})
                if 'legend_label' in astudy:
                    label = astudy['legend_label']
                    axA1.plot(xdates,isma_values,color=colss[i_id],label=label[0])
                    axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
                else:
                    axA1.plot(xdates,isma_values,color=colss[i_id])
        else:
            isma = pd.Series(closes).rolling(sma_period).mean()
            isma_values = isma.values
            yticks.append(isma_values[-1].round(2))
            yticklabels.append(isma_values[-1].round(2))
            colors.update({str(isma_values[-1].round(2)):colss[0]})
            if 'legend_label' in astudy:
                label = astudy['legend_label']
                axA1.plot(xdates,isma_values,color=colss[0],label=label[0])
                axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
            else:
                axA1.plot(xdates,isma_values,color=colss[0])
        axA1.set_yticks(yticks, labels=yticklabels)
        for xtic in axA1.get_yticklabels():
            if xtic.get_text() in colors.keys():
                xtic.set_color(colors[xtic.get_text()])   

    if astudy.get("kind") == "BBand":
        if astudy.get("period") is not None:
            BBand_period = astudy['period']
        else:
            BBand_period = 21

        if astudy.get("color") is not None:
            colss = astudy['color']
        else:
            colss = colss
        rolling_mean = pd.Series(closes).rolling(window=BBand_period).mean()
        rolling_std =  pd.Series(closes).rolling(window=BBand_period).std()
        middle_band = pd.Series(closes).rolling(window=BBand_period).mean()
        upper_band = rolling_mean + (rolling_std * 3)
        lower_band = rolling_mean - (rolling_std * 3)

        
        if 'legend_label' in astudy:
            label = astudy['legend_label']
            axA1.plot(xdates,upper_band.values,color=colss[0],label=label[0])
            axA1.plot(xdates,middle_band.values,color=colss[1],label=label[1])
            axA1.plot(xdates,lower_band.values,color=colss[2],label=label[2])
            axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
        else:
            axA1.plot(xdates,upper_band.values,color=colss[0])
            axA1.plot(xdates,middle_band.values,color=colss[1])
            axA1.plot(xdates,lower_band.values,color=colss[2])
        

        upper = upper_band.values[-1].round(2)
        middle = middle_band.values[-1].round(2)
        lower = lower_band.values[-1].round(2)

        yticks = [*axA1.get_yticks(), upper,middle,lower]
        yticklabels = [*axA1.get_yticklabels(), float(upper),float(middle),float(lower)]
        colors = {str(upper):colss[0],str(middle):colss[1],str(lower):colss[2]}

        axA1.set_yticks(yticks, labels=yticklabels)
        for xtic in axA1.get_yticklabels():
            if xtic.get_text() in colors.keys():
                xtic.set_color(colors[xtic.get_text()])

    if astudy['kind'] == 'ichimoku':
            if astudy.get("period") is not None:
                short_period = astudy['period'][0]
                long_period = astudy['period'][1]
                window_period = astudy['period'][2]
            else:
                short_period = 9
                long_period = 26
                window_period = 52

            if astudy.get("color") is not None:
                colss = astudy['color']

            else:
                colss = colss
            
            yticks = [*axA1.get_yticks(),]
            yticklabels = [*axA1.get_yticklabels(),]
            colors = {}


            Tenkan_sen = (pd.Series(closes).rolling(window=short_period).max() + pd.Series(closes).rolling(window=short_period).min()) / 2
            Kijun_sen = (pd.Series(closes).rolling(window=long_period).max() + pd.Series(closes).rolling(window=long_period).min()) / 2
            Senkou_Span_A = (Tenkan_sen + Kijun_sen) / 2
            Senkou_Span_B = (pd.Series(highs).rolling(window=window_period).max() + pd.Series(lows).rolling(window=window_period).min()) / 2
            Chikou_Span  = pd.Series(closes).shift(periods=-long_period)
            Tenkan_sen_values = Tenkan_sen.values
            yticks.append(Tenkan_sen_values[-1].round(2))
            yticklabels.append(float(Tenkan_sen_values[-1].round(2)))
            colors.update({str(Tenkan_sen_values[-1].round(2)):colss[0]})

            Kijun_sen_values = Kijun_sen.values
            yticks.append(Kijun_sen_values[-1].round(2))
            yticklabels.append(float(Kijun_sen_values[-1].round(2)))
            colors.update({str(Kijun_sen_values[-1].round(2)):colss[1]})

            Senkou_Span_A_values =  Senkou_Span_A.values
            yticks.append(Senkou_Span_A_values[-1].round(2))
            yticklabels.append(float(Senkou_Span_A_values[-1].round(2)))
            colors.update({str(Senkou_Span_A_values[-1].round(2)):colss[2]})

            Senkou_Span_B_values = Senkou_Span_B.values
            yticks.append(Senkou_Span_B_values[-1].round(2))
            yticklabels.append(float(Senkou_Span_B_values[-1].round(2)))
            colors.update({str(Senkou_Span_B_values[-1].round(2)):colss[3]})

            Chikou_Span_values = Chikou_Span.values
            yticks.append(Chikou_Span_values[-(long_period + 1)].round(2))
            yticklabels.append(float(Chikou_Span_values[-(long_period + 1)].round(2)))
            colors.update({str(Chikou_Span_values[-1].round(2)):colss[4]})

            if 'legend_label' in astudy:
                label = astudy['legend_label']
                axA1.plot(xdates,Tenkan_sen_values,color=colss[0],label=label[0])
                axA1.plot(xdates,Kijun_sen_values,color=colss[1],label=label[1])
                axA1.plot(xdates,Senkou_Span_A_values,color=colss[2],label=label[2])
                axA1.plot(xdates,Senkou_Span_B_values,color=colss[3],label=label[3])
                axA1.plot(xdates,Chikou_Span_values,color=colss[4],label=label[4])
                axA1.legend(title=script_title, title_fontsize='large',loc='upper left')
            else:
                axA1.plot(xdates,Tenkan_sen_values,color=colss[0])
                axA1.plot(xdates,Kijun_sen_values,color=colss[1])
                axA1.plot(xdates,Senkou_Span_A_values,color=colss[2])
                axA1.plot(xdates,Senkou_Span_B_values,color=colss[3])
                axA1.plot(xdates,Chikou_Span_values,color=colss[4])
            
            axA1.fill_between(xdates,Senkou_Span_A_values,Senkou_Span_B_values,where = Senkou_Span_A_values>= Senkou_Span_B_values, color='green',alpha=0.1)
            axA1.fill_between(xdates,Senkou_Span_A_values,Senkou_Span_B_values,where = Senkou_Span_A_values<= Senkou_Span_B_values, color='red',alpha=0.1)
            axA1.set_yticks(yticks, labels=yticklabels)
            for xtic in axA1.get_yticklabels():
                if xtic.get_text() in colors.keys():
                    xtic.set_color(colors[xtic.get_text()])  