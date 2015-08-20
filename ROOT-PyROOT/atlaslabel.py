
# @author:  Doug Schouten <doug dot schouten at triumf dot ca>

import ROOT
import globalcfg

# ----------- ============ ----------- ============ ----------- ============ -----------
def atlasLabel( x, y, cv, preliminary = False, internal = True, color = ROOT.kBlack, size = globalcfg.labelFontSizeLarge ):
    if cv == None:
        return None
    cv.cd()
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont( 42 )
    l.SetTextColor( color )
    l.SetTextSize( size )
    txt = '#bf{#it{ATLAS}}'
    if preliminary: txt += ' Preliminary'
    elif internal : txt += ' Internal'
    else          : txt += ' Public'
    l.DrawLatex(x, y, txt)
    return l

# ----------- ============ ----------- ============ ----------- ============ -----------
def atlasLumiLabel( x, y, intl, cv, color = ROOT.kBlack, size = globalcfg.labelFontSize ):
    if cv == None:
        return None
    cv.cd()
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextColor(color)
    l.SetTextSize(size)
    s = '%0.1f'%( intl / 1000.0 )
    l.DrawLatex(x,y,'#scale[0.6]{#int_{  }}L_{ }dt = ' + s + ' fb^{-1}')
    return l

# ----------- ============ ----------- ============ ----------- ============ -----------
def atlasCMLabel( x, y, cv, color = ROOT.kBlack, size = globalcfg.labelFontSize ):
    if cv == None:
        return None
    cv.cd()
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextColor(color)
    l.SetTextSize(size)
    l.DrawLatex(x,y,'#sqrt{s} = 8 TeV')
    return l

# ----------- ============ ----------- ============ ----------- ============ -----------
def atlasAllLabels( x, y, intl, cv, color = ROOT.kBlack, size = globalcfg.labelFontSize,
                    preliminary = False, internal = True, subtxt=None):
    if cv == None:
        return None
    cv.cd()
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextColor(color)
    l.SetTextSize(size)
    s = '%0.1f'%( intl / 1000. )
    atlasLabel( x, y, cv, preliminary = preliminary, internal = internal, size = size / 0.75 )
    txt = '#sqrt{#font[12]{s}} = 8 TeV'
    if intl > 0:
        txt = ','.join( ( txt, ' #scale[0.8]{#int}_{  }L_{ }dt = ' + s + ' fb^{-1} ' ) )
    l.DrawLatex( x, y - size / 0.75 - size / 3.0, txt )
    ls = None
    if subtxt != None:
        ls = ROOT.TLatex()
        ls.SetNDC()
        ls.SetTextFont(42)
        ls.SetTextColor(color)
        ls.SetTextSize(size/1.25)
        ls.DrawLatex( x, y - 2.0*(size / 0.75) - size / 3.0, subtxt )
    return (l, ls)

# ----------- ============ ----------- ============ ----------- ============ -----------
def label(x, y, text, cv = None, angle = 0, color = ROOT.kBlack, size = globalcfg.labelFontSize):
    if cv != None:
        cv.cd( )
    TextSize = 0.05
    lText = ROOT.TLatex()
    lText.SetNDC()
    lText.SetTextSize(size)
    lText.SetTextColor(color)
    lText.SetTextAngle(angle)
    lText.DrawLatex(x,y,text)
    return lText

# ----------- ============ ----------- ============ ----------- ============ -----------
def applyAtlasLabels( cv, xd = 0, yd = 0, size = globalcfg.labelFontSize, lumi = -1, sub=None ):
    from globalcfg import atlaslabelX
    from globalcfg import atlaslabelY
    if globalcfg.atlaslabel == 'preliminary':
        return atlasAllLabels( xd + atlaslabelX, yd + atlaslabelY, lumi, cv, size = size,
                               preliminary = True, internal = False, subtxt=sub )
    if globalcfg.atlaslabel == 'internal':
        return atlasAllLabels( xd + atlaslabelX, yd + atlaslabelY, lumi, cv, size = size,
                               preliminary = False, internal = True, subtxt=sub )
    if globalcfg.atlaslabel == 'public':
        return atlasAllLabels( xd + atlaslabelX, yd + atlaslabelY, lumi, cv, size = size,
                               preliminary = False, internal = False, subtxt=sub )
    return None

