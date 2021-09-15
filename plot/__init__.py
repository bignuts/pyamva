import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from typing import List
from reference import Reference
from matplotlib.figure import Figure
from matplotlib.axes import Axes


class MakeRectangle:

    @staticmethod
    def make_rectangle(ref: Reference) -> List[Rectangle]:
        l: List[Rectangle] = []
        # ref.tpo_profile.to_csv('tpo.csv')
        # ref.sub_profile.to_csv('sub.csv')
        for col in ref.tpo_profile.itertuples():
            l.append(Rectangle((0, col.price), col.count,
                               ref.param.tpo_size, facecolor='r', edgecolor='k'))
        # togli ultimo elemento, verrebbe troppo alto
        l.pop()
        return l


class MakeDistribution:

    @staticmethod
    def make_distribution(ref: Reference) -> List[Rectangle]:
        l: List[Rectangle] = []
        poc_len = ref.tpo_profile['count'].max()
        for distr in ref.distr:
            # ll and ul
            l.append(Rectangle((0, distr.ll), poc_len, distr.ul -
                               distr.ll + ref.param.tpo_size, edgecolor="gray", fill=False))
            # lo and uo
            l.append(Rectangle((0, distr.lo), poc_len, distr.uo-distr.lo + ref.param.tpo_size,
                               edgecolor="gray", fill=False, linestyle="dashed"))
            # lq and uq
            l.append(Rectangle((0, distr.lq), poc_len, distr.uq-distr.lq + ref.param.tpo_size,
                               edgecolor="gray", fill=False, linestyle="dashed"))
            # mid
            l.append(Rectangle((0, distr.mid), poc_len, 0,
                               edgecolor="gray", fill=False, linestyle="dashed"))
        return l


class MakeCloseLine:

    @staticmethod
    def make_close_line(ref: Reference) -> List[Rectangle]:
        poc_len = ref.tpo_profile['count'].max()
        l: List[Rectangle] = []
        l.append(Rectangle((0, ref.close-1),
                           poc_len, 2, facecolor='k', edgecolor='k'))
        return l


class PlotSingleComposite:

    def __init__(self, fig, ax):
        self.__fig = fig
        self.__ax = ax
        self.__collection: List = []
        plt.style.use('seaborn')

    def plot(self, ref: Reference) -> None:
        self.__collection += MakeRectangle.make_rectangle(ref)
        self.__collection += MakeDistribution.make_distribution(ref)
        self.__collection += MakeCloseLine.make_close_line(ref)
        pc = PatchCollection(self.__collection, match_original=True)
        self.__ax.add_collection(pc)
        self.__ax.set_title(f'{ref.count} days')
        self.__ax.plot()


class PlotMultipleComposite:

    def __init__(self, nrows: int):
        self.__fig, self.__ax = plt.subplots(ncols=1, nrows=nrows)
        self.__collection: List = []

    def plot(self, ref_list: List[Reference]) -> None:
        for index, ref in enumerate(ref_list):
            self.__collection + MakeRectangle.make_rectangle(ref)
            # accedi agli assi
            self.__ax[index].add_collection(self.__collection)
        plt.show()


class PlotComposite:

    def __init__(self) -> None:
        self.__fig: Figure
        self.__ax: Axes

    def plot_single(self, ref: Reference) -> None:
        self.__fig, self.__ax = plt.subplots(ncols=1, nrows=1)
        single = PlotSingleComposite(self.__fig, self.__ax)
        single.plot(ref)

        self.__fig.canvas.set_window_title('Composite Profiles')
        plt.show()

    def plot_multiple(self, ref_list: List[Reference]):
        ref_list = ref_list[1:]
        self.__fig, self.__ax = plt.subplots(
            ncols=len(ref_list), nrows=1, sharey=True)
        for index, ref in enumerate(ref_list):
            PlotSingleComposite(self.__fig, self.__ax[-(index+1)]).plot(ref)

        plt.subplots_adjust(left=0.05, bottom=0.04, right=0.99,
                            top=0.96, wspace=0.05, hspace=0.20)

        self.__fig.canvas.set_window_title('Composite Profiles')
        plt.show()
