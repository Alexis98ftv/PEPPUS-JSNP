
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import conda
CondaFileDir = conda.__file__
CondaDir = CondaFileDir.split('lib')[0]
ProjLib = os.path.join(os.path.join(CondaDir, 'share'), 'proj')
os.environ["PROJ_LIB"] = ProjLib
from mpl_toolkits.basemap import Basemap

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

#import PlotsConstants as Const

def createFigure(PlotConf):
    if "Polar" in PlotConf: 
        projection = {'projection': 'polar'}
    else:
        projection = None

    try:
        fig, ax = plt.subplots(1, 1, figsize = PlotConf["FigSize"], subplot_kw = projection)
    
    except:
        fig, ax = plt.subplots(1, 1)

    return fig, ax

def saveFigure(fig, Path):
    Dir = os.path.dirname(Path)
    try:
        os.makedirs(Dir)
    except: pass
    fig.savefig(Path, dpi=150., bbox_inches='tight')

def prepareAxis(PlotConf, ax):

    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    for key in PlotConf:
        if key == "Title":
            ax.set_title(PlotConf["Title"])

        for axis in ["x", "y"]:
            if axis == "x":
                if key == axis + "Label":
                    ax.set_xlabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_xticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_xticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_xlim(PlotConf[axis + "Lim"])

            if axis == "y":
                if key == axis + "Label":
                    ax.set_ylabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_yticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_yticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_ylim(PlotConf[axis + "Lim"])            

        if key == "Grid" and PlotConf[key] == True:
            ax.grid(linestyle='--', linewidth=0.5, which='both')

        if key == "Polar":
            #------------------------
            # Center N and decide the direction
            ax.set_theta_offset(np.radians(90))
            ax.set_theta_direction(1)
            #-------------------
            # Central origin without radius
            ax.set_rorigin(-0)
            #-------------------
            # Visible limits
            ax.set_rlim(0,90) 
            #-------------------
            # thetagrid ticks, "N", "E", "S", "W"
            ax.set_thetagrids([0, 90, 180, 270], labels = ['N', 'W', 'S', 'E'])
            #-------------------
            # rgrid ticks, angle, labels
            ax.set_rgrids(range(0, 91, 10), angle=345,\
                           labels = ['90°','80°','70°','60°','50°','40°','30°','20°','10°','0°'])
            #------------------- set_x/yticks & set_x/yticklabels

            
def prepareDoubleAxis (PlotConf, ax2):
    for key in PlotConf:
        for axis in ["x2", "y2"]:
            if axis == "x2":
                if key == axis + "Label":
                    ax2.set_xlabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax2.set_xticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax2.set_xticklabels(PlotConf[axis + "TicksLabels"])
            
                if key == axis + "Lim":
                    ax2.set_xlim(PlotConf[axis + "Lim"])

            if axis == "y2":
                if key == axis + "Label":
                    ax2.set_ylabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax2.set_yticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax2.set_yticklabels(PlotConf[axis + "TicksLabels"])
            
                if key == axis + "Lim":
                    ax2.set_ylim(PlotConf[axis + "Lim"])

def prepareColorBar(PlotConf, ax, Values):
    try:
        Min = PlotConf["ColorBarMin"]
    except:
        Mins = []
        for v in Values.values():
            Mins.append(min(v))
        Min = min(Mins)
    try:
        Max = PlotConf["ColorBarMax"]
    except:
        Maxs = []
        for v in Values.values():
            Maxs.append(max(v))
        Max = max(Maxs)

    #ticks option in colorbarbase
    if "ColorBarTicks" in PlotConf:
        colorbarticks=PlotConf["ColorBarTicks"]
    else:
        colorbarticks=None
    
    normalize = mpl.cm.colors.Normalize(vmin=Min, vmax=Max)
    
    if "Polar" in PlotConf:
        color_ax, kwargs = mpl.colorbar.make_axes(ax, orientation="vertical", pad=0.05, fraction=0.05)
    else:
        divider = make_axes_locatable(ax)
        color_ax = divider.append_axes("right", size="3%", pad="2%")
    
    if "LutColorBar" in PlotConf:
        Lut = PlotConf["LutColorBar"]
    else:
        Lut = None
        
    cmap = mpl.cm.get_cmap(PlotConf["ColorBar"],Lut)
    cbar = mpl.colorbar.ColorbarBase(color_ax, 
        cmap=cmap,
        norm=mpl.colors.Normalize(vmin=Min, vmax=Max),
        label=PlotConf["ColorBarLabel"],
        ticks=colorbarticks
    )

    return normalize, cmap

def drawMap(PlotConf, ax,):
    Map = Basemap(projection = 'cyl',
    llcrnrlat  = PlotConf["LatMin"]-0,
    urcrnrlat  = PlotConf["LatMax"]+0,
    llcrnrlon  = PlotConf["LonMin"]-0,
    urcrnrlon  = PlotConf["LonMax"]+0,
    lat_ts     = 10,
    resolution = 'l',
    ax         = ax)

    # Draw map meridians
    Map.drawmeridians(
    np.arange(PlotConf["LonMin"],PlotConf["LonMax"]+1,PlotConf["LonStep"]),
    labels = [0,0,0,1],
    fontsize = 6,
    linewidth=0.2)
        
    # Draw map parallels
    Map.drawparallels(
    np.arange(PlotConf["LatMin"],PlotConf["LatMax"]+1,PlotConf["LatStep"]),
    labels = [1,0,0,0],
    fontsize = 6,
    linewidth=0.2)

    # Draw coastlines
    Map.drawcoastlines(linewidth=0.5)

    # Draw countries
    Map.drawcountries(linewidth=0.25)

def generateLinesPlot(PlotConf):
    LineWidth = 1.5
    Color = "b"
    fig, ax = createFigure(PlotConf)

    #Store the information of the curves and labels to plot a legend
    LegendCurve = None
    LegendLabel = None
    
    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]
        if key == "ColorBar":
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)

    for Label in PlotConf["yData"].keys():
        if "Color" in PlotConf and Label in PlotConf["Color"]:
            ColorData = PlotConf["Color"][Label]
        else:
            ColorData = Color

        if "ColorBar" in PlotConf:
            if "Color" in PlotConf and Label in PlotConf["Color"]:
                ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label],
                marker = PlotConf["Marker"],
                s = LineWidth,
                c = ColorData)
            else:
                ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label],
                marker = PlotConf["Marker"],
                s = LineWidth,
                c = cmap(normalize(np.array(PlotConf["zData"][Label]))))
        
        elif "BarPlot" in PlotConf:
            ax.bar(PlotConf["xData"][Label], PlotConf["yData"][Label],
            color = ColorData,
            width=PlotConf["WidthBar"],
            label = Label)
        else:
            ax.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
            PlotConf["Marker"],
            color = ColorData,
            label = Label,
            markersize = LineWidth)
            #LEGEND
            legendcurve , legendlabel = ax.get_legend_handles_labels()
            LegendCurve = legendcurve
            LegendLabel = legendlabel

        if "RejFlagAnnotate" in PlotConf:
            for i in range (len(PlotConf["zData"][Label])):
                if PlotConf["yData"][Label].iloc[i] != 2:
                    PRN = PlotConf["zData"][Label].iloc[i]
                    satlabel = "G" + ("%02d" % PRN)
                    ax.annotate(satlabel,
                                xy = (PlotConf["xData"][Label].iloc[i], PlotConf["yData"][Label].iloc[i]),
                                xytext = (PlotConf["xPosText"], PlotConf["yPosText"]),
                                textcoords = "offset points",
                                ha = "center",
                                fontsize = PlotConf["AnnFontSize"],
                                color = cmap(normalize(np.array(PlotConf["zData"][Label].iloc[i]))),
                                bbox = dict(boxstyle = "round", fc="w", ec="w")
                                )

        elif "Annotate" in PlotConf:
            for i in range(len(PlotConf["zData"][Label])):
                text = PlotConf["zData"][Label].iloc[i]
                ax.annotate(text,
                            xy = (PlotConf["xData"][Label].iloc[i], PlotConf["yData"][Label].iloc[i]),
                            xytext = (PlotConf["xPosText"], PlotConf["yPosText"]),
                            textcoords = "offset points",
                            ha = "center",
                            fontsize = PlotConf["AnnFontSize"],
                            color = cmap(normalize(np.array(PlotConf["zData"][Label].iloc[i])))
                            ,bbox = dict(boxstyle = "round", pad=0.05, fc="w", ec="w")
                            )
            if "RcvrTag" in PlotConf:
                for i in range(len(PlotConf["RcvrTag"][Label])):
                    RcvrText = PlotConf["RcvrTag"][Label].iloc[i]
                    ax.annotate(RcvrText,
                                xy = (PlotConf["xData"][Label].iloc[i], PlotConf["yData"][Label].iloc[i]),
                                xytext = (-5,-5),
                                textcoords = "offset points",
                                ha = "center",
                                fontsize = PlotConf["AnnFontSize"],
                                color = cmap(normalize(np.array(PlotConf["zData"][Label].iloc[i])))
                                ,bbox = dict(boxstyle = "round", pad=0.01, fc="w", ec="w")
                                )
        
        

        
    

    #TwinAx
    if "DoubleAx" in PlotConf:
        ax2 = ax.twinx()
        # label,ticks,lim,etc in Prepare Axes
        prepareDoubleAxis(PlotConf, ax2)
        for Label in PlotConf["zData"].keys():
            if "Color" in PlotConf:
                ColorData = PlotConf["Color"][Label]
            else:
                ColorData = Color
            if PlotConf["DoubleAx"] == Label:
                ax2.plot(PlotConf["xData"][Label], PlotConf["zData"][Label],
                PlotConf["Marker"],
                color = ColorData,
                label = Label,
                markersize = LineWidth)
                #LEGEND
                legendcurve , legendlabel = ax2.get_legend_handles_labels()
                LegendCurve.extend(legendcurve)
                LegendLabel.extend(legendlabel)
                
    #LEGEND             
    if "Legend" in PlotConf:
        plt.legend(LegendCurve, LegendLabel)
    if "LegendText" in PlotConf:
        plt.legend([PlotConf["LegendText"]])
    
    saveFigure(fig, PlotConf["Path"])
    plt.close('all')





def generatePlot(PlotConf):
    if(PlotConf["Type"] == "Lines"):
        generateLinesPlot(PlotConf)
    elif(PlotConf["Type"] == "Table"):
        generateTablePlot(PlotConf)


#

def generateTablePlot(PlotConf):
    LineWidth = 1
    Alpha = 1
    Colors = np.array(["tomato", "gold", "aquamarine", "darkturquoise"]) # LOOK OUT! Modify colors and range when needed
    CellData = [[0] * len(PlotConf["xData"]) for i in range(len(Colors))] # LOOK OUT! range automatically modified
    ColNames = []

    fig, ax = createFigure(PlotConf)

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]
        
        if "AxTable" not in PlotConf: # Normal X axis on Bar plot
            for Label in PlotConf["yData"].keys():
                ax.bar(PlotConf["xData"][Label], 
                       PlotConf["yData"][Label], 
                       linewidth=LineWidth, 
                       color=Colors)
        if "AxTable" in PlotConf: # Use a table as X axis on Bar plot
            Cn = 0 # Columns number (prn number). Reset every new epoch once all prn data are filled in
            for Label in PlotConf["yData"].keys():
                Rn = 0 # Rows number (Max, 95%, RMS, Min). Reset every new prn on same epoch once all 4 data rows are filled in
                for ydata in PlotConf["yData"][Label]:
                    ax.bar(Cn, 
                           ydata, 
                           linewidth=LineWidth, 
                           color=Colors[Rn])
                    CellData[Rn][Cn] = ("%1.2f" % (ydata)) # Fill in a position on celldata matrix
                    Rn += 1 # Increasing counter ([Max, 95%, RMS, Min] positions)
                
                Cn += 1 # Increasing counter (prn number)
                ColNames.append(Label)
            
            RowNames = [x for x in ("Max", "95%", "RMS", "Min")] # LOOK OUT! Modify when needed
            ColColors = np.array(Cn * ["lightgrey"])

            ax.table(cellText   = CellData,  
                     rowLabels  = RowNames,  
                     colLabels  = ColNames, 
                     rowColours = Colors,  
                     colColours = ColColors, 
                     cellLoc    = 'center',  
                     loc        = 'bottom')
            ax.set_xlim(left=-.5, right=len(PlotConf["xData"]) - 1 + .5)


    # Save figure
    saveFigure(fig, PlotConf["Path"])

####



#